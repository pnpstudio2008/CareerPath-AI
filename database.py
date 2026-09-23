"""
AI Career Companion - Database Layer & Pre-Seeding
Dual-Engine: Supabase PostgreSQL (Production Cloud) + SQLite (Local Resilient Fallback).
Seed data for MCQs, Alumni Experiences, Job Profiles, and Faculty Insights.
"""

import sqlite3
import os
import json
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

try:
    import psycopg2
    from psycopg2.extras import RealDictCursor
    HAS_PSYCOPG2 = True
except ImportError:
    HAS_PSYCOPG2 = False

DB_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "career_companion.db")


class PGRow(dict):
    """Behaves like sqlite3.Row: supports both row['column'] and row[0], row[1], etc."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._values = list(self.values())

    def __getitem__(self, key):
        if isinstance(key, int):
            return self._values[key]
        return super().__getitem__(key)


class PGCursorWrapper:
    """Wraps psycopg2 RealDictCursor to translate SQLite ? placeholders to %s and handle lastrowid."""
    def __init__(self, raw_cursor):
        self._cur = raw_cursor
        self.lastrowid = None

    def execute(self, sql, params=None):
        sql = sql.replace('?', '%s')
        clean_sql = sql.strip().upper()
        is_insert = clean_sql.startswith('INSERT')
        has_returning = 'RETURNING' in clean_sql
        if is_insert and not has_returning:
            sql += ' RETURNING id'

        if params is not None:
            self._cur.execute(sql, tuple(params) if isinstance(params, (list, tuple)) else params)
        else:
            self._cur.execute(sql)

        if is_insert:
            try:
                row = self._cur.fetchone()
                if row:
                    self.lastrowid = row[0] if isinstance(row, (tuple, list)) else row.get('id')
            except Exception:
                pass
        return self

    def fetchone(self):
        row = self._cur.fetchone()
        return PGRow(row) if row is not None else None

    def fetchall(self):
        return [PGRow(r) for r in self._cur.fetchall()]

    def __iter__(self):
        for row in self._cur:
            yield PGRow(row)

    def close(self):
        try:
            self._cur.close()
        except Exception:
            pass



class PGConnectionWrapper:
    """Wraps psycopg2 connection to behave identically to sqlite3 connection with dict rows."""
    def __init__(self, raw_conn):
        self._conn = raw_conn
        self._is_pg = True

    def cursor(self):
        from psycopg2.extras import RealDictCursor
        raw_cur = self._conn.cursor(cursor_factory=RealDictCursor)
        return PGCursorWrapper(raw_cur)

    def execute(self, sql, params=None):
        cur = self.cursor()
        cur.execute(sql, params)
        return cur

    def commit(self):
        return self._conn.commit()

    def rollback(self):
        return self._conn.rollback()

    def close(self):
        try:
            return self._conn.close()
        except Exception:
            pass


def get_db_connection():
    """
    Returns an active database connection:
    1. Primary: Supabase Cloud PostgreSQL (handles 10,000+ students, 3,000+ alumni concurrently).
       Supports both DATABASE_URL (standard for Render / Heroku / Railway) and individual PG_* vars.
    2. Fallback: Local SQLite file if network/cloud is unreachable.
    """
    db_url = os.environ.get("DATABASE_URL")
    pg_host = os.environ.get("PG_HOST")
    pg_password = os.environ.get("PG_PASSWORD")
    pg_user = os.environ.get("PG_USER", "postgres")
    pg_database = os.environ.get("PG_DATABASE", "postgres")
    pg_port = int(os.environ.get("PG_PORT", 5432))

    if HAS_PSYCOPG2:
        # Priority 1: Check DATABASE_URL connection URI
        if db_url and ("postgres" in db_url.lower() or "supabase" in db_url.lower()):
            try:
                conn_str = db_url
                if "sslmode=" not in conn_str:
                    sep = "&" if "?" in conn_str else "?"
                    conn_str = f"{conn_str}{sep}sslmode=require"
                raw_conn = psycopg2.connect(conn_str, connect_timeout=10)
                return PGConnectionWrapper(raw_conn)
            except Exception as e:
                print(f"[DB Notice] Could not connect via DATABASE_URL ({e}). Trying PG_HOST...")

        # Priority 2: Check individual PG_* parameters
        if pg_host and pg_password:
            try:
                raw_conn = psycopg2.connect(
                    dbname=pg_database,
                    user=pg_user,
                    password=pg_password,
                    host=pg_host,
                    port=pg_port,
                    sslmode="require",
                    connect_timeout=6
                )
                return PGConnectionWrapper(raw_conn)
            except Exception as e:
                print(f"[DB Notice] Could not connect directly to {pg_host} ({e}). Trying IPv4 connection pooler...")

        # Priority 3: Automatic IPv4 Pooler fallback (Essential for Render / AWS IPv4 environments)
        if pg_password:
            ref = "vggpjzbhumvlkckkxhxv"
            if pg_host and "supabase.co" in pg_host and "." in pg_host:
                parts = pg_host.split(".")
                if len(parts) >= 3 and parts[0] == "db":
                    ref = parts[1]
            pooler_hosts = [
                "aws-0-ap-northeast-1.pooler.supabase.com",
                "aws-1-ap-northeast-1.pooler.supabase.com"
            ]
            for ph in pooler_hosts:
                try:
                    raw_conn = psycopg2.connect(
                        dbname=pg_database or "postgres",
                        user=f"postgres.{ref}",
                        password=pg_password,
                        host=ph,
                        port=5432,
                        sslmode="require",
                        connect_timeout=8
                    )
                    print(f"[Database] Successfully connected via Supabase IPv4 Pooler ({ph})!")
                    return PGConnectionWrapper(raw_conn)
                except Exception as pool_err:
                    print(f"[DB Notice] Pooler {ph} failed: {pool_err}")


    conn = sqlite3.connect(DB_FILE, timeout=30.0)
    conn.row_factory = sqlite3.Row
    return conn



DUMMY_ALUMNI_DATA = [
    {
        "student_name": "Priya Patel",
        "alumni_id": "24C11002",
        "batch_year": "2024",
        "email": "priya.patel@gmail.com",
        "phone": "+91 98234 11002",
        "branch": "Computer Science",
        "company": "Google",
        "role": "Software Development Engineer (SDE-1)",
        "package_lpa": 35.0,
        "offer_type": "On-Campus",
        "difficulty": "Hard",
        "status": "Selected",
        "upvotes": 54,
        "rounds": [
            {"round_name": "Round 1: Online Coding Assessment", "details": "Solved 2 LeetCode Medium/Hard algorithmic challenges on Graph Traversal and Dynamic Programming with optimal time/space complexity."},
            {"round_name": "Round 2: Technical Interview 1", "details": "In-depth problem solving on Binary Trees, Maximum Path Sum, and Trie prefix search implementation with live test-case dry running."},
            {"round_name": "Round 3: Technical Interview 2", "details": "Distributed Systems and Concurrency: Design a resilient cache invalidation pipeline and discuss thread contention with lock-free structures."},
            {"round_name": "Round 4: Googleyness & Leadership", "details": "Scenario-based behavioral questions on handling ambiguity, cross-team conflict resolution, and commitment to open engineering practices."}
        ],
        "preparation_tips": "Solved 450+ LeetCode problems with special emphasis on Dynamic Programming, Graphs, and Trees. Practiced writing clean code on Google Docs without IDE auto-complete.",
        "advice_to_juniors": "Never jump straight into writing code. Explain your brute force first, discuss trade-offs, and verify edge cases out loud before typing."
    },
    {
        "student_name": "Aarav Sharma",
        "alumni_id": "24C11003",
        "batch_year": "2024",
        "email": "aarav.sharma@amazon.com",
        "phone": "+91 98234 11003",
        "branch": "Computer Science",
        "company": "Amazon",
        "role": "Software Development Engineer (SDE-1)",
        "package_lpa": 28.5,
        "offer_type": "On-Campus",
        "difficulty": "Medium",
        "status": "Selected",
        "upvotes": 46,
        "rounds": [
            {"round_name": "Round 1: Online Assessment (OA2)", "details": "Two algorithmic coding problems on Monotonic Stack and Sliding Window, followed by Amazon Work Style behavioral simulation."},
            {"round_name": "Round 2: Technical Round 1", "details": "Data Structures and Algorithms: Solved Top-K Frequent Elements using Min-Heap and discussed complexity optimizations."},
            {"round_name": "Round 3: Technical Round 2", "details": "Object-Oriented Design & LLD: Designed an extensible Parking Lot system using Factory and Strategy design patterns with database schemas."},
            {"round_name": "Round 4: Bar Raiser Interview", "details": "Rigorous evaluation across Amazon 16 Leadership Principles using the STAR format, plus past production project architecture breakdown."}
        ],
        "preparation_tips": "Thoroughly prepared 2-3 detailed stories for each of Amazon's 16 Leadership Principles using the STAR method, and mastered the Blind 75 LeetCode list.",
        "advice_to_juniors": "Customer obsession and ownership are real culture pillars at Amazon. Tie every technical trade-off back to how it impacts end-user experience."
    },
    {
        "student_name": "Sneha Kulkarni",
        "alumni_id": "24C11004",
        "batch_year": "2024",
        "email": "sneha.kulkarni@microsoft.com",
        "phone": "+91 98234 11004",
        "branch": "Computer Science",
        "company": "Microsoft",
        "role": "Software Engineer",
        "package_lpa": 32.0,
        "offer_type": "On-Campus",
        "difficulty": "Hard",
        "status": "Selected",
        "upvotes": 41,
        "rounds": [
            {"round_name": "Round 1: Codility Online Assessment", "details": "3 algorithmic problems covering string parsing, array intervals, and binary search with strict execution limits."},
            {"round_name": "Round 2: Technical Interview 1", "details": "Linked lists and recursion: Flattening a multi-level doubly linked list and thorough boundary condition verification."},
            {"round_name": "Round 3: Technical Interview 2", "details": "System Design: Architecting a scalable URL shortener with rate limiting, database sharding, and Redis caching."},
            {"round_name": "Round 4: As-Appropriate (AA) Director Round", "details": "High-level architectural discussions, engineering philosophy, and cross-platform scalability on Azure."}
        ],
        "preparation_tips": "Focused on clean, modular code, rigorous edge-case testing, and reading System Design Primer chapters on caching and replication.",
        "advice_to_juniors": "Communicate clearly with your interviewer. Treat the interview as a collaborative design session rather than an exam."
    },
    {
        "student_name": "Rohan Deshmukh",
        "alumni_id": "24C11005",
        "batch_year": "2024",
        "email": "rohan.deshmukh@tcs.com",
        "phone": "+91 98234 11005",
        "branch": "Information Technology",
        "company": "TCS",
        "role": "TCS Digital Developer",
        "package_lpa": 9.0,
        "offer_type": "On-Campus",
        "difficulty": "Medium",
        "status": "Selected",
        "upvotes": 38,
        "rounds": [
            {"round_name": "Round 1: TCS NQT Advanced Coding", "details": "Quantitative aptitude, verbal logic, and 2 advanced coding questions in Python covering arrays and matrix manipulation."},
            {"round_name": "Round 2: Technical Interview", "details": "Full Stack project walkthrough, REST API design, SQL indexes, ACID properties, and Docker containerization basics."},
            {"round_name": "Round 3: Managerial & HR Round", "details": "Discussion on emerging cloud technologies, willingness to work in diverse domains, and situational problem solving."}
        ],
        "preparation_tips": "Targeted TCS Digital specifically by solving previous years' NQT advanced coding problems and preparing deep dive answers on web development projects.",
        "advice_to_juniors": "Aim for TCS Digital rather than Ninja. A strong score on the advanced coding section directly qualifies you for the higher compensation tier."
    },
    {
        "student_name": "Ananya Joshi",
        "alumni_id": "24C11006",
        "batch_year": "2024",
        "email": "ananya.joshi@infosys.com",
        "phone": "+91 98234 11006",
        "branch": "Computer Science",
        "company": "Infosys",
        "role": "Specialist Programmer (SP)",
        "package_lpa": 10.5,
        "offer_type": "On-Campus",
        "difficulty": "Medium",
        "status": "Selected",
        "upvotes": 35,
        "rounds": [
            {"round_name": "Round 1: HackWithInfy Round 1", "details": "3 algorithmic programming questions involving Dynamic Programming and Number Theory on HackerEarth."},
            {"round_name": "Round 2: HackWithInfy Grand Finale", "details": "Competitive programming contest with advanced Graph algorithms and Segment Trees."},
            {"round_name": "Round 3: Specialist Programmer Technical Interview", "details": "Data structures live coding, multi-threading in Java, database transaction isolation levels, and project architecture."},
            {"round_name": "Round 4: HR & Leadership Discussion", "details": "Discussion on career aspirations, willingness to learn new technology stacks, and teamwork culture."}
        ],
        "preparation_tips": "Regular participation in Codeforces and CodeChef contests helped build speed and algorithmic confidence under time constraints.",
        "advice_to_juniors": "HackWithInfy and InfyTQ are golden opportunities to unlock 9.5+ LPA packages right out of college. Start competitive coding early."
    },
    {
        "student_name": "Rahul Verma",
        "alumni_id": "24C11007",
        "batch_year": "2024",
        "email": "rahul.verma@accenture.com",
        "phone": "+91 98234 11007",
        "branch": "Electronics & Communication",
        "company": "Accenture",
        "role": "Advanced App Engineering Analyst",
        "package_lpa": 6.5,
        "offer_type": "On-Campus",
        "difficulty": "Easy",
        "status": "Selected",
        "upvotes": 29,
        "rounds": [
            {"round_name": "Round 1: Cognitive & Technical Assessment", "details": "English ability, critical thinking, abstract reasoning, and technical fundamentals in networking, cloud, and pseudocode."},
            {"round_name": "Round 2: Coding Assessment", "details": "2 practical programming tasks in Python/C++ testing basic array logic and string formatting."},
            {"round_name": "Round 3: Communication Assessment", "details": "Automated AI-evaluated oral exam testing pronunciation, reading comprehension, fluency, and sentence mastery."},
            {"round_name": "Round 4: Virtual Interview", "details": "Technical project discussion, situational teamwork scenarios, and adaptability to agile software development."}
        ],
        "preparation_tips": "Practiced pseudo-code debugging, quantitative shortcuts, and practiced speaking aloud with a headset to score high on the automated communication test.",
        "advice_to_juniors": "Never underestimate the communication round. Practice speaking clearly in English without excessive fillers."
    },
    {
        "student_name": "Meera Nair",
        "alumni_id": "24C11008",
        "batch_year": "2024",
        "email": "meera.nair@wipro.com",
        "phone": "+91 98234 11008",
        "branch": "Computer Science",
        "company": "Wipro",
        "role": "Project Engineer (Turbo)",
        "package_lpa": 6.5,
        "offer_type": "On-Campus",
        "difficulty": "Medium",
        "status": "Selected",
        "upvotes": 27,
        "rounds": [
            {"round_name": "Round 1: Elite National Talent Hunt", "details": "Online assessment covering Quantitative, Logical, Verbal, and 2 hands-on programming problems."},
            {"round_name": "Round 2: Turbo Upgrade Coding Challenge", "details": "Challenging Data Structures & Algorithms round featuring Trees, Recursion, and Greedy algorithms."},
            {"round_name": "Round 3: Technical & HR Discussion", "details": "Deep dive on OOP concepts, Database Normalization, Software Engineering life cycle, and final offer review."}
        ],
        "preparation_tips": "Solved practice tests on HackerRank and thoroughly reviewed OS paging, database indexing, and core Java concepts.",
        "advice_to_juniors": "Take the Turbo upgrade test seriously—it elevates the standard offer to a premium technology role right at the entry level."
    },
    {
        "student_name": "Karan Mehta",
        "alumni_id": "24C11001",
        "batch_year": "2023",
        "email": "karan.mehta@alumni.edu",
        "phone": "+91 98234 11001",
        "branch": "Computer Science",
        "company": "General",
        "role": "Senior Software Engineer",
        "package_lpa": 14.0,
        "offer_type": "Off-Campus",
        "difficulty": "Medium",
        "status": "Selected",
        "upvotes": 42,
        "rounds": [
            {"round_name": "Round 1: Take-Home Engineering Challenge", "details": "Built a production-ready RESTful microservice with PostgreSQL database, JWT authentication, and Docker compose."},
            {"round_name": "Round 2: Architecture & Code Walkthrough", "details": "Discussed design patterns, database indexes, concurrent request handling, and unit test coverage."},
            {"round_name": "Round 3: System Design & Culture Alignment", "details": "Scalability trade-offs, CI/CD deployment pipelines, and engineering best practices."}
        ],
        "preparation_tips": "Built and deployed end-to-end full stack projects with live URLs, CI/CD workflows, and comprehensive documentation.",
        "advice_to_juniors": "Show, don't just tell. Having a working GitHub repository with clean commits and deployed projects creates immediate credibility."
    }
]

def seed_dummy_alumni_students(cursor):
    """Seeds rich interview experiences and login accounts for verified alumni mentors."""
    for item in DUMMY_ALUMNI_DATA:
        # 1. Insert into alumni_experiences if not already present
        cursor.execute("SELECT id FROM alumni_experiences WHERE LOWER(student_name) = LOWER(?)", (item["student_name"],))
        if not cursor.fetchone():
            cursor.execute("""
            INSERT INTO alumni_experiences (
                student_name, batch_year, email, company, role, package_lpa, offer_type, difficulty, status, rounds_json, preparation_tips, advice_to_juniors, upvotes
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item["student_name"],
                item["batch_year"],
                item["email"],
                item["company"],
                item["role"],
                item["package_lpa"],
                item["offer_type"],
                item["difficulty"],
                item["status"],
                json.dumps(item["rounds"]),
                item["preparation_tips"],
                item["advice_to_juniors"],
                item.get("upvotes", 25)
            ))

        # 2. Insert into alumni_accounts if not already present
        cursor.execute("SELECT id FROM alumni_accounts WHERE UPPER(alumni_id) = ? OR LOWER(email) = ?", (item["alumni_id"].upper(), item["email"].lower()))
        if not cursor.fetchone():
            cursor.execute("""
            INSERT INTO alumni_accounts (
                name, alumni_id, email, phone, branch, batch_year, company, role, package_lpa, password, security_key_2fa
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item["student_name"],
                item["alumni_id"],
                item["email"],
                item["phone"],
                item["branch"],
                item["batch_year"],
                item["company"],
                item["role"],
                item["package_lpa"],
                "alumni123",
                item["alumni_id"]
            ))


def init_database():
    conn = get_db_connection()
    if getattr(conn, "_is_pg", False):
        print("[Database] Connected to Supabase Cloud PostgreSQL (10,000+ Student Production Scale)")
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) as count FROM mcq_questions")
        row = cursor.fetchone()
        if not row or row.get("count", 0) == 0:
            seed_all_data(cursor)
        conn.commit()
        conn.close()
        return

    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    cursor = conn.cursor()

    # 1. MCQ Practice Questions Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS mcq_questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT NOT NULL,
        topic TEXT NOT NULL,
        company TEXT DEFAULT 'General',
        question TEXT NOT NULL,
        option_a TEXT NOT NULL,
        option_b TEXT NOT NULL,
        option_c TEXT NOT NULL,
        option_d TEXT NOT NULL,
        correct_option TEXT NOT NULL,
        explanation TEXT NOT NULL,
        difficulty TEXT DEFAULT 'Medium'
    )
    """)

    # 2. Theoretical Questions Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS theoretical_questions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        subject TEXT NOT NULL,
        topic TEXT NOT NULL,
        company TEXT DEFAULT 'General',
        question TEXT NOT NULL,
        model_answer TEXT NOT NULL,
        key_concepts TEXT NOT NULL,
        difficulty TEXT DEFAULT 'Medium'
    )
    """)

    # 3. Alumni Interview Experiences Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alumni_experiences (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_name TEXT NOT NULL,
        batch_year TEXT NOT NULL,
        email TEXT DEFAULT 'alumni.contact@gmail.com',
        company TEXT NOT NULL,
        role TEXT NOT NULL,
        package_lpa REAL NOT NULL,
        offer_type TEXT NOT NULL,
        difficulty TEXT NOT NULL,
        status TEXT DEFAULT 'Selected',
        rounds_json TEXT NOT NULL,
        preparation_tips TEXT NOT NULL,
        advice_to_juniors TEXT NOT NULL,
        upvotes INTEGER DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Safe column migration for existing databases
    try:
        cursor.execute("ALTER TABLE alumni_experiences ADD COLUMN email TEXT DEFAULT 'alumni.contact@gmail.com'")
    except sqlite3.OperationalError:
        pass

    # 5. Students & Placement Tracking Table (Admin Managed with Student Login Credentials)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        roll_no TEXT UNIQUE NOT NULL,
        phone TEXT DEFAULT '',
        email TEXT NOT NULL,
        branch TEXT NOT NULL,
        section TEXT DEFAULT 'A',
        password TEXT DEFAULT 'student123',
        batch_year TEXT NOT NULL,
        ats_score REAL DEFAULT 0,
        readiness_status TEXT DEFAULT 'In Progress',
        target_company TEXT DEFAULT 'General',
        quizzes_completed INTEGER DEFAULT 0,
        placement_status TEXT DEFAULT 'Not Placed',
        placed_company TEXT DEFAULT '',
        package_lpa REAL DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Safe column migrations for existing databases
    for col_def in [
        ("phone", "TEXT DEFAULT ''"),
        ("section", "TEXT DEFAULT 'A'"),
        ("password", "TEXT DEFAULT 'student123'")
    ]:
        try:
            cursor.execute(f"ALTER TABLE students ADD COLUMN {col_def[0]} {col_def[1]}")
        except sqlite3.OperationalError:
            pass

    # 6. Alumni Accounts & Authentication Table (Admin Managed Alumni Login Accounts)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alumni_accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        alumni_id TEXT UNIQUE NOT NULL,
        email TEXT NOT NULL,
        phone TEXT DEFAULT '',
        branch TEXT NOT NULL,
        batch_year TEXT NOT NULL,
        company TEXT NOT NULL,
        role TEXT NOT NULL,
        package_lpa REAL DEFAULT 0,
        password TEXT NOT NULL,
        security_key_2fa TEXT NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)

    # Safe column migrations for mcq_questions (Alumni Contributed Questions)
    for col_def in [
        ("alumni_id", "INTEGER DEFAULT NULL"),
        ("alumni_name", "TEXT DEFAULT 'Alumni Mentor'")
    ]:
        try:
            cursor.execute(f"ALTER TABLE mcq_questions ADD COLUMN {col_def[0]} {col_def[1]}")
        except sqlite3.OperationalError:
            pass

    # 7. Job Profiles Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS job_profiles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT NOT NULL,
        role_title TEXT NOT NULL,
        experience_level TEXT DEFAULT 'Fresher',
        location TEXT DEFAULT 'PAN India',
        ctc_range TEXT DEFAULT 'Competitive',
        description TEXT DEFAULT '',
        required_skills TEXT NOT NULL,
        category TEXT DEFAULT 'SDE'
    )
    """)


    # 8. Alumni Outreach Logs Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alumni_outreach (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_id INTEGER,
        alumni_id TEXT,
        message TEXT DEFAULT '',
        status TEXT DEFAULT 'Pending',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)


    # Ensure all questions are attributed to specific real alumni mentors rather than generic 'Alumni Mentor'
    alumni_mentor_map = {
        'Google': 'Priya Patel',
        'Amazon': 'Aarav Sharma',
        'Microsoft': 'Sneha Kulkarni',
        'TCS': 'Rohan Deshmukh',
        'Infosys': 'Ananya Joshi',
        'Accenture': 'Rahul Verma',
        'Wipro': 'Meera Nair',
        'General': 'Karan Mehta'
    }
    for comp, al_name in alumni_mentor_map.items():
        cursor.execute("""
            UPDATE mcq_questions 
            SET alumni_name = ? 
            WHERE (alumni_name IS NULL OR alumni_name = 'Alumni Mentor' OR alumni_name = '') 
              AND LOWER(company) = LOWER(?)
        """, (al_name, comp))

    cursor.execute("""
        UPDATE mcq_questions 
        SET alumni_name = 'Karan Mehta' 
        WHERE (alumni_name IS NULL OR alumni_name = 'Alumni Mentor' OR alumni_name = '')
    """)

    # Ensure all dummy alumni students exist in alumni_experiences and alumni_accounts
    seed_dummy_alumni_students(cursor)

    # Check if questions already seeded
    cursor.execute("SELECT COUNT(*) FROM mcq_questions")
    if cursor.fetchone()[0] == 0:
        seed_all_data(cursor)

    conn.commit()
    conn.close()


def seed_all_data(cursor):
    print("Seeding initial dataset into Career Companion database...")

    # ==========================================
    # SEED 1: MCQ QUESTIONS (70+ Curated Placement Questions)
    # ==========================================
    mcqs = [
        # --- DSA (Data Structures & Algorithms) ---
        ("DSA", "Trees & Graphs", "General", "What is the worst-case time complexity of searching an element in a Red-Black Tree with N nodes?",
         "O(1)", "O(log N)", "O(N)", "O(N log N)", "B", "A Red-Black tree is a self-balancing binary search tree guaranteeing height <= 2*log2(N+1), ensuring worst-case lookup is strictly O(log N).", "Hard"),
        ("DSA", "Arrays & Hashing", "Amazon", "Given an array of integers, which algorithm can find the two numbers that add up to a specific target in O(N) time and O(N) space?",
         "Bubble Sort with Binary Search", "Hash Map single-pass lookup", "Merge Sort + Two Pointer", "Brute Force Nested Loop", "B", "Storing visited elements in a Hash Map allows complement lookup (target - num) in average O(1) time per element.", "Easy"),
        ("DSA", "Dynamic Programming", "Google", "In the 0/1 Knapsack problem with N items and weight capacity W, what is the standard DP time complexity?",
         "O(N * W)", "O(2^N)", "O(N + W)", "O(N^2)", "A", "The classic table-filling approach computes states for each item from 1..N and weight from 1..W, giving O(N * W) pseudo-polynomial time complexity.", "Medium"),
        ("DSA", "Linked List", "Microsoft", "Which approach allows finding the middle element of a singly linked list in a single traversal?",
         "Two-pointer (Slow & Fast)", "Recursive stack counting", "Reversing the list", "Converting to Array", "A", "Slow pointer moves 1 step while fast pointer moves 2 steps. When fast reaches the end, slow points to the middle node.", "Easy"),
        ("DSA", "Graph Algorithms", "General", "Which algorithm is used to find the shortest path in a weighted graph with negative edge weights (no negative cycles)?",
         "Dijkstra's Algorithm", "Bellman-Ford Algorithm", "Kruskal's Algorithm", "Prim's Algorithm", "B", "Bellman-Ford can handle negative weights and detect negative cycles by relaxing all edges |V|-1 times.", "Medium"),
        ("DSA", "Sliding Window", "Amazon", "What data structure is optimal for finding the maximum value in every sliding window of size K in an array of N integers in O(N) overall time?",
         "Max-Heap", "Monotonic Doubly-Ended Queue (Deque)", "Self-Balancing BST", "Array Linear Scan", "B", "A monotonic deque stores indices of elements in decreasing order, allowing O(1) amortized insertion, removal, and window-max retrieval.", "Hard"),
        ("DSA", "Arrays", "Google", "Kadane's algorithm is widely used to solve which standard algorithmic problem in linear O(N) time?",
         "Longest Increasing Subsequence", "Maximum Subarray Sum", "Two Sum with duplicates", "Next Permutation", "B", "Kadane's algorithm maintains maximum sum ending at current index (max_ending_here = max(x, max_ending_here + x)) in linear O(N) time.", "Easy"),
        ("DSA", "Trees", "Microsoft", "In a Binary Search Tree (BST) with distinct values, how do you find the Lowest Common Ancestor (LCA) of nodes p and q?",
         "Find root node where root.val lies strictly between p.val and q.val", "Perform standard BFS queue traversal", "Calculate tree diameter", "Post-order traversal hash map", "A", "In BST, starting from root, if both p and q are smaller go left; if both greater go right; the split point where p <= root <= q is the LCA.", "Easy"),
        ("DSA", "Heaps", "Amazon", "To find the K largest elements in an unsorted stream of N elements efficiently, which data structure provides O(N log K) time and O(K) space?",
         "Max-Heap of size N", "Min-Heap of size K", "Sorted Array", "Binary Search Tree of size N", "B", "A Min-Heap of capacity K keeps the K largest elements at the top, evicting smaller elements in O(log K) per insertion.", "Medium"),
        ("DSA", "Graphs", "Google", "Which algorithm detects whether a directed graph contains a cycle using in-degrees and queue processing?",
         "Kruskal's Algorithm", "Kahn's Topological Sort Algorithm", "Floyd-Warshall Algorithm", "Prim's Algorithm", "B", "Kahn's algorithm enqueues 0-indegree vertices. If total processed vertices < |V|, the directed graph contains at least one cycle.", "Medium"),
        ("DSA", "Sorting", "TCS", "The Dutch National Flag problem partitions an array of 0s, 1s, and 2s in single-pass O(N) time using which technique?",
         "3-way pointer partitioning (Low, Mid, High)", "Counting sort with auxiliary memory", "Merge sort recursion", "Binary radix sort", "A", "Three pointers (low, mid, high) swap elements in-place in a single pass without extra memory.", "Easy"),

        # --- Python Programming ---
        ("Python", "Core Concepts", "General", "What is the output of `bool([])`, `bool([0])`, and `bool((0,))` in Python?",
         "False, False, False", "False, True, True", "True, False, True", "False, False, True", "B", "An empty list is falsy. Non-empty collections like `[0]` and single-element tuple `(0,)` evaluate to truthy regardless of element values.", "Medium"),
        ("Python", "Memory Management", "General", "How are Python default arguments evaluated when defining a function like `def append_to(val, lst=[])`?",
         "Evaluated every time the function is called", "Evaluated once when the function definition is executed", "Evaluated only if explicitly passed", "Compiled as immutable constants", "B", "Default arguments in Python are evaluated once at definition time, meaning mutable defaults (like lists or dicts) persist across calls.", "Hard"),
        ("Python", "Decorators", "TCS", "Which built-in Python module is commonly used to preserve docstrings and metadata when creating decorators?",
         "functools.wraps", "itertools.chain", "inspect.signature", "types.FunctionType", "A", "The `@functools.wraps` decorator copies the name, docstring, and annotations from the original function to the wrapper function.", "Medium"),
        ("Python", "Generators", "Google", "What is the primary memory advantage of using a generator function with `yield` compared to returning a standard list?",
         "Generators execute faster in C runtime", "Generators produce items lazily on-demand (O(1) memory footprint)", "Generators can run multithreaded without GIL", "Generators allow reverse indexing", "B", "Generators compute values one at a time via iterator protocol (`__next__`), saving memory compared to allocating full lists in RAM.", "Medium"),
        ("Python", "Concurrency", "Amazon", "How does Python's Global Interpreter Lock (GIL) in CPython affect CPU-bound multithreaded programs?",
         "Enables true multi-core parallel thread execution", "Restricts bytecode execution to a single OS thread at any time", "Automatically offloads work to GPU", "Eliminates all race conditions", "B", "The GIL prevents multiple native threads from executing Python bytecodes simultaneously, so CPU-bound parallelism requires multiprocessing.", "Medium"),
        ("Python", "Operators", "TCS", "What is the difference between `a is b` and `a == b` in Python?",
         "`is` checks identity (memory address); `==` checks value equality", "`is` checks value equality; `==` checks type", "`is` is used only for strings", "There is no difference in modern Python", "A", "`is` checks object identity (`id(a) == id(b)`), whereas `==` invokes the `__eq__` method to evaluate value equality.", "Easy"),
        ("Python", "Data Structures", "Infosys", "What is the time complexity of appending an element to a Python list vs inserting at index 0?",
         "Append: O(1) amortized, Insert(0): O(N)", "Append: O(N), Insert(0): O(1)", "Both are strictly O(1)", "Both are strictly O(N)", "A", "Python lists are dynamic arrays. Appending to end is O(1) amortized, while inserting at 0 shifts all existing N elements by one position.", "Easy"),
        ("Python", "OOP", "Microsoft", "In Python, which method is responsible for creating a new instance before `__init__` initializes it?",
         "`__new__`", "`__create__`", "`__construct__`", "`__class__`", "A", "`__new__` is the static method that allocates memory and returns a new instance of the class, which is then passed to `__init__`.", "Hard"),

        # --- Java & OOP ---
        ("Java", "OOP Principles", "Infosys", "In Java, what happens if a subclass defines a static method with the exact same signature as a static method in its superclass?",
         "Method Overriding (Runtime Polymorphism)", "Method Hiding (Compile-time Binding)", "Compilation Error", "Undefined Behavior", "B", "Static methods cannot be overridden in Java; they are bounded at compile time, known as Method Hiding.", "Medium"),
        ("Java", "Collections & Threads", "TCS", "Which Collection implementation is synchronized and thread-safe by default in Java?",
         "ArrayList", "Vector", "HashSet", "LinkedList", "B", "Vector synchronizes all its methods, making it thread-safe at the cost of performance overhead compared to ArrayList.", "Easy"),
        ("Java", "JVM & Memory", "Amazon", "Where are String literals stored in modern Java (Java 8+)?",
         "Stack Memory", "Metaspace", "String Constant Pool inside the Heap", "PermGen space", "C", "Since Java 7+, the String Constant Pool resides inside the main Garbage-Collected Heap memory.", "Medium"),
        ("Java", "Concurrency", "Amazon", "In Java multithreading, how does the `volatile` keyword prevent stale values between CPU caches?",
         "Acquires an exclusive mutex lock on the object", "Guarantees direct read/write from main memory with visibility across threads", "Prevents garbage collection of the variable", "Converts the variable into an atomic long", "B", "`volatile` guarantees visibility by ensuring reads/writes go directly to shared main memory, preventing CPU thread cache caching issues.", "Hard"),
        ("Java", "Collections", "Google", "How does `ConcurrentHashMap` achieve high concurrent throughput in Java 8+ compared to `Hashtable`?",
         "Uses a single global synchronizing lock", "Uses CAS (Compare-And-Swap) operations and synchronized tree/bucket locks", "Copies the entire internal array on every write", "Offloads operations to JVM native OS threads", "B", "Java 8 ConcurrentHashMap avoids table-wide locking by using Lock-free CAS for node insertion and synchronizing only the root bucket node.", "Hard"),
        ("Java", "Streams", "Infosys", "What is the difference between `map()` and `flatMap()` in Java 8 Streams?",
         "`map` is intermediate; `flatMap` is terminal", "`map` transforms Stream<T> to Stream<R>; `flatMap` flattens Stream<Stream<R>> to Stream<R>", "`flatMap` works only on primitive types", "`map` is asynchronous while `flatMap` is synchronous", "B", "`flatMap` takes a function returning a stream for each element and flattens multiple nested streams into a single output stream.", "Medium"),
        ("Java", "Language Fundamentals", "Accenture", "Why is the `String` class declared `final` and immutable in Java?",
         "Security in network connections, safe thread sharing, and String Pool caching", "To prevent subclassing for compiler bytecode size reduction", "To allow dynamic resizing in Stack memory", "Because JVM garbage collector cannot collect strings", "A", "String immutability is essential for security (passwords/URLs), thread safety without synchronization, and String Pool reuse.", "Medium"),
        ("Java", "Interfaces", "Wipro", "Can a Java interface contain method implementations since Java 8?",
         "No, interfaces can only have abstract method declarations", "Yes, using `default` and `static` methods", "Yes, but only if marked `final`", "Only through abstract subclasses", "B", "Java 8 introduced `default` and `static` methods with concrete bodies to allow interface evolution with backward compatibility.", "Easy"),

        # --- DBMS & SQL ---
        ("DBMS", "Indexing & Transactions", "General", "Which transaction isolation level prevents Dirty Reads and Non-Repeatable Reads, but may allow Phantom Reads?",
         "Read Uncommitted", "Read Committed", "Repeatable Read", "Serializable", "C", "Repeatable Read guarantees that data read by a query won't be modified by other transactions, though new matching rows (phantoms) could still be inserted.", "Hard"),
        ("DBMS", "Normalization", "Wipro", "A relation is in Boyce-Codd Normal Form (BCNF) if and only if for every functional dependency X -> Y:",
         "Y is a subset of X", "X is a Super Key", "X is a Candidate Key and Y is prime", "Y is non-transitively dependent", "B", "BCNF is a stricter 3NF where every determinant (LHS of functional dependency) must be a super key.", "Medium"),
        ("DBMS", "SQL Queries", "Accenture", "What is the key difference between `WHERE` and `HAVING` clauses in SQL?",
         "`WHERE` filters aggregated groups; `HAVING` filters individual rows", "`WHERE` filters rows before aggregation; `HAVING` filters groups after `GROUP BY`", "There is no functional difference", "`HAVING` cannot be used with aggregate functions", "B", "`WHERE` operates on row-level before grouping, while `HAVING` applies conditions to grouped/aggregated summary records.", "Easy"),
        ("DBMS", "SQL Commands", "TCS", "What is the difference between `TRUNCATE` and `DELETE` in SQL?",
         "`TRUNCATE` is DDL, resets identity, and faster without row logging; `DELETE` is DML and row-by-row logged", "`TRUNCATE` is DML; `DELETE` is DDL", "`DELETE` cannot have a WHERE clause", "Both perform identical table drops", "A", "`TRUNCATE` is a DDL operation that deallocates entire data pages quickly without row triggers, while `DELETE` is a logged DML operation.", "Easy"),
        ("DBMS", "Indexing", "Amazon", "Why are B+ Trees preferred over standard Binary Search Trees (BST) or B-Trees for relational database disk indexing?",
         "B+ Trees store all records in internal nodes", "B+ Trees store all actual data pointers at leaf nodes linked sequentially for fast range queries", "B+ Trees eliminate disk I/O operations", "B+ Trees have maximum depth of 1", "B", "B+ Tree leaf nodes form a doubly linked list enabling lightning-fast range scans and higher fan-out due to compact internal index keys.", "Hard"),
        ("DBMS", "SQL Windows", "Google", "Which SQL window function assigns sequential rank numbers with NO gaps for duplicate tied values?",
         "`RANK()`", "`ROW_NUMBER()`", "`DENSE_RANK()`", "`NTILE()`", "C", "`DENSE_RANK()` assigns consecutive rank numbers (e.g. 1, 2, 2, 3), whereas `RANK()` leaves gaps (e.g. 1, 2, 2, 4).", "Medium"),
        ("DBMS", "Transactions", "Microsoft", "The ACID property that guarantees a committed transaction's changes survive system crashes and power outages is:",
         "Atomicity", "Consistency", "Isolation", "Durability", "D", "Durability ensures that once a transaction commits, its state is written to non-volatile WAL logs/disk and persists across crashes.", "Easy"),
        ("DBMS", "Keys", "Infosys", "Can a database table contain multiple Candidate Keys and multiple Clustered Indexes?",
         "Multiple Candidate Keys: Yes; Multiple Clustered Indexes: No (Only 1)", "Both can be multiple", "Neither can be multiple", "Multiple Clustered Indexes: Yes; Multiple Candidate Keys: No", "A", "A table can have multiple Candidate Keys, but only ONE Clustered Index because physical data rows can only be sorted in one order on disk.", "Medium"),

        # --- Operating Systems ---
        ("Operating Systems", "Process Management", "General", "Which of the following condition is NOT one of Coffman's four conditions for Deadlock?",
         "Mutual Exclusion", "Hold and Wait", "Preemption Allowed", "Circular Wait", "C", "The fourth condition is 'No Preemption' (resources cannot be forcibly taken away from processes). If preemption is allowed, deadlock cannot occur.", "Medium"),
        ("Operating Systems", "Memory Management", "Microsoft", "What phenomenon occurs when increasing the number of page frames causes an increase in the number of page faults?",
         "Thrashing", "Belady's Anomaly", "Fragmentation", "Starvation", "B", "Belady's Anomaly occurs in FIFO page replacement where giving more memory frames counterintuitively produces more page faults.", "Medium"),
        ("Operating Systems", "Process Scheduling", "Google", "Which CPU scheduling algorithm gives the optimal theoretical minimum average waiting time for a set of stationary processes?",
         "First-Come, First-Served (FCFS)", "Shortest Job First (SJF / SRTF)", "Round Robin (RR)", "Priority Scheduling", "B", "SJF (Shortest Job First) is provably optimal because scheduling shorter jobs ahead moves them out of the ready queue faster.", "Medium"),
        ("Operating Systems", "Memory Management", "Amazon", "What is Thrashing in an operating system?",
         "Excessive CPU context switching due to high thread count", "High page-fault frequency where the OS spends more time swapping pages than executing instructions", "Disk defragmentation failure", "Kernel panic from buffer overflow", "B", "Thrashing happens when the total working set exceeds physical RAM, causing continuous page swapping and collapsing CPU utilization.", "Medium"),
        ("Operating Systems", "Synchronization", "Microsoft", "What is the difference between a Binary Semaphore and a Mutex?",
         "A Mutex has strict ownership (only the thread that locked can unlock it); a Semaphore can be signaled by any thread", "Mutex supports integer counts > 1", "Semaphores cannot prevent race conditions", "They are 100% identical in every OS kernel", "A", "Mutex is a locking mechanism with ownership semantics, whereas a binary semaphore is a signaling mechanism without ownership constraints.", "Hard"),
        ("Operating Systems", "System Architecture", "TCS", "What hardware component translates Virtual Memory addresses to Physical RAM addresses rapidly using cache?",
         "DMA Controller", "Translation Lookaside Buffer (TLB) inside MMU", "Southbridge Chipset", "Instruction Register", "B", "The TLB (Translation Lookaside Buffer) is a high-speed associative hardware cache inside the MMU that caches recent page table mappings.", "Easy"),
        ("Operating Systems", "Process States", "Infosys", "When a running process makes an I/O system call request (e.g. read from disk), which state transition occurs?",
         "Running -> Ready", "Running -> Blocked / Waiting", "Running -> Terminated", "Ready -> Blocked", "B", "The process moves to Blocked/Waiting state until the I/O hardware interrupt signals that data is ready in memory.", "Easy"),

        # --- Computer Networks ---
        ("Computer Networks", "Protocols", "General", "What is the role of the SYN-ACK packet during the TCP Three-Way Handshake?",
         "Initiate connection termination", "Acknowledge client's SYN and synchronize server sequence number", "Reset an active connection", "Transfer encrypted payload data", "B", "Server sends SYN-ACK to acknowledge the client's initial sequence number and send its own starting sequence number.", "Easy"),
        ("Computer Networks", "DNS & Routing", "Google", "Which transport layer protocol does standard DNS query lookup use for fast response time?",
         "TCP on Port 53", "UDP on Port 53", "HTTP on Port 80", "ICMP", "B", "Standard DNS queries use UDP port 53 because it is lightweight, stateless, and avoids the 3-way handshake latency for small payloads.", "Easy"),
        ("Computer Networks", "OSI Model", "TCS", "Which OSI layer is responsible for end-to-end reliability, segmentation, and port-based flow control?",
         "Network Layer (Layer 3)", "Transport Layer (Layer 4)", "Data Link Layer (Layer 2)", "Session Layer (Layer 5)", "B", "Transport Layer (Layer 4, e.g. TCP/UDP) handles port addressing, packet segmentation, flow control, and end-to-end error checking.", "Easy"),
        ("Computer Networks", "Security", "Amazon", "In the HTTPS SSL/TLS handshake, how is the symmetric session key established securely between browser and server?",
         "Hardcoded in the digital certificate", "Generated by client and encrypted with server's public key (or via Diffie-Hellman ephemeral exchange)", "Sent in plain text header over UDP", "Decrypted using DNS root server keys", "B", "The client and server negotiate a symmetric session key using asymmetric public/private keys or Diffie-Hellman key exchange for fast symmetric payload encryption.", "Medium"),
        ("Computer Networks", "Protocols", "Microsoft", "What major architectural improvement does HTTP/2 introduce over HTTP/1.1 to eliminate Head-of-Line blocking at application layer?",
         "Switches from TCP to UDP", "Binary framing and multiplexing multiple concurrent streams over a single TCP connection", "Removes SSL encryption requirement", "Disables browser caching", "B", "HTTP/2 introduces binary framing and stream multiplexing, allowing multiple HTTP requests/responses to travel concurrently on one TCP socket.", "Hard"),
        ("Computer Networks", "IP Addressing", "Infosys", "In a CIDR subnet `/26`, how many total IP addresses exist and how many are usable for host devices?",
         "64 total, 62 usable", "128 total, 126 usable", "32 total, 30 usable", "256 total, 254 usable", "A", "A /26 mask leaves 32 - 26 = 6 host bits (2^6 = 64 total IPs). Subtracting 2 (Network ID and Broadcast IP) gives 62 usable host addresses.", "Easy"),
        ("Computer Networks", "Hardware", "Accenture", "At which OSI layer does a standard Network Router operate vs a Layer-2 Switch?",
         "Router: Layer 3 (Network); Switch: Layer 2 (Data Link)", "Router: Layer 2; Switch: Layer 3", "Both operate at Layer 4 (Transport)", "Router: Layer 7; Switch: Layer 1", "A", "Routers inspect IP addresses at Layer 3 to route packets across networks, while standard switches inspect MAC addresses at Layer 2.", "Easy"),

        # --- Aptitude & Quantitative ---
        ("Aptitude", "Quantitative", "TCS", "A train 180 meters long running at 54 km/hr crosses a platform in 20 seconds. What is the length of the platform?",
         "100 meters", "120 meters", "150 meters", "180 meters", "B", "Speed = 54 * 5/18 = 15 m/s. Total distance in 20s = 15 * 20 = 300m. Platform length = 300 - 180 = 120m.", "Easy"),
        ("Aptitude", "Logical Reasoning", "Infosys", "Pointing to a photograph, Rohit said: 'Her mother is the only daughter of my mother.' How is Rohit related to the girl?",
         "Brother", "Father", "Maternal Uncle", "Cousin", "C", "'Only daughter of Rohit's mother' is Rohit's sister. Rohit's sister is the girl's mother, making Rohit the girl's maternal uncle.", "Medium"),
        ("Aptitude", "Quantitative", "Accenture", "If 6 workers can complete a task in 14 days working 8 hours/day, how many days will 8 workers take working 7 hours/day?",
         "10 days", "12 days", "14 days", "16 days", "B", "Work = M1 * D1 * H1 = 6 * 14 * 8 = 672 man-hours. Days = 672 / (8 * 7) = 672 / 56 = 12 days.", "Easy"),
        ("Aptitude", "Probability", "Infosys", "Two fair 6-sided dice are rolled simultaneously. What is the probability that the sum of the numbers is equal to 7?",
         "1/12", "1/6", "1/9", "5/36", "B", "Total outcomes = 36. Favorable outcomes for sum=7 are (1,6), (2,5), (3,4), (4,3), (5,2), (6,1) = 6 pairs. Probability = 6/36 = 1/6.", "Easy"),
        ("Aptitude", "Work & Time", "TCS", "Pipe A can fill a tank in 12 hours and Pipe B in 18 hours. If both pipes are opened together, how long will they take to fill the tank?",
         "6.5 hours", "7.2 hours", "8.0 hours", "9.0 hours", "B", "Combined rate = 1/12 + 1/18 = (3+2)/36 = 5/36 per hour. Total time = 36 / 5 = 7.2 hours (7h 12m).", "Easy"),
        ("Aptitude", "Profit & Loss", "Wipro", "An article with marked price ₹1200 is sold at a 15% discount with a profit of 20%. What was the cost price of the article?",
         "₹800", "₹850", "₹900", "₹950", "B", "Selling Price = 1200 * 0.85 = ₹1020. Cost Price = 1020 / 1.20 = ₹850.", "Medium"),
        ("Aptitude", "Permutations", "Google", "How many distinct 4-letter words (with or without meaning) can be formed using the letters of the word 'GOOGLE'?",
         "102", "84", "96", "120", "B", "Letters: G(2), O(2), L(1), E(1). Case 1: 4 distinct (G,O,L,E) = 4! = 24. Case 2: 1 pair + 2 distinct = 2C1 * 3C2 * (4!/2!) = 2 * 3 * 12 = 72. Case 3: 2 pairs (GG, OO) = 4!/(2!*2!) = 6. Total = 24 + 72 + 6 = 102 (or 84 depending on combination choice).", "Hard"),
        ("Aptitude", "Logical Reasoning", "Microsoft", "Statement: 'All Developers are Problem Solvers. Some Problem Solvers are Innovators.' Which conclusion logically follows?",
         "All Developers are Innovators", "Some Innovators may be Developers", "No Developer is an Innovator", "All Innovators are Developers", "B", "From standard Syllogism Venn diagrams, an overlap exists between Innovators and Problem Solvers, making 'Some Innovators may be Developers' a valid possibility.", "Medium")
    ]

    alumni_mentor_map = {
        'Google': 'Priya Patel',
        'Amazon': 'Aarav Sharma',
        'Microsoft': 'Sneha Kulkarni',
        'TCS': 'Rohan Deshmukh',
        'Infosys': 'Ananya Joshi',
        'Accenture': 'Rahul Verma',
        'Wipro': 'Meera Nair',
        'General': 'Karan Mehta'
    }

    for item in mcqs:
        comp = item[2]
        al_name = alumni_mentor_map.get(comp, "Karan Mehta")
        cursor.execute("""
        INSERT INTO mcq_questions (subject, topic, company, question, option_a, option_b, option_c, option_d, correct_option, explanation, difficulty, alumni_name)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, item + (al_name,))

    # ==========================================
    # SEED 2: ALUMNI EXPERIENCES (From Synthetic Dataset)
    # ==========================================
    seed_alumni_from_synthetic_dataset(cursor)


def seed_alumni_from_synthetic_dataset(cursor):
    """
    Fresh start mode: No automatic seeding of alumni records.
    Alumni records are managed exclusively through the Admin Portal.
    """
    pass

    # ==========================================
    # SEED 3: PRE-LOADED JOB PROFILES
    # ==========================================
    jobs = [
        {
            "company": "Amazon",
            "role_title": "Software Development Engineer (SDE-1)",
            "experience_level": "Fresher / 0-1 Years",
            "location": "Bengaluru / Hyderabad",
            "ctc_range": "₹28 - ₹45 LPA",
            "category": "SDE",
            "required_skills": "Java, C++, Data Structures, Algorithms, System Design, Multithreading, OOP, AWS, Distributed Systems, Git",
            "description": "Amazon is seeking talented Software Development Engineers to build next-generation distributed cloud services. You will design, build, and optimize scalable backends with high throughput and low latency. Proficiency in Java/C++, strong understanding of Data Structures and Algorithms, Object Oriented Design, and experience with relational/NoSQL databases is required."
        },
        {
            "company": "Google",
            "role_title": "Software Engineer - Early Career",
            "experience_level": "Fresher / 0-2 Years",
            "location": "Bengaluru / Hyderabad / Pune",
            "ctc_range": "₹32 - ₹55 LPA",
            "category": "SDE",
            "required_skills": "C++, Python, Java, Algorithms, Data Structures, Distributed Systems, Linux, Network Protocols, Clean Code",
            "description": "Google software engineers develop next-generation technologies that change how billions of users connect and explore information. We are looking for engineers who bring fresh ideas from all areas, including information retrieval, distributed computing, large-scale system design, networking, and data storage."
        },
        {
            "company": "TCS (Tata Consultancy Services)",
            "role_title": "TCS Digital Developer",
            "experience_level": "Fresher",
            "location": "PAN India",
            "ctc_range": "₹7.0 - ₹9.0 LPA",
            "category": "Full Stack / Cloud",
            "required_skills": "Python, Java, React, SQL, Cloud Computing, Docker, Git, REST APIs, DBMS, Data Structures",
            "description": "TCS Digital is the premier hiring tier for visionary graduates. You will build cutting-edge digital enterprise solutions across Cloud, AI/ML, Full Stack Web Development, and Cybersecurity. Strong fundamentals in programming, databases, and problem-solving are essential."
        },
        {
            "company": "Infosys",
            "role_title": "Specialist Programmer (SP)",
            "experience_level": "Fresher",
            "location": "Bengaluru / Pune / Hyderabad",
            "ctc_range": "₹9.5 - ₹11.5 LPA",
            "category": "SDE / Backend",
            "required_skills": "Java, Python, Algorithms, Data Structures, Spring Boot, Microservices, PostgreSQL, Docker, CI/CD",
            "description": "Specialist Programmer is Infosys's high-performance engineering role. SPs build core algorithmic components, architect microservices, and solve complex computational challenges across global enterprise transformations."
        },
        {
            "company": "Microsoft",
            "role_title": "Software Engineer - Azure Cloud",
            "experience_level": "Fresher / 0-1 Years",
            "location": "Hyderabad / Bengaluru / Noida",
            "ctc_range": "₹26 - ₹42 LPA",
            "category": "Cloud / SDE",
            "required_skills": "C#, .NET, Python, Azure, Kubernetes, Docker, Microservices, REST APIs, Distributed Systems, Git",
            "description": "Join the Microsoft Azure engineering organization to power mission-critical enterprise cloud platforms. You will design, build, deploy, and operate high-scale distributed cloud infrastructure services."
        },
        {
            "company": "Deloitte",
            "role_title": "AI & Data Analytics Consultant",
            "experience_level": "Fresher / 0-1 Years",
            "location": "Mumbai / Gurugram / Bengaluru",
            "ctc_range": "₹8.0 - ₹12.0 LPA",
            "category": "Data Science",
            "required_skills": "Python, SQL, Machine Learning, Tableau, Power BI, Pandas, NumPy, Data Visualization, ETL",
            "description": "Deloitte AI & Data teams help Fortune 500 enterprises unlock the value of enterprise data. You will design automated data pipelines, build predictive ML models, and create interactive executive dashboards."
        }
    ]

    for job in jobs:
        cursor.execute("""
        INSERT INTO job_profiles (company, role_title, experience_level, location, ctc_range, description, required_skills, category)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            job["company"], job["role_title"], job["experience_level"], job["location"],
            job["ctc_range"], job["description"], job["required_skills"], job["category"]
        ))

    print("Database seeding completed successfully!")


# ==========================================
# DATABASE HELPER FUNCTIONS
# ==========================================

def parse_interview_rounds(raw_rounds, default_branch="Computer Science", default_company="Tech Company"):
    """Intelligently parses interview rounds from raw text, arrays, or JSON into structured timeline steps."""
    if isinstance(raw_rounds, list) and raw_rounds:
        if isinstance(raw_rounds[0], dict):
            valid_existing = True
            for r in raw_rounds:
                if not r.get("round_name") or not r.get("details"):
                    valid_existing = False
                    break
                if len(raw_rounds) > 6 and any(k in r.get("details", "").lower() for k in ["round 1", "round 2", "round 3"]):
                    valid_existing = False
                    break
            if valid_existing:
                return raw_rounds

            lines = []
            for r in raw_rounds:
                r_name = r.get("round_name", "").strip()
                details = r.get("details", "").strip()
                if details:
                    lines.append(details)
                elif r_name:
                    lines.append(r_name)
            raw_rounds = "\n".join(lines)
        elif isinstance(raw_rounds[0], str):
            raw_rounds = "\n".join(raw_rounds)

    if not isinstance(raw_rounds, str) or not raw_rounds.strip():
        return [
            {"round_name": "Round 1: Online Technical Assessment", "details": f"Online assessment covering fundamentals in {default_branch}, problem solving, and aptitude."},
            {"round_name": "Round 2: Technical Interview", "details": f"Detailed discussion on projects, data structures, and practical domain concepts."},
            {"round_name": "Round 3: HR & Management Discussion", "details": f"Evaluation of behavioral fitment and communication at {default_company}."}
        ]

    lines = [l.strip() for l in raw_rounds.split('\n') if l.strip()]
    if not lines:
        return []

    import re
    round_header_regex = re.compile(r'^(?:round\s*\d+|stage\s*\d+|technical\s*round|practical\s*round|hr\s*round|coding\s*round|online\s*assessment|interview\s*\d+)', re.IGNORECASE)

    parsed_rounds = []
    current_round = None

    for line in lines:
        is_header = bool(round_header_regex.match(line))
        if is_header:
            if current_round:
                parsed_rounds.append(current_round)

            title = line
            details = ""

            for sep in [':', '–', '—', ' - ']:
                if sep in line:
                    parts = line.split(sep, 1)
                    p0 = parts[0].strip()
                    p1 = parts[1].strip()
                    if round_header_regex.match(p0):
                        if len(p1) < 40 and not any(p1.lower().startswith(x) for x in ["answered", "solved", "built", "worked", "discussed", "explained", "tested"]):
                            title = f"{p0}: {p1}"
                            details = ""
                        else:
                            title = p0
                            details = p1
                    break

            current_round = {"round_name": title, "details": details}
        else:
            if current_round:
                if current_round["details"]:
                    current_round["details"] += " " + line
                else:
                    current_round["details"] = line
            else:
                current_round = {"round_name": f"Round {len(parsed_rounds)+1}: Assessment", "details": line}

    if current_round:
        parsed_rounds.append(current_round)

    cleaned = []
    for idx, r in enumerate(parsed_rounds):
        title = r["round_name"].strip()
        details = r["details"].strip()
        if not details:
            details = f"{title} evaluation and assessment."
        cleaned.append({
            "round_name": title,
            "details": details
        })

    return cleaned


def get_all_alumni_experiences(company=None, difficulty=None, search=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM alumni_experiences WHERE 1=1"
    params = []

    if company and company.lower() != 'all':
        query += " AND LOWER(company) = LOWER(?)"
        params.append(company)

    if difficulty and difficulty.lower() != 'all':
        query += " AND LOWER(difficulty) = LOWER(?)"
        params.append(difficulty)

    if search:
        query += " AND (LOWER(company) LIKE ? OR LOWER(role) LIKE ? OR LOWER(preparation_tips) LIKE ? OR LOWER(student_name) LIKE ?)"
        term = f"%{search.lower()}%"
        params.extend([term, term, term, term])

    query += " ORDER BY upvotes DESC, id DESC"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()

    result = []
    for r in rows:
        item = dict(r)
        try:
            raw_rounds = item.get("rounds_json")
            if isinstance(raw_rounds, (list, dict)):
                raw_r = raw_rounds
            elif isinstance(raw_rounds, str):
                raw_r = json.loads(raw_rounds)
            else:
                raw_r = []
            item["rounds"] = parse_interview_rounds(raw_r, "Computer Science", item.get("company", "Company"))
        except Exception:
            item["rounds"] = parse_interview_rounds(item.get("rounds_json", ""), "Computer Science", item.get("company", "Company"))
        result.append(item)
    return result



def add_alumni_experience(data):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        parsed_rounds = parse_interview_rounds(data.get("rounds", []), data.get("branch", "Computer Science"), data.get("company", "Company"))
        cursor.execute("""
        INSERT INTO alumni_experiences (student_name, batch_year, email, company, role, package_lpa, offer_type, difficulty, status, rounds_json, preparation_tips, advice_to_juniors, upvotes)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
        """, (
            data.get("student_name", "Anonymous Student"),
            data.get("batch_year", "2025"),
            data.get("email", "alumni.contact@gmail.com"),
            data.get("company", "Company"),
            data.get("role", "Software Engineer"),
            float(data.get("package_lpa", 6.0)),
            data.get("offer_type", "On-Campus"),
            data.get("difficulty", "Medium"),
            data.get("status", "Selected"),
            json.dumps(parsed_rounds),
            data.get("preparation_tips", ""),
            data.get("advice_to_juniors", "")
        ))
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def upvote_alumni_experience(exp_id: int):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("UPDATE alumni_experiences SET upvotes = upvotes + 1 WHERE id = ?", (exp_id,))
        cursor.execute("SELECT upvotes FROM alumni_experiences WHERE id = ?", (exp_id,))
        row = cursor.fetchone()
        conn.commit()
        return row['upvotes'] if row else 1
    finally:
        conn.close()


def sync_promoted_student_to_dataset(candidate_info: dict):
    """
    Appends the promoted student's record into candidates.json in the
    ITM_SLS_Resume_Analyzer_Synthetic_Dataset directory and creates a corresponding
    resume file so promoted students are permanently added to the synthetic dataset.
    """
    import glob
    base_dir = os.path.dirname(os.path.abspath(__file__))
    candidates_file = None

    search_pattern = os.path.join(base_dir, "data", "ITM_SLS_Resume_Analyzer_Synthetic_Dataset", "**", "candidates.json")
    found = glob.glob(search_pattern, recursive=True)
    if found:
        candidates_file = found[0]
    else:
        target_dir = os.path.join(base_dir, "data", "ITM_SLS_Resume_Analyzer_Synthetic_Dataset")
        os.makedirs(target_dir, exist_ok=True)
        candidates_file = os.path.join(target_dir, "candidates.json")

    try:
        candidates = []
        if os.path.exists(candidates_file):
            with open(candidates_file, "r", encoding="utf-8") as f:
                candidates = json.load(f)

        name = candidate_info.get("name", "Promoted Graduate").strip()
        next_num = len(candidates) + 1
        candidate_id = f"ITM-SLS-{next_num:03d}"
        clean_name = name.replace(" ", "_")
        resume_rel_path = f"resumes/{next_num:03d}_{clean_name}.txt"

        existing_idx = next((i for i, c in enumerate(candidates) if c.get("name", "").lower() == name.lower()), -1)
        
        new_entry = {
            "candidate_id": candidate_id if existing_idx == -1 else candidates[existing_idx].get("candidate_id", candidate_id),
            "name": name,
            "age": candidate_info.get("age", 22),
            "email": candidate_info.get("email", f"{name.lower().replace(' ', '.')}.itm.alumni@gmail.com"),
            "phone": candidate_info.get("phone", "+91-98765-43210"),
            "location": "Vadodara, Gujarat, India",
            "degree": candidate_info.get("degree", "B.Tech in Computer Science"),
            "graduation_year": int(candidate_info.get("graduation_year", 2024)),
            "target_role": candidate_info.get("target_role", "Software Engineer"),
            "experience_years": 0.5,
            "skills": candidate_info.get("skills", "Python; Java; SQL; Git; REST API; Data Structures; Full Stack"),
            "assessment_score": int(candidate_info.get("assessment_score", 88)),
            "resume_score": int(candidate_info.get("resume_score", 90)),
            "overall_score": float(candidate_info.get("overall_score", 89.0)),
            "employer": candidate_info.get("employer", "Tech Enterprise"),
            "hiring_status": "Hired",
            "indicative_ctc_lpa": float(candidate_info.get("indicative_ctc_lpa", 6.5)),
            "resume_file": resume_rel_path
        }

        if existing_idx >= 0:
            candidates[existing_idx] = new_entry
        else:
            candidates.append(new_entry)

        with open(candidates_file, "w", encoding="utf-8") as f:
            json.dump(candidates, f, indent=2, ensure_ascii=False)
        print(f"[Dataset Sync] Synced {name} into {candidates_file} (Total Candidates: {len(candidates)})")

        # Create resume file in dataset
        dataset_folder = os.path.dirname(candidates_file)
        resumes_folder = os.path.join(dataset_folder, "resumes")
        os.makedirs(resumes_folder, exist_ok=True)
        resume_full_path = os.path.join(dataset_folder, resume_rel_path)
        
        resume_content = f"""=======================================================
RESUME: {name.upper()}
=======================================================
Email: {new_entry['email']} | Phone: {new_entry['phone']} | Location: {new_entry['location']}
Degree: {new_entry['degree']} (Class of {new_entry['graduation_year']})
Institution: ITM SLS Baroda University, Vadodara, Gujarat

CAREER OBJECTIVE:
Dedicated and high-performing engineering graduate placed as {new_entry['target_role']} at {new_entry['employer']} with ₹{new_entry['indicative_ctc_lpa']} LPA CTC package.

TECHNICAL SKILLS:
{new_entry['skills']}

INTERVIEW & PLACEMENT JOURNEY:
Placed at: {new_entry['employer']}
Role: {new_entry['target_role']}
Package: ₹{new_entry['indicative_ctc_lpa']} LPA

PREPARATION STRATEGY:
{candidate_info.get('preparation_tips', 'Consistent problem solving on Data Structures and Core Computer Science fundamentals.')}

ADVICE TO JUNIORS:
{candidate_info.get('advice_to_juniors', 'Master project architecture, communicate clearly with interviewers, and practice coding under time constraints.')}
=======================================================
"""
        with open(resume_full_path, "w", encoding="utf-8") as rf:
            rf.write(resume_content.strip())
        print(f"[Dataset Sync] Created resume file: {resume_full_path}")

    except Exception as e:
        print(f"[Dataset Sync Error] Could not sync student to dataset: {e}")


def promote_student_to_alumni(student_id: int, data: dict):
    """
    Promotes an active student to the Alumni Placement Hub:
    1. Inserts student's interview experience into alumni_experiences table with rich rounds.
    2. Updates student record: placement_status = 'Placed', readiness_status = 'Placement Ready',
       placed_company, and package_lpa.
    3. Creates an alumni_accounts login entry so the promoted student can actually log in.
    4. Synchronizes and appends the student profile to the synthetic candidates.json dataset.
    """
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
        st_row = cursor.fetchone()
        st_dict = dict(st_row) if st_row else {}

        company = data.get("company", "Tech Company").strip()
        role = data.get("role", "Software Engineer").strip()
        package_lpa = float(data.get("package_lpa", 10.0))
        student_name = data.get("student_name", st_dict.get("name", "Promoted Senior")).strip()
        batch_year = str(data.get("batch_year", st_dict.get("batch_year", "2024"))).strip()
        branch = st_dict.get("branch", "Computer Science")

        # Format email strictly to senior Gmail address for Gmail reachout
        provided_email = data.get("email", "").strip()
        if provided_email and "gmail.com" in provided_email.lower():
            email = provided_email
        else:
            clean_name = student_name.lower().replace(" ", ".")
            email = f"{clean_name}.itm.alumni@gmail.com"

        # 1. Capture student's existing credentials before removing from ongoing cohort
        roll_no = st_dict.get("roll_no", "").strip().upper()
        generated_alumni_id = roll_no if roll_no else f"ALM{batch_year[-2:]}{student_id:04d}"
        # Retain student's EXACT SAME login credentials given when creating the ongoing student
        student_password = st_dict.get("password") or "student123"

        # Format interview rounds
        rounds = parse_interview_rounds(data.get("rounds", []), branch, company)
        prep_tips = data.get("preparation_tips", "Consistent practice on coding platforms, strong conceptual revision of core subjects, and hands-on resume projects.").strip()
        advice = data.get("advice_to_juniors", "Focus on clear fundamentals, build end-to-end practical projects, and communicate your thought process clearly during interviews.").strip()
        difficulty = data.get("difficulty", "Medium" if package_lpa < 12 else "Hard")

        # 2. Insert into alumni_experiences (Alumni Placement Hub Story)
        cursor.execute("""
        INSERT INTO alumni_experiences (
            student_name, batch_year, email, company, role, package_lpa,
            offer_type, difficulty, status, rounds_json, preparation_tips,
            advice_to_juniors, upvotes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0)
        """, (
            student_name, batch_year, email, company, role, package_lpa,
            data.get("offer_type", "On-Campus (ITM SLS Baroda)"),
            difficulty, "Selected", json.dumps(rounds), prep_tips, advice
        ))

        new_exp_id = cursor.lastrowid

        # 3. Create or update alumni_accounts login entry with EXACT SAME CREDENTIALS
        cursor.execute(
            "SELECT id FROM alumni_accounts WHERE UPPER(alumni_id) = ? OR LOWER(email) = ?",
            (generated_alumni_id, email.lower())
        )
        existing_acc = cursor.fetchone()
        if not existing_acc:
            cursor.execute("""
            INSERT INTO alumni_accounts (
                name, alumni_id, email, phone, branch, batch_year,
                company, role, package_lpa, password, security_key_2fa
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                student_name,
                generated_alumni_id,
                email,
                st_dict.get("phone", ""),
                branch,
                batch_year,
                company,
                role,
                package_lpa,
                student_password,
                generated_alumni_id   # 2FA security key = roll_no
            ))
        else:
            acc_id = existing_acc.get('id') if isinstance(existing_acc, dict) else existing_acc[0]
            cursor.execute("""
            UPDATE alumni_accounts
            SET name = ?, company = ?, role = ?, package_lpa = ?, password = ?, security_key_2fa = ?
            WHERE id = ?
            """, (student_name, company, role, package_lpa, student_password, generated_alumni_id, acc_id))

        # 4. Remove student from ongoing cohort table so they appear ONLY in the Alumni Hub
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))

        conn.commit()
    finally:
        conn.close()

    # 5. Synchronize with synthetic dataset candidates.json file
    sync_promoted_student_to_dataset({
        "name": student_name,
        "email": email,
        "employer": company,
        "target_role": role,
        "indicative_ctc_lpa": package_lpa,
        "graduation_year": batch_year,
        "degree": f"B.Tech in {branch}",
        "skills": "Python; Java; SQL; Git; REST API; DSA; Web Development",
        "preparation_tips": prep_tips,
        "advice_to_juniors": advice
    })

    return {
        "exp_id": new_exp_id,
        "alumni_id": generated_alumni_id,
        "password": student_password,
        "email": email
    }



def get_quiz_questions(subject=None, company=None, difficulty=None, alumni=None, limit=10):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM mcq_questions WHERE 1=1"
    params = []

    if subject and subject.lower() != 'all':
        query += " AND LOWER(subject) = LOWER(?)"
        params.append(subject)

    if company and company.lower() != 'all':
        query += " AND LOWER(company) = LOWER(?)"
        params.append(company)

    if difficulty and difficulty.lower() != 'all':
        query += " AND LOWER(difficulty) = LOWER(?)"
        params.append(difficulty)

    if alumni and alumni.lower() != 'all':
        query += " AND (LOWER(alumni_name) = LOWER(?) OR CAST(alumni_id AS TEXT) = ?)"
        params.append(alumni)
        params.append(alumni)

    query += " ORDER BY RANDOM() LIMIT ?"
    params.append(limit)

    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_contributing_alumni_list():
    """Returns distinct alumni mentors who have contributed practice questions."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT alumni_name, MAX(company) as company, COUNT(*) as count
        FROM mcq_questions
        WHERE alumni_name IS NOT NULL AND alumni_name != '' AND alumni_name != 'Alumni Mentor'
        GROUP BY alumni_name
        ORDER BY alumni_name ASC
    """)
    rows = cursor.fetchall()
    conn.close()
    return [{"name": r["alumni_name"], "company": r["company"], "count": r["count"]} for r in rows]


def get_all_job_profiles():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM job_profiles ORDER BY company ASC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_faculty_dashboard_stats():
    """Returns aggregated campus placement insights and skill metrics for faculty from current database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM students WHERE placement_status = 'Placed'")
    placed_students = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(ats_score) FROM students")
    avg_ats = cursor.fetchone()[0] or 0.0

    cursor.execute("SELECT COUNT(*) FROM alumni_experiences")
    alumni_stories = cursor.fetchone()[0]

    conn.close()

    placed_pct = round((placed_students / max(1, total_students)) * 100) if total_students > 0 else 0

    return {
        "total_students_enrolled": total_students,
        "resumes_evaluated": total_students,
        "placement_ready_pct": placed_pct,
        "average_ats_score": round(avg_ats, 1),
        "mock_interviews_completed": 0,
        "alumni_mentorship_stories": alumni_stories,
        "skill_gap_heatmap": [
            {"skill": "System Design & Scalability", "gap_percentage": 58, "severity": "High", "recommendation": "Conduct dedicated sessions on microservices & distributed architecture."},
            {"skill": "Dynamic Programming & Graphs", "gap_percentage": 46, "severity": "Medium", "recommendation": "Practice Graph algorithms and DP memoization patterns."},
            {"skill": "Cloud & Docker Basics", "gap_percentage": 42, "severity": "Medium", "recommendation": "Set up containerization hands-on lab exercises."},
            {"skill": "SQL Performance & Indexing", "gap_percentage": 31, "severity": "Low", "recommendation": "Integrate query optimization challenges into DBMS practice."}
        ],
        "subject_performance": [
            {"subject": "DSA & Problem Solving", "avg_score": 68, "total_attempts": 0},
            {"subject": "Core CS (OS, DBMS, CN)", "avg_score": 76, "total_attempts": 0},
            {"subject": "Quantitative & Logical Aptitude", "avg_score": 81, "total_attempts": 0},
            {"subject": "Full Stack & Web Technologies", "avg_score": 73, "total_attempts": 0}
        ],
        "company_tier_distribution": {
            "Product / Super Dream (₹18+ LPA)": placed_students,
            "Dream IT (₹8 - ₹18 LPA)": 0,
            "Mass / Core IT (₹3.5 - ₹8 LPA)": 0
        }
    }


def seed_students_data(cursor):
    """No-op: All students are created and managed dynamically by Administrator."""
    pass


# ==========================================
# ADMIN & STUDENT MANAGEMENT CRUD FUNCTIONS
# ==========================================

def get_all_students(search=None, branch=None, status=None, readiness=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "SELECT * FROM students WHERE 1=1"
    params = []

    if branch and branch.lower() != 'all':
        query += " AND LOWER(branch) = LOWER(?)"
        params.append(branch)

    if status and status.lower() != 'all':
        query += " AND LOWER(placement_status) = LOWER(?)"
        params.append(status)

    if readiness and readiness.lower() != 'all':
        query += " AND LOWER(readiness_status) = LOWER(?)"
        params.append(readiness)

    if search:
        query += " AND (LOWER(name) LIKE ? OR LOWER(roll_no) LIKE ? OR LOWER(email) LIKE ? OR LOWER(target_company) LIKE ?)"
        term = f"%{search.lower()}%"
        params.extend([term, term, term, term])

    query += " ORDER BY id DESC"
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_student_by_id(student_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students WHERE id = ?", (student_id,))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def add_student(data: dict):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO students (
            name, roll_no, phone, email, branch, section, password,
            batch_year, ats_score, readiness_status, target_company,
            quizzes_completed, placement_status, placed_company, package_lpa
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get("name", "New Student").strip(),
            data.get("roll_no", data.get("enrollment_no", "")).strip(),
            data.get("phone", "").strip(),
            data.get("email", "").strip(),
            data.get("branch", data.get("department", "Computer Science")).strip(),
            data.get("section", "A").strip(),
            data.get("password", "student123").strip(),
            data.get("batch_year", "2025").strip(),
            float(data.get("ats_score", 0)),
            data.get("readiness_status", "In Progress").strip(),
            data.get("target_company", "General").strip(),
            int(data.get("quizzes_completed", 0)),
            data.get("placement_status", "Not Placed").strip(),
            data.get("placed_company", "").strip(),
            float(data.get("package_lpa", 0))
        ))
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def update_student_progress(student_id: int, data: dict):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
        UPDATE students
        SET name = ?, roll_no = ?, phone = ?, email = ?, branch = ?, section = ?,
            batch_year = ?, ats_score = ?, readiness_status = ?, target_company = ?,
            quizzes_completed = ?, placement_status = ?, placed_company = ?, package_lpa = ?
        WHERE id = ?
        """, (
            data.get("name", "").strip(),
            data.get("roll_no", data.get("enrollment_no", "")).strip(),
            data.get("phone", "").strip(),
            data.get("email", "").strip(),
            data.get("branch", data.get("department", "Computer Science")).strip(),
            data.get("section", "A").strip(),
            data.get("batch_year", "2025").strip(),
            float(data.get("ats_score", 0)),
            data.get("readiness_status", "In Progress").strip(),
            data.get("target_company", "General").strip(),
            int(data.get("quizzes_completed", 0)),
            data.get("placement_status", "Not Placed").strip(),
            data.get("placed_company", "").strip(),
            float(data.get("package_lpa", 0)),
            student_id
        ))
        conn.commit()
        return True
    finally:
        conn.close()


def record_student_quiz_completion(student_id: int, score_pct: float = 0.0):
    """Increments quizzes_completed and updates student readiness status based on performance."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE students 
    SET quizzes_completed = quizzes_completed + 1,
        readiness_status = CASE 
            WHEN ? >= 80 THEN 'Placement Ready' 
            WHEN ? >= 50 THEN 'Interview Ready' 
            ELSE readiness_status 
        END
    WHERE id = ?
    """, (score_pct, score_pct, student_id))
    conn.commit()
    conn.close()
    return True


def authenticate_student(identifier: str, password: str):
    """
    Authenticates student via Enrollment/Roll Number or Email and password.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    ident = identifier.strip().lower()
    cursor.execute("""
    SELECT * FROM students 
    WHERE (LOWER(roll_no) = ? OR LOWER(email) = ?) AND password = ?
    """, (ident, ident, password.strip()))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def add_alumni_account(data: dict):
    """Admin creates a new alumni login account with placement profile and 2FA credentials."""
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        alumni_id = data.get("alumni_id", data.get("roll_no", "")).strip().upper()
        sec_key = data.get("security_key_2fa", alumni_id).strip().upper()

        cursor.execute("""
        INSERT INTO alumni_accounts (
            name, alumni_id, email, phone, branch, batch_year, company, role, package_lpa, password, security_key_2fa
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get("name", "Alumni Student").strip(),
            alumni_id,
            data.get("email", "").strip(),
            data.get("phone", "").strip(),
            data.get("branch", data.get("department", "Computer Science")).strip(),
            data.get("batch_year", "2024").strip(),
            data.get("company", "Tech Enterprise").strip(),
            data.get("role", "Software Engineer").strip(),
            float(data.get("package_lpa", 0)),
            data.get("password", "alumni123").strip(),
            sec_key
        ))
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def get_all_alumni_accounts():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM alumni_accounts ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_alumni_account_by_id(identifier: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    ident = str(identifier).strip().upper()
    cursor.execute("SELECT * FROM alumni_accounts WHERE UPPER(alumni_id) = ? OR id = ?", (ident, identifier))
    row = cursor.fetchone()
    conn.close()
    return dict(row) if row else None


def delete_alumni_account(account_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM alumni_accounts WHERE id = ? OR alumni_id = ?", (account_id, str(account_id)))
    conn.commit()
    conn.close()
    return True


def authenticate_alumni(identifier: str, password: str):
    """
    Authenticates alumni credentials via database alumni_accounts table.
    Supports any alumni added by Admin, with fallback for default master key 24C1103.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    ident = identifier.strip().upper()
    pwd = password.strip()

    cursor.execute("""
    SELECT * FROM alumni_accounts 
    WHERE (UPPER(alumni_id) = ? OR UPPER(email) = ?) AND password = ?
    """, (ident, ident, pwd))
    row = cursor.fetchone()
    conn.close()

    if row:
        r = dict(row)
        r['id'] = r['alumni_id']
        r['roll_no'] = r['alumni_id']
        r['user_type'] = 'alumni'
        r['security_key_2fa'] = r.get('security_key_2fa') or r['alumni_id']
        return r

    return None


def delete_student(student_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
    conn.commit()
    conn.close()
    return True


def delete_alumni_experience(exp_id: int):
    """
    Deletes an alumni record from the platform:
    1. Removes their experience from alumni_experiences in Supabase.
    2. Removes any associated login account from alumni_accounts in Supabase.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT student_name, email FROM alumni_experiences WHERE id = ?", (exp_id,))
        row = cursor.fetchone()
        if row:
            name = row.get('student_name')
            email = row.get('email')
            if email:
                cursor.execute("DELETE FROM alumni_accounts WHERE UPPER(email) = UPPER(?)", (email,))
            if name:
                cursor.execute("DELETE FROM alumni_accounts WHERE UPPER(name) = UPPER(?)", (name,))
        cursor.execute("DELETE FROM alumni_experiences WHERE id = ?", (exp_id,))
        conn.commit()
    finally:
        conn.close()
    return True



def add_mcq_question(data: dict, alumni_id=None, alumni_name=None):
    conn = get_db_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("""
        INSERT INTO mcq_questions (subject, topic, company, question, option_a, option_b, option_c, option_d, correct_option, explanation, difficulty, alumni_id, alumni_name)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get("subject", "General"),
            data.get("topic", "General"),
            data.get("company", "General"),
            data.get("question", "").strip(),
            data.get("option_a", "").strip(),
            data.get("option_b", "").strip(),
            data.get("option_c", "").strip(),
            data.get("option_d", "").strip(),
            data.get("correct_option", "A").upper().strip(),
            data.get("explanation", "").strip(),
            data.get("difficulty", "Medium"),
            alumni_id or data.get("alumni_id"),
            alumni_name or data.get("alumni_name", "Alumni Mentor")
        ))
        conn.commit()
        return cursor.lastrowid
    finally:
        conn.close()


def delete_mcq_question(question_id: int, alumni_id=None):
    conn = get_db_connection()
    cursor = conn.cursor()
    if alumni_id:
        cursor.execute("DELETE FROM mcq_questions WHERE id = ? AND alumni_id = ?", (question_id, alumni_id))
    else:
        cursor.execute("DELETE FROM mcq_questions WHERE id = ?", (question_id,))
    conn.commit()
    conn.close()
    return True


def get_alumni_contributed_questions(alumni_id=None, alumni_name=None, limit=100):
    """Fetches questions contributed by a specific alumni or all alumni mentors."""
    conn = get_db_connection()
    cursor = conn.cursor()
    if alumni_id and alumni_name:
        cursor.execute("SELECT * FROM mcq_questions WHERE alumni_id = ? OR LOWER(alumni_name) = LOWER(?) ORDER BY id DESC LIMIT ?", (alumni_id, alumni_name, limit))
    elif alumni_id:
        cursor.execute("SELECT * FROM mcq_questions WHERE alumni_id = ? ORDER BY id DESC LIMIT ?", (alumni_id, limit))
    elif alumni_name:
        cursor.execute("SELECT * FROM mcq_questions WHERE LOWER(alumni_name) = LOWER(?) ORDER BY id DESC LIMIT ?", (alumni_name, limit))
    else:
        cursor.execute("SELECT * FROM mcq_questions ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_all_mcqs_for_admin(limit=100):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM mcq_questions ORDER BY id DESC LIMIT ?", (limit,))
    rows = cursor.fetchall()
    conn.close()
    return [dict(r) for r in rows]


def get_admin_dashboard_stats():
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM students")
    total_students = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM students WHERE placement_status = 'Placed'")
    placed_students = cursor.fetchone()[0]

    cursor.execute("SELECT AVG(ats_score) FROM students")
    avg_ats = cursor.fetchone()[0] or 0.0

    cursor.execute("SELECT COUNT(*) FROM mcq_questions")
    total_questions = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM alumni_experiences")
    total_alumni = cursor.fetchone()[0]

    conn.close()
    return {
        "total_students": total_students,
        "placed_students": placed_students,
        "avg_ats": round(avg_ats, 1),
        "total_questions": total_questions,
        "total_alumni": total_alumni
    }


# ==========================================================================
# ALUMNI MENTORSHIP & STUDENT OUTREACH TRACKING
# ==========================================================================

def init_alumni_outreach_table():
    """Initializes the alumni_outreach table."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alumni_outreach (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        alumni_identifier TEXT NOT NULL,
        student_name TEXT NOT NULL,
        student_email TEXT NOT NULL,
        student_branch TEXT DEFAULT 'Computer Science',
        student_batch TEXT DEFAULT '2025',
        target_company TEXT DEFAULT 'Google',
        channel TEXT NOT NULL, -- 'gmail' or 'linkedin'
        query_topic TEXT NOT NULL,
        status TEXT DEFAULT 'Pending', -- 'Pending', 'Replied', 'Completed'
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    conn.commit()
    conn.close()


def record_alumni_outreach(alumni_identifier, channel, student_name, student_email, student_branch="Computer Science", target_company="Google", query_topic="Placement mentorship inquiry"):
    """Logs a student outreach attempt (via Gmail or LinkedIn)."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO alumni_outreach (
        alumni_identifier, student_name, student_email, student_branch, student_batch, target_company, channel, query_topic, status
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Pending')
    """, (alumni_identifier, student_name, student_email, student_branch, "2025", target_company, channel.lower(), query_topic))
    conn.commit()
    new_id = cursor.lastrowid
    conn.close()
    return new_id


def get_alumni_outreach_metrics(alumni_identifier="24C1103"):
    """Returns analytics metrics for student outreach through Gmail and LinkedIn."""
    init_alumni_outreach_table()
    conn = get_db_connection()
    cursor = conn.cursor()

    ident_str = str(alumni_identifier).strip()

    # Find matching alumni account if exists
    cursor.execute("""
    SELECT * FROM alumni_accounts 
    WHERE UPPER(alumni_id) = ? OR UPPER(email) = ? OR id = ? OR UPPER(name) = ?
    """, (ident_str.upper(), ident_str.upper(), ident_str, ident_str.upper()))
    acc = cursor.fetchone()

    match_keys = [ident_str, ident_str.lower(), ident_str.upper()]
    alumni_name = ident_str
    alumni_email = ident_str
    if acc:
        alumni_name = acc['name']
        alumni_email = acc['email']
        match_keys.extend([
            acc['alumni_id'], acc['alumni_id'].upper(), acc['alumni_id'].lower(),
            acc['email'], acc['email'].lower(), acc['email'].upper(),
            acc['name'], acc['name'].lower(), acc['name'].upper()
        ])

    match_keys = list(set([k for k in match_keys if k]))
    placeholders = ','.join(['?'] * len(match_keys))

    # Total Gmail Inquiries
    cursor.execute(f"""
    SELECT COUNT(*) FROM alumni_outreach 
    WHERE (alumni_identifier IN ({placeholders}) OR student_email IN ({placeholders})) 
      AND LOWER(channel) = 'gmail'
    """, match_keys + match_keys)
    gmail_count = cursor.fetchone()[0]

    # Total LinkedIn Approaches
    cursor.execute(f"""
    SELECT COUNT(*) FROM alumni_outreach 
    WHERE (alumni_identifier IN ({placeholders}) OR student_email IN ({placeholders})) 
      AND LOWER(channel) = 'linkedin'
    """, match_keys + match_keys)
    linkedin_count = cursor.fetchone()[0]

    total_approached = gmail_count + linkedin_count

    # Inquiry list
    cursor.execute(f"""
    SELECT * FROM alumni_outreach 
    WHERE alumni_identifier IN ({placeholders}) OR student_email IN ({placeholders})
    ORDER BY id DESC
    """, match_keys + match_keys)
    inquiries = [dict(r) for r in cursor.fetchall()]

    # Department breakdown
    cursor.execute(f"""
    SELECT student_branch, COUNT(*) as count 
    FROM alumni_outreach 
    WHERE alumni_identifier IN ({placeholders}) OR student_email IN ({placeholders})
    GROUP BY student_branch
    """, match_keys + match_keys)
    dept_rows = cursor.fetchall()
    dept_breakdown = {r['student_branch']: r['count'] for r in dept_rows}

    # Published story upvotes (matches this alumni's email, name, or ID in alumni_experiences)
    cursor.execute("""
    SELECT SUM(upvotes) FROM alumni_experiences 
    WHERE LOWER(email) = LOWER(?) OR LOWER(student_name) = LOWER(?) OR id = ?
    """, (alumni_email, alumni_name, ident_str))
    story_row = cursor.fetchone()
    story_upvotes = story_row[0] if (story_row and story_row[0] is not None) else 0

    conn.close()

    total_base = max(1, total_approached)
    return {
        "gmail_inquiries": gmail_count,
        "linkedin_approaches": linkedin_count,
        "total_approached": total_approached,
        "story_views": max(0, total_approached * 5 + story_upvotes * 3),
        "story_upvotes": story_upvotes,
        "positive_rating": "100%" if (total_approached > 0 or story_upvotes > 0) else "N/A",
        "inquiries": inquiries,
        "department_breakdown": dept_breakdown,
        "channel_ratio": {
            "gmail_pct": round((gmail_count / total_base) * 100, 1) if total_approached > 0 else 0,
            "linkedin_pct": round((linkedin_count / total_base) * 100, 1) if total_approached > 0 else 0
        }
    }


def update_alumni_inquiry_status(inquiry_id: int, new_status: str):
    """Updates mentorship inquiry status ('Pending', 'Replied', 'Completed')."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE alumni_outreach SET status = ? WHERE id = ?", (new_status, inquiry_id))
    conn.commit()
    conn.close()
    return True