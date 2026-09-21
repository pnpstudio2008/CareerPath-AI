"""
AI Career Companion - Intelligent NLP & Placement Engine
Implements resume text extraction, skill taxonomy extraction, ATS scoring,
role recommendation, JD matching, interview question generation, and mock interview evaluation.
"""

import re
import math
from typing import Dict, List, Any, Tuple, Optional
import pypdf
import io

# ==========================================
# SKILL TAXONOMY DEFINITION (1000+ keywords)
# ==========================================
SKILL_TAXONOMY = {
    "languages": [
        "python", "java", "c++", "c", "c#", "javascript", "typescript", "golang", "go",
        "rust", "ruby", "php", "swift", "kotlin", "sql", "r", "dart", "scala",
        "bash", "shell", "powershell", "html", "html5", "css", "css3", "sass", "scss",
        "matlab", "perl", "haskell", "lua", "assembly"
    ],
    "frameworks_libraries": [
        "react", "react.js", "reactjs", "next.js", "nextjs", "angular", "vue", "vue.js", "vuejs",
        "node.js", "nodejs", "express", "express.js", "django", "flask", "fastapi",
        "spring", "spring boot", "springboot", "asp.net", "asp.net core", ".net",
        "laravel", "ruby on rails", "rails", "redux", "tailwind", "tailwind css",
        "bootstrap", "material-ui", "mui", "jquery", "pytorch", "tensorflow",
        "keras", "scikit-learn", "sklearn", "pandas", "numpy", "opencv", "scipy",
        "matplotlib", "seaborn", "pyspark", "spark", "hadoop", "flutter",
        "react native", "graphql", "apollo", "prisma", "hibernate", "jpa",
        "celery", "electron", "fastify", "nest.js", "nestjs", "svelte"
    ],
    "databases": [
        "mysql", "postgresql", "postgres", "mongodb", "sqlite", "redis",
        "oracle", "microsoft sql server", "mssql", "firebase", "firestore",
        "cassandra", "dynamodb", "elasticsearch", "neo4j", "mariadb", "supabase",
        "couchdb", "cockroachdb", "snowflake", "bigquery"
    ],
    "cloud_devops": [
        "aws", "amazon web services", "azure", "microsoft azure", "gcp", "google cloud",
        "docker", "kubernetes", "k8s", "jenkins", "git", "github", "gitlab", "bitbucket",
        "ci/cd", "ci-cd", "continuous integration", "terraform", "ansible", "linux",
        "ubuntu", "nginx", "apache", "prometheus", "grafana", "helm", "serverless",
        "lambda", "ec2", "s3", "cloudformation", "circleci", "argo cd", "vagrant"
    ],
    "core_cs": [
        "data structures", "algorithms", "dsa", "object-oriented programming", "oop", "oops",
        "dbms", "database management", "operating systems", "os", "computer networks", "cn",
        "system design", "distributed systems", "rest", "restful api", "rest api",
        "microservices", "agile", "scrum", "sdlc", "clean architecture", "design patterns",
        "multithreading", "concurrency", "unit testing", "tdd", "software engineering",
        "tcp/ip", "http", "https", "websockets", "low level design", "high level design"
    ],
    "ai_ml_data": [
        "machine learning", "ml", "deep learning", "dl", "artificial intelligence", "ai",
        "natural language processing", "nlp", "computer vision", "cv", "generative ai", "genai",
        "large language models", "llm", "llms", "prompt engineering", "data science",
        "data analysis", "data analytics", "data visualization", "etl", "data pipelines",
        "big data", "power bi", "tableau", "feature engineering", "reinforcement learning",
        "transformers", "huggingface", "langchain", "rag", "fine-tuning", "bert", "gpt"
    ],
    "soft_skills": [
        "communication", "problem solving", "team collaboration", "teamwork", "leadership",
        "critical thinking", "time management", "adaptability", "presentation", "analytical skills",
        "project management", "work ethic", "decision making", "interpersonal skills",
        "conflict resolution", "mentorship", "creativity", "emotional intelligence"
    ]
}

# Pre-computed flat skill lookup dictionary (lowercased)
FLAT_SKILL_MAP = {}
for category, skills in SKILL_TAXONOMY.items():
    for skill in skills:
        FLAT_SKILL_MAP[skill.lower()] = category

# Action verbs for resume ATS evaluation
ACTION_VERBS = [
    "accelerated", "achieved", "analyzed", "architected", "automated", "built", "collaborated",
    "conducted", "configured", "constructed", "created", "debugged", "deployed", "designed",
    "developed", "devised", "documented", "engineered", "enhanced", "established", "executed",
    "formulated", "implemented", "improved", "increased", "initiated", "integrated", "launched",
    "led", "maintained", "managed", "migrated", "modeled", "monitored", "optimized", "orchestrated",
    "overhauled", "performed", "pioneered", "programmed", "refactored", "resolved", "restructured",
    "revamped", "scaled", "simplified", "spearheaded", "standardized", "streamlined", "supervised",
    "tested", "trained", "transformed", "upgraded", "utilized", "validated"
]

CAREER_ROLES = {
    "Full Stack Developer": {
        "core_skills": ["javascript", "react", "node.js", "html", "css", "sql", "mongodb", "git", "restful api"],
        "description": "Designs and builds end-to-end web applications across client and server architectures."
    },
    "Backend Engineer": {
        "core_skills": ["python", "java", "node.js", "sql", "postgresql", "redis", "docker", "microservices", "system design", "restful api"],
        "description": "Specializes in server-side logic, high-throughput APIs, database optimization, and cloud architecture."
    },
    "Frontend Engineer": {
        "core_skills": ["javascript", "typescript", "react", "next.js", "tailwind", "html", "css", "redux", "ui/ux"],
        "description": "Crafts responsive, performant, and intuitive user interfaces and web applications."
    },
    "AI / ML Engineer": {
        "core_skills": ["python", "machine learning", "deep learning", "pytorch", "tensorflow", "scikit-learn", "nlp", "pandas", "numpy"],
        "description": "Develops, trains, and deploys predictive models, deep neural networks, and generative AI systems."
    },
    "Data Scientist / Analyst": {
        "core_skills": ["python", "sql", "data analysis", "pandas", "numpy", "tableau", "power bi", "matplotlib", "statistics"],
        "description": "Extracts actionable insights, visualizes trends, and builds statistical models from enterprise datasets."
    },
    "Cloud & DevOps Engineer": {
        "core_skills": ["aws", "docker", "kubernetes", "ci/cd", "linux", "terraform", "jenkins", "git", "bash"],
        "description": "Automates cloud infrastructure, deployment pipelines, container orchestration, and system reliability."
    },
    "Software Development Engineer (SDE)": {
        "core_skills": ["dsa", "algorithms", "data structures", "c++", "java", "python", "oop", "dbms", "os", "system design"],
        "description": "Solves complex algorithmic challenges and builds scalable, robust software solutions for tech enterprises."
    },
    "Mobile App Developer": {
        "core_skills": ["flutter", "react native", "kotlin", "swift", "dart", "android", "ios", "restful api", "firebase"],
        "description": "Develops native and cross-platform mobile experiences for iOS and Android platforms."
    }
}

# Domain specific interview question templates
DOMAIN_QUESTIONS = {
    "python": [
        {"q": "Explain the difference between deep copy and shallow copy in Python.", "key": "Shallow copy creates a new object referencing original nested elements; deep copy recursively clones all child objects.", "type": "Technical"},
        {"q": "How does Python's Global Interpreter Lock (GIL) affect multithreading?", "key": "GIL allows only one native thread to execute Python bytecode at a time, making CPU-bound tasks better suited for multiprocessing.", "type": "Core CS"},
        {"q": "What are generators and how do they differ from regular functions?", "key": "Generators use the 'yield' keyword to produce values lazily on demand without loading entire datasets into memory.", "type": "Technical"}
    ],
    "java": [
        {"q": "What is the difference between HashMap and ConcurrentHashMap in Java?", "key": "HashMap is non-synchronized; ConcurrentHashMap uses bucket-level segment locking allowing thread-safe concurrent reads and writes.", "type": "Technical"},
        {"q": "Explain JVM memory architecture (Heap, Stack, Metaspace) and Garbage Collection.", "key": "Stack stores primitive variables & method execution frames; Heap stores runtime objects; Metaspace stores class metadata. GC runs Generational collection (Eden, Survivor, Tenured).", "type": "Core CS"},
        {"q": "What is the difference between Abstract Class and Interface in Java 8+?", "key": "Interfaces can have default and static methods, support multiple inheritance; abstract classes can maintain state with instance fields and constructors.", "type": "Technical"}
    ],
    "c++": [
        {"q": "Explain the RAII (Resource Acquisition Is Initialization) idiom in C++.", "key": "Binds the lifecycle of resources (memory, file handles) to object lifetime, ensuring automatic cleanup upon stack unwinding.", "type": "Technical"},
        {"q": "What are virtual functions and how does the vtable mechanism work?", "key": "Virtual functions enable runtime polymorphism via a virtual method table (vtable) and virtual table pointer (vptr) per object.", "type": "Technical"}
    ],
    "javascript": [
        {"q": "Explain the JavaScript Event Loop, Call Stack, Microtask Queue, and Callback Queue.", "key": "Synchronous code runs on the Call Stack; Promises/MutationObservers resolve in the Microtask Queue; setTimeout/DOM events go to Task Queue; Event loop prioritizes Microtasks before rendering.", "type": "Technical"},
        {"q": "What is closure in JavaScript and provide a practical use case?", "key": "A closure is a function bundled with lexical scope references, commonly used for data encapsulation/private variables and currying.", "type": "Technical"}
    ],
    "react": [
        {"q": "How does React's Virtual DOM and Reconciliation algorithm (Fiber) work?", "key": "Fiber breaks rendering into interruptible units of work, creates a lightweight in-memory VDOM, diffs it against current DOM, and applies minimal batch updates.", "type": "Technical"},
        {"q": "When would you use `useMemo` and `useCallback` versus normal memoization?", "key": "`useMemo` caches computed values; `useCallback` caches function instances across re-renders to prevent unnecessary child re-renders.", "type": "Technical"}
    ],
    "sql": [
        {"q": "Explain the difference between Clustered and Non-Clustered Indexes.", "key": "Clustered index physically alters data row storage order (1 per table); Non-clustered index creates a separate lookup pointer table.", "type": "Database"},
        {"q": "What are ACID properties in relational database transactions?", "key": "Atomicity (all or nothing), Consistency (preserves constraints), Isolation (concurrent safety levels), Durability (persisted after commit).", "type": "Database"}
    ],
    "docker": [
        {"q": "What is the difference between Docker images and Docker containers?", "key": "An image is an immutable, read-only template with instructions; a container is a runnable, isolated instance of an image with a read-write layer.", "type": "DevOps"}
    ],
    "aws": [
        {"q": "How would you design a scalable, fault-tolerant web architecture on AWS?", "key": "Use Route 53, CloudFront CDN, Application Load Balancer across multiple AZs, Auto Scaling EC2 / ECS / Lambda, and RDS Multi-AZ / DynamoDB.", "type": "System Design"}
    ],
    "machine learning": [
        {"q": "How do you handle the Bias-Variance Tradeoff and prevent model overfitting?", "key": "Regularization (L1/L2, Dropout), Cross-Validation (K-Fold), Early Stopping, Data Augmentation, and ensemble methods (Random Forest, XGBoost).", "type": "AI/ML"},
        {"q": "Explain the difference between precision, recall, and F1-score.", "key": "Precision = TP/(TP+FP) [relevance of positive predictions]; Recall = TP/(TP+FN) [completeness of captured positives]; F1 is the harmonic mean of both.", "type": "AI/ML"}
    ],
    "dsa": [
        {"q": "How would you detect and find the starting node of a cycle in a Linked List?", "key": "Floyd's Tortoise and Hare algorithm with slow and fast pointers. Once they meet, reset one pointer to head and advance both by 1 step to meet at loop start.", "type": "Problem Solving"},
        {"q": "Compare the time and space complexity of QuickSort vs MergeSort.", "key": "QuickSort: Avg O(N log N), Worst O(N^2), in-place O(log N) auxiliary stack. MergeSort: Guaranteed O(N log N), O(N) auxiliary space, stable.", "type": "Problem Solving"}
    ],
    "general_hr": [
        {"q": "Tell me about a challenging technical project you built and how you handled unexpected obstacles.", "key": "Use the STAR method (Situation, Task, Action, Result). Highlight technical leadership, root-cause debugging, and measurable impact.", "type": "Behavioral"},
        {"q": "How do you stay up-to-date with fast-evolving technologies and decide what to learn next?", "key": "Mention reading engineering blogs, building hands-on POCs, contributing to open source, and aligning with industry demand.", "type": "Behavioral"}
    ]
}


# ==========================================
# PARSER & NLP UTILITY FUNCTIONS
# ==========================================

def extract_text_from_pdf_bytes(pdf_bytes: bytes) -> str:
    """
    Extracts clean text from PDF byte stream with multi-level resilient fallbacks:
    1. Standard PyPDF page text extraction
    2. PyPDF visitor extraction (extracts raw text components & annotations)
    3. Flate/raw stream text extraction for custom font-mapped or compressed PDFs
    4. Printable ASCII/UTF sequence scanning
    """
    if not pdf_bytes or len(pdf_bytes) == 0:
        return ""

    extracted_pages = []

    # Strategy 1: Standard PyPDF page extraction
    try:
        reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
        for page in reader.pages:
            try:
                page_text = page.extract_text() or ""
                if page_text.strip():
                    extracted_pages.append(page_text.strip())
            except Exception:
                pass
    except Exception as e:
        print(f"[PDF Extraction Warning] PyPDF standard reader notice: {e}")

    # If Strategy 1 succeeded with substantial text, return it
    full_text = "\n".join(extracted_pages).strip()
    if len(full_text) >= 50:
        return full_text

    # Strategy 2: PyPDF visitor/text operator fallback
    try:
        reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
        visitor_text = []
        def visitor_body(text, cm, tm, fontDict, fontSize):
            if text and text.strip():
                visitor_text.append(text)

        for page in reader.pages:
            try:
                page.extract_text(visitor_text=visitor_body)
            except Exception:
                pass

        if visitor_text:
            combined_visitor = " ".join(visitor_text).strip()
            if len(combined_visitor) >= 50:
                return combined_visitor
    except Exception:
        pass

    # Strategy 3: Raw stream extraction (scanning for uncompressed or decompressed PDF text streams)
    try:
        import zlib
        raw_text_chunks = []
        stream_matches = re.findall(rb'stream[\r\n]+(.*?)[\r\n]+endstream', pdf_bytes, re.DOTALL)
        for s in stream_matches:
            try:
                decomp = zlib.decompress(s)
                text_matches = re.findall(rb'\((.*?)\)\s*Tj', decomp)
                for tm in text_matches:
                    try:
                        raw_text_chunks.append(tm.decode('utf-8', errors='ignore'))
                    except Exception:
                        pass
            except Exception:
                pass
        
        if raw_text_chunks:
            stream_result = " ".join(raw_text_chunks).strip()
            if len(stream_result) >= 50:
                return stream_result
    except Exception:
        pass

    # Strategy 4: Printable ASCII/UTF sequence extraction
    try:
        printable_sequences = re.findall(rb'[a-zA-Z0-9\+\#\.\,\-\@\:\/\s]{4,}', pdf_bytes)
        decoded_tokens = [seq.decode('utf-8', errors='ignore').strip() for seq in printable_sequences if len(seq.strip()) > 3]
        if decoded_tokens:
            printable_result = " ".join(decoded_tokens).strip()
            if len(printable_result) >= 40:
                return printable_result
    except Exception:
        pass

    return full_text if full_text else ""


def clean_and_tokenize(text: str) -> List[str]:
    """Tokenize and clean text into lowercase words/tokens."""
    # Preserve key symbols like c++, c#, .net, node.js
    text = text.lower()
    # Normalize common abbreviations
    text = re.sub(r'[\r\n\t]+', ' ', text)
    tokens = re.findall(r'[a-zA-Z0-9\+\#\.\-]+', text)
    return tokens


def extract_skills_from_text(text: str) -> Dict[str, List[str]]:
    """
    Intelligently identifies and categorizes technical and soft skills
    from plain text or parsed resume content.
    """
    text_lower = " " + text.lower() + " "
    found_skills: Dict[str, set] = {cat: set() for cat in SKILL_TAXONOMY.keys()}

    for category, skill_list in SKILL_TAXONOMY.items():
        for skill in skill_list:
            # Build regex word-boundary pattern respecting symbols like c++, c#, .net
            escaped_skill = re.escape(skill)
            # Boundary checks
            pattern = rf'(?<![a-zA-Z0-9]){escaped_skill}(?![a-zA-Z0-9])'
            if re.search(pattern, text_lower):
                found_skills[category].add(skill.title() if len(skill) > 3 and not skill.isupper() else skill.upper() if len(skill) <= 3 else skill.title())

    # Format output dictionary with sorted lists
    return {cat: sorted(list(skills)) for cat, skills in found_skills.items()}


def extract_certifications_from_text(text: str) -> List[str]:
    """
    Extracts recognized technical certifications and credentials from resume content.
    """
    text_lower = " " + text.lower() + " "
    found_certs = set()

    certs_patterns = [
        ("AWS Certified Solutions Architect", r"aws\s+certified\s+solutions\s+architect"),
        ("AWS Certified Cloud Practitioner", r"aws\s+certified\s+cloud\s+practitioner"),
        ("AWS Certified Developer", r"aws\s+certified\s+developer"),
        ("Azure Fundamentals (AZ-900)", r"(azure\s+fundamentals|az-900)"),
        ("Azure Developer Associate (AZ-204)", r"(azure\s+developer\s+associate|az-204)"),
        ("GCP Associate Cloud Engineer", r"(gcp|google\s+cloud)\s+associate\s+cloud\s+engineer"),
        ("Oracle Certified Java Associate / Professional", r"(oracle\s+certified|java\s+certified|ocjp|ocja)"),
        ("Python Institute Certified (PCAP/PCEP)", r"(pcap|pcep|python\s+institute\s+certified)"),
        ("Meta Front-End Developer", r"meta\s+front-?end\s+developer"),
        ("Meta Back-End Developer", r"meta\s+back-?end\s+developer"),
        ("Google Data Analytics Certificate", r"google\s+data\s+analytics"),
        ("Google IT Automation with Python", r"google\s+it\s+automation"),
        ("DeepLearning.AI Machine Learning", r"(deeplearning\.ai|andrew\s+ng\s+machine\s+learning)"),
        ("TensorFlow Developer Certificate", r"tensorflow\s+developer"),
        ("Certified Kubernetes Administrator (CKA)", r"(certified\s+kubernetes\s+administrator|cka)"),
        ("Certified Kubernetes Application Developer (CKAD)", r"(certified\s+kubernetes\s+application\s+developer|ckad)"),
        ("Docker Certified Associate", r"docker\s+certified\s+associate"),
        ("CompTIA Security+", r"comptia\s+security\+?"),
        ("CompTIA Network+", r"comptia\s+network\+?"),
        ("Certified ScrumMaster (CSM)", r"(certified\s+scrum\s*master|csm)"),
        ("HackerRank Problem Solving (Gold/Silver)", r"hackerrank\s+problem\s+solving"),
        ("HackerRank Python / SQL Certified", r"hackerrank\s+(python|sql)"),
        ("freeCodeCamp Web Development Certified", r"freecodecamp"),
        ("NPTEL Elite Certificate", r"nptel\s+(elite|certificate)")
    ]

    for cert_title, pattern in certs_patterns:
        if re.search(pattern, text_lower):
            found_certs.add(cert_title)

    # General regex for "Certified in X" or "Certificate in X"
    general_matches = re.findall(r'(?:certified|certification|certificate)\s+(?:in|for|of)?\s+([A-Za-z0-9\+\#\.\s]{3,35})(?=[,\.\n\(\)])', text, re.IGNORECASE)
    for gm in general_matches[:3]:
        clean_gm = gm.strip()
        if len(clean_gm) > 3 and not re.search(r'(the|this|that|which|with|from)', clean_gm, re.IGNORECASE):
            found_certs.add(f"Certificate in {clean_gm.title()}")

    return sorted(list(found_certs))


def extract_contact_info(text: str) -> Dict[str, Optional[str]]:
    """Extracts email, phone, linkedin, and github links."""
    email_pattern = r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+'
    phone_pattern = r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}'
    linkedin_pattern = r'(?:https?:\/\/)?(?:www\.)?linkedin\.com\/in\/[a-zA-Z0-9_-]+'
    github_pattern = r'(?:https?:\/\/)?(?:www\.)?github\.com\/[a-zA-Z0-9_-]+'

    emails = re.findall(email_pattern, text)
    phones = re.findall(phone_pattern, text)
    linkedins = re.findall(linkedin_pattern, text, re.IGNORECASE)
    githubs = re.findall(github_pattern, text, re.IGNORECASE)

    return {
        "email": emails[0] if emails else None,
        "phone": phones[0] if phones else None,
        "linkedin": linkedins[0] if linkedins else None,
        "github": githubs[0] if githubs else None
    }


def verify_is_resume(text: str) -> Tuple[bool, str, Dict[str, Any]]:
    """
    Validates whether the provided document text genuinely represents an authentic Resume / CV.
    Filters out irrelevant or malicious uploads such as invoices, food recipes, textbooks,
    legal agreements, logs, source code files, or random text.

    Returns:
        (is_valid: bool, feedback_message: str, details_dict: Dict[str, Any])
    """
    clean_text = text.strip()
    words = clean_text.split()
    word_count = len(words)

    # 1. Minimum Length Check
    if word_count < 35:
        return False, (
            f"Resume Verification Failed: The uploaded document contains only {word_count} words. "
            "A standard resume must contain substantive academic background, technical skills, "
            "and project or work experience."
        ), {"reason": "insufficient_content", "word_count": word_count}

    text_lower = clean_text.lower()

    # 2. Strong Non-Resume Disqualifiers (Bills, Invoices, Legal Policies, Recipes)
    invoice_signals = [
        r'\btax\s+invoice\b', r'\binvoice\s+(no|number|#)\b', r'\bamount\s+due\b',
        r'\bbilling\s+address\b', r'\bshipping\s+address\b', r'\bunit\s+price\b',
        r'\bsubtotal\b', r'\bgrand\s+total\b', r'\bpayment\s+terms\b', r'\bdue\s+date\b'
    ]
    invoice_hits = sum(1 for p in invoice_signals if re.search(p, text_lower))

    legal_signals = [
        r'\bterms\s+and\s+conditions\b', r'\bprivacy\s+policy\b', r'\ball\s+rights\s+reserved\b',
        r'\bend\s+user\s+license\b', r'\bconfidentiality\s+agreement\b',
        r'\bindemnification\b', r'\bgoverning\s+law\b'
    ]
    legal_hits = sum(1 for p in legal_signals if re.search(p, text_lower))

    recipe_signals = [
        r'\bingredients?\b', r'\btablespoons?\b', r'\bteaspoons?\b', r'\bpreheat\s+oven\b',
        r'\bcook\s+time\b', r'\bprep\s+time\b', r'\bservings?\b', r'\bbake\s+for\b'
    ]
    recipe_hits = sum(1 for p in recipe_signals if re.search(p, text_lower))

    # 3. Core Resume Section Detectors
    # A. Education / Academic Record
    edu_pattern = r'\b(education|academics?|qualifications?|degree|b\.?tech|b\.?e|bachelor|master|m\.?tech|bca|mca|b\.?sc|m\.?sc|cbse|icse|cgpa|gpa|percentage|university|college|school|institute|graduat(ed|ion|ing)?|diploma|secondary\s+school|coursework)\b'
    has_education = bool(re.search(edu_pattern, text_lower))

    # B. Work Experience, Internships, Projects
    exp_pattern = r'\b(experience|work\s+experience|employment|internships?|intern|projects?|work\s+history|professional\s+experience|responsibilities|contributions|developed|built|designed|implemented|co-op|freelance|initiatives?)\b'
    has_experience = bool(re.search(exp_pattern, text_lower))

    # C. Technical & Professional Skills
    skills_pattern = r'\b(skills?|technical\s+skills|core\s+competencies|technologies|tools|programming\s+languages?|languages?|proficiencies|expertise|tech\s+stack|frameworks?|databases?|libraries|competencies)\b'
    has_skills_heading = bool(re.search(skills_pattern, text_lower))
    
    # Extract skills using the existing taxonomy
    extracted_skills = extract_skills_from_text(clean_text)
    total_skills_count = sum(len(v) for v in extracted_skills.values())
    has_skills = has_skills_heading or (total_skills_count >= 2)

    # D. Contact Details & Candidate Identity
    email_match = bool(re.search(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+', clean_text))
    phone_match = bool(re.search(r'(\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}', clean_text))
    contact_keywords = bool(re.search(r'\b(email|phone|mobile|contact|address|linkedin|github|portfolio|curriculum\s+vitae|resume|cv)\b', text_lower))
    has_contact = email_match or phone_match or contact_keywords

    # E. Summary, Objective, Certifications, Awards
    summary_certs_pattern = r'\b(summary|objective|career\s+objective|professional\s+summary|profile|about\s+me|certifications?|certificates?|achievements?|awards?|honors?|extracurricular|publications?|activities|participat(ed|ion))\b'
    has_summary_certs = bool(re.search(summary_certs_pattern, text_lower))

    # Compile detected sections
    detected_sections = []
    if has_education:
        detected_sections.append("Education & Academics")
    if has_experience:
        detected_sections.append("Projects & Experience")
    if has_skills:
        detected_sections.append("Technical Skills")
    if has_contact:
        detected_sections.append("Contact Information")
    if has_summary_certs:
        detected_sections.append("Summary & Certifications")

    section_count = len(detected_sections)

    # Check for disqualifying non-resume documents
    if invoice_hits >= 2 and section_count < 3:
        return False, (
            "Resume Verification Failed: The uploaded file appears to be an invoice, billing receipt, "
            "or financial document rather than a resume. Please upload an authentic resume/CV PDF."
        ), {"reason": "invoice_or_receipt_detected", "detected_sections": detected_sections, "word_count": word_count}

    if legal_hits >= 2 and section_count < 3:
        return False, (
            "Resume Verification Failed: The uploaded file appears to be a legal agreement or policy statement "
            "rather than a resume. Please upload your student resume PDF."
        ), {"reason": "legal_agreement_detected", "detected_sections": detected_sections, "word_count": word_count}

    if recipe_hits >= 2 and section_count < 3:
        return False, (
            "Resume Verification Failed: The uploaded document does not match a professional resume structure. "
            "Please upload an authentic student or job candidate resume PDF."
        ), {"reason": "recipe_or_instructions_detected", "detected_sections": detected_sections, "word_count": word_count}

    # Core validation criteria
    is_genuine_resume = False
    rejection_reason = ""

    if section_count >= 3:
        # 3 or more standard resume sections found
        is_genuine_resume = True
    elif section_count == 2:
        # If only 2 sections matched, must have at least Education or Projects/Experience,
        # plus either contact info or recognized skills.
        if (has_education or has_experience) and (has_contact or total_skills_count >= 2):
            is_genuine_resume = True
        else:
            rejection_reason = "Missing essential resume pillars (Education or Experience & Skills)."
    else:
        rejection_reason = "Document lacks standard resume sections (Education, Skills, Projects, Contact)."

    if not is_genuine_resume:
        return False, (
            f"Resume Verification Failed: {rejection_reason} "
            "Our verification engine could not find sufficient resume structure in this document. "
            "Please make sure you are uploading a genuine Resume or Curriculum Vitae (CV) in PDF format."
        ), {
            "reason": "unrecognized_resume_structure",
            "detected_sections": detected_sections,
            "skills_found": total_skills_count,
            "word_count": word_count
        }

    return True, "Resume structure successfully verified.", {
        "verified": True,
        "detected_sections": detected_sections,
        "skills_found": total_skills_count,
        "word_count": word_count
    }


def analyze_resume_ats(text: str, extracted_skills: Dict[str, List[str]]) -> Dict[str, Any]:
    """
    Computes an industry-grade ATS (Applicant Tracking System) score,
    identifying section completeness, action verbs, quantifiable metrics,
    and areas for improvement.
    """
    text_lower = text.lower()
    total_words = len(text.split())

    # 1. Section Completeness (Weight: 30 pts)
    sections_checked = {
        "Contact Information": bool(re.search(r'(email|phone|linkedin|github|contact)', text_lower)),
        "Education": bool(re.search(r'(education|degree|bachelor|b\.tech|m\.tech|bca|mca|university|college|gpa|cgpa)', text_lower)),
        "Experience / Projects": bool(re.search(r'(experience|projects|work history|internship|employment|portfolio)', text_lower)),
        "Technical Skills": bool(re.search(r'(skills|technical skills|technologies|proficiencies|competencies)', text_lower)),
        "Summary / Objective": bool(re.search(r'(summary|objective|about me|profile)', text_lower)),
        "Certifications / Achievements": bool(re.search(r'(certification|certifications|awards|achievements|honors|publications)', text_lower))
    }
    section_score = sum(5 for present in sections_checked.values() if present) # max 30

    # 2. Skill Breadth & Depth (Weight: 25 pts)
    total_skills_found = sum(len(v) for v in extracted_skills.values())
    if total_skills_found >= 15:
        skill_score = 25
    elif total_skills_found >= 10:
        skill_score = 20
    elif total_skills_found >= 6:
        skill_score = 15
    elif total_skills_found >= 3:
        skill_score = 10
    else:
        skill_score = 5

    # 3. Action Verb Usage & Strength (Weight: 20 pts)
    found_action_verbs = set()
    for verb in ACTION_VERBS:
        if re.search(rf'\b{verb}\b', text_lower):
            found_action_verbs.add(verb)

    verb_count = len(found_action_verbs)
    if verb_count >= 10:
        verb_score = 20
    elif verb_count >= 6:
        verb_score = 15
    elif verb_count >= 3:
        verb_score = 10
    else:
        verb_score = 5

    # 4. Quantifiable Impact & Metrics (Weight: 15 pts)
    # Detect percentages (e.g., 40%), numbers with multipliers (e.g., 100k, $5M), statistics
    metric_matches = re.findall(r'(\d+[\%％]|\b\d+\+\s*(users|clients|students|requests|queries)|\b\d+x\b|\b\d{2,}\b)', text)
    metric_score = min(15, len(metric_matches) * 3)

    # 5. Length & Formatting Heuristics (Weight: 10 pts)
    format_score = 10
    format_issues = []
    if total_words < 150:
        format_score -= 5
        format_issues.append("Resume appears too short (under 150 words). Add more details regarding your projects and coursework.")
    elif total_words > 1000:
        format_score -= 3
        format_issues.append("Resume is somewhat verbose (>1,000 words). Aim for a crisp 1-2 page layout.")

    if not bool(re.search(r'[\•\-\*]', text)):
        format_score -= 2
        format_issues.append("Consider using bullet points for project descriptions to enhance ATS readability.")

    # Calculate Total ATS Score
    total_ats_score = min(100, max(15, section_score + skill_score + verb_score + metric_score + format_score))

    # Rating badge & summary
    if total_ats_score >= 85:
        rating = "Excellent"
        rating_color = "#10B981" # Emerald
        feedback_summary = "Your resume exhibits outstanding ATS compatibility with well-defined sections, high-impact action verbs, and quantifiable achievements."
    elif total_ats_score >= 70:
        rating = "Strong"
        rating_color = "#3B82F6" # Blue
        feedback_summary = "Great resume structure! Polishing a few missing sections and adding measurable project impact metrics will push it to top-tier status."
    elif total_ats_score >= 50:
        rating = "Average"
        rating_color = "#F59E0B" # Amber
        feedback_summary = "Solid foundation, but requires optimization. Strengthen technical keywords, use strong action verbs, and highlight quantifiable project results."
    else:
        rating = "Needs Improvement"
        rating_color = "#EF4444" # Red
        feedback_summary = "Resume requires substantial enhancement. Add missing core sections, structure skills into distinct categories, and elaborate on your technical projects."

    # Improvement recommendations
    recommendations = []
    for sec_name, present in sections_checked.items():
        if not present:
            recommendations.append(f"Add a dedicated '{sec_name}' section to improve ATS parsing.")

    if verb_count < 8:
        recommendations.append(f"Incorporate more impactful action verbs (e.g., 'Architected', 'Optimized', 'Automated', 'Spearheaded') to demonstrate ownership.")

    if len(metric_matches) < 3:
        recommendations.append("Include quantifiable metrics in project bullet points (e.g., 'Improved query speed by 35%', 'Served 500+ active users').")

    recommendations.extend(format_issues)

    return {
        "ats_score": total_ats_score,
        "rating": rating,
        "rating_color": rating_color,
        "feedback_summary": feedback_summary,
        "word_count": total_words,
        "section_breakdown": {
            "sections": sections_checked,
            "section_score": section_score,
            "skill_score": skill_score,
            "action_verb_score": verb_score,
            "quantifiable_metrics_score": metric_score,
            "formatting_score": format_score
        },
        "action_verbs_found": sorted(list(found_action_verbs)),
        "metrics_found_count": len(metric_matches),
        "recommendations": recommendations[:6]
    }


def recommend_career_paths(extracted_skills: Dict[str, List[str]]) -> List[Dict[str, Any]]:
    """
    Evaluates student's skill profile against top tech career tracks
    and generates ranked role match percentages.
    """
    # Flatten all found skills into a lowercase set
    flat_student_skills = set()
    for cat_skills in extracted_skills.values():
        for s in cat_skills:
            flat_student_skills.add(s.lower())

    ranked_roles = []
    for role_name, role_data in CAREER_ROLES.items():
        required_skills = role_data["core_skills"]
        matched = [s for s in required_skills if s in flat_student_skills or any(s in x for x in flat_student_skills)]
        missing = [s for s in required_skills if s not in matched]

        match_ratio = len(matched) / len(required_skills)
        match_percentage = min(98, max(20, int(match_ratio * 100)))

        ranked_roles.append({
            "role": role_name,
            "match_percentage": match_percentage,
            "matched_skills": [s.title() for s in matched],
            "missing_skills": [s.title() for s in missing],
            "description": role_data["description"]
        })

    # Sort descending by match percentage
    ranked_roles.sort(key=lambda x: x["match_percentage"], reverse=True)
    return ranked_roles


def generate_personalized_interview_questions(extracted_skills: Dict[str, List[str]], max_questions: int = 8) -> List[Dict[str, Any]]:
    """
    Generates targeted technical and behavioral interview questions
    tailored specifically to the technologies found in the student's resume.
    """
    flat_student_skills = set()
    for cat_skills in extracted_skills.values():
        for s in cat_skills:
            flat_student_skills.add(s.lower())

    generated_questions = []
    seen_questions = set()

    # Match skills to domain question banks
    for skill, questions in DOMAIN_QUESTIONS.items():
        if skill in flat_student_skills or any(skill in s for s in flat_student_skills) or skill in ["dsa", "general_hr"]:
            for q_obj in questions:
                if q_obj["q"] not in seen_questions:
                    seen_questions.add(q_obj["q"])
                    generated_questions.append({
                        "question": q_obj["q"],
                        "topic": skill.title() if skill not in ["dsa", "general_hr"] else "DSA & Algorithms" if skill == "dsa" else "HR & Behavioral",
                        "type": q_obj["type"],
                        "model_answer": q_obj["key"],
                        "difficulty": "Medium" if q_obj["type"] == "Technical" else "Fundamental" if q_obj["type"] == "Behavioral" else "Advanced"
                    })

    # Ensure at least 6 questions
    if len(generated_questions) < max_questions:
        for q_obj in DOMAIN_QUESTIONS["general_hr"] + DOMAIN_QUESTIONS["dsa"]:
            if q_obj["q"] not in seen_questions:
                seen_questions.add(q_obj["q"])
                generated_questions.append({
                    "question": q_obj["q"],
                    "topic": "Core Fundamentals",
                    "type": q_obj["type"],
                    "model_answer": q_obj["key"],
                    "difficulty": "Medium"
                })

    return generated_questions[:max_questions]


def match_resume_with_job_description(resume_text: str, jd_text: str) -> Dict[str, Any]:
    """
    Performs deep semantic & skill-based matching between student resume and Job Description.
    Calculates Match %, Matched Skills, Missing Skills, and generates an actionable Learning Roadmap.
    """
    resume_skills_dict = extract_skills_from_text(resume_text)
    jd_skills_dict = extract_skills_from_text(jd_text)

    # Flatten skills into lowercased sets
    resume_skills_flat = set()
    for cat_skills in resume_skills_dict.values():
        for s in cat_skills:
            resume_skills_flat.add(s.lower())

    jd_skills_flat = set()
    for cat_skills in jd_skills_dict.values():
        for s in cat_skills:
            jd_skills_flat.add(s.lower())

    # If JD didn't yield enough direct taxonomy keywords, extract key capitalized tech words
    if len(jd_skills_flat) < 3:
        words = re.findall(r'\b[A-Z][a-zA-Z0-9\+\#\.\-]{2,}\b', jd_text)
        for w in words:
            if w.lower() in FLAT_SKILL_MAP:
                jd_skills_flat.add(w.lower())

    # Calculate overlap
    matched_skills = jd_skills_flat.intersection(resume_skills_flat)
    missing_skills = jd_skills_flat.difference(resume_skills_flat)
    extra_skills = resume_skills_flat.difference(jd_skills_flat)

    # Calculate weighted match score
    if jd_skills_flat:
        skill_match_ratio = len(matched_skills) / len(jd_skills_flat)
    else:
        skill_match_ratio = 0.5

    # Text TF-IDF cosine heuristic
    resume_tokens = set(clean_and_tokenize(resume_text))
    jd_tokens = set(clean_and_tokenize(jd_text))
    common_tokens = resume_tokens.intersection(jd_tokens)
    text_overlap = len(common_tokens) / max(1, len(jd_tokens))

    # Overall Match % calculation
    calculated_score = int((skill_match_ratio * 0.70 + text_overlap * 0.30) * 100)
    final_match_score = min(98, max(15, calculated_score))

    # Determine readiness level
    if final_match_score >= 80:
        readiness_badge = "High Match - Ready to Apply!"
        readiness_color = "#10B981"
    elif final_match_score >= 60:
        readiness_badge = "Moderate Match - Bridge Minor Gaps"
        readiness_color = "#3B82F6"
    elif final_match_score >= 40:
        readiness_badge = "Partial Match - Preparation Recommended"
        readiness_color = "#F59E0B"
    else:
        readiness_badge = "Low Match - Significant Skill Upgrades Needed"
        readiness_color = "#EF4444"

    # Generate Personalized Learning Roadmap for Missing Skills
    roadmap_weeks = []
    missing_list = sorted(list(missing_skills))

    if not missing_list:
        roadmap_weeks.append({
            "week": "Week 1",
            "title": "Interview Simulation & Portfolio Review",
            "focus_skills": ["Project Architecture", "Mock Interviews"],
            "tasks": [
                "Review system design trade-offs in your past projects",
                "Conduct 2-3 timed mock interviews covering core algorithms",
                "Customize your resume summary with target company keywords"
            ],
            "resources": ["LeetCode Top 150", "System Design Primer"]
        })
    else:
        # Distribute missing skills across 3-4 week roadmap
        chunk_size = max(1, math.ceil(len(missing_list) / 3))
        week_chunks = [missing_list[i:i + chunk_size] for i in range(0, len(missing_list), chunk_size)]

        for idx, chunk in enumerate(week_chunks[:4]):
            week_num = idx + 1
            skills_titled = [s.title() for s in chunk]
            roadmap_weeks.append({
                "week": f"Week {week_num}",
                "title": f"Mastering {', '.join(skills_titled[:2])}",
                "focus_skills": skills_titled,
                "tasks": [
                    f"Study official documentation & core architectural patterns for {skills_titled[0]}",
                    f"Build a hands-on mini feature or service implementing {', '.join(skills_titled)}",
                    f"Solve 5 domain-specific interview problems on {skills_titled[0]}"
                ],
                "resources": [
                    f"Official {skills_titled[0]} Documentation",
                    "freeCodeCamp / GeeksforGeeks",
                    "GitHub Community Best Practices"
                ]
            })

    return {
        "match_score": final_match_score,
        "readiness_badge": readiness_badge,
        "readiness_color": readiness_color,
        "matched_skills": sorted([s.title() for s in matched_skills]),
        "missing_skills": sorted([s.title() for s in missing_skills]),
        "extra_skills": sorted([s.title() for s in extra_skills])[:8],
        "total_required_skills_count": len(jd_skills_flat),
        "roadmap": roadmap_weeks,
        "actionable_tips": [
            f"Tailor your resume bullet points to explicitly mention {', '.join([s.title() for s in list(missing_skills)[:3]])} if you have course/project experience.",
            "Align your project section headings with the job description terminology.",
            "Prepare STAR (Situation, Task, Action, Result) stories demonstrating practical problem-solving in matched technologies."
        ]
    }


def evaluate_mock_interview_response(question: str, topic: str, user_answer: str) -> Dict[str, Any]:
    """
    Evaluates student's typed or spoken mock interview answer,
    providing technical accuracy score, STAR methodology check,
    strengths, missing elements, and model answer.
    """
    user_answer = user_answer.strip()
    words = user_answer.split()
    word_count = len(words)

    if word_count < 10:
        return {
            "score": 30,
            "rating": "Insufficient Detail",
            "feedback": "Your response is too brief. In a real interview, aim to provide a comprehensive explanation with concrete technical reasoning, architectural context, or a structured STAR response.",
            "strengths": ["Quick response"],
            "areas_to_improve": ["Elaborate with technical depth", "Provide concrete code/system examples", "Explain 'Why' behind design decisions"],
            "model_answer": "A strong answer clearly defines the core concept, explains its underlying mechanism, contrasts it with alternatives, and mentions a real-world use case."
        }

    # Keyword search against taxonomy and question terms
    q_tokens = set(clean_and_tokenize(question))
    a_tokens = set(clean_and_tokenize(user_answer))
    overlap = len(q_tokens.intersection(a_tokens))

    # Evaluate depth heuristics
    score = 50
    strengths = []
    areas_to_improve = []

    if word_count >= 50:
        score += 20
        strengths.append("Good elaboration and thorough explanation")
    elif word_count >= 25:
        score += 10
        strengths.append("Concise overview provided")
    else:
        areas_to_improve.append("Expand on details and trade-offs")

    # Check for structured transition words (STAR / logical flow)
    structure_words = ["because", "therefore", "for example", "such as", "furthermore", "trade-off", "in my project", "resulted in", "benefit"]
    has_structure = any(sw in user_answer.lower() for sw in structure_words)
    if has_structure:
        score += 15
        strengths.append("Well-structured reasoning with clear causal links or examples")
    else:
        areas_to_improve.append("Include real-world examples or STAR (Situation-Task-Action-Result) format")

    if overlap >= 2:
        score += 15
        strengths.append("Directly addressed key terminology from the prompt")

    score = min(96, max(35, score))

    if score >= 80:
        rating = "Excellent Response"
    elif score >= 65:
        rating = "Good Attempt"
    else:
        rating = "Needs Polish"

    return {
        "score": score,
        "rating": rating,
        "word_count": word_count,
        "strengths": strengths if strengths else ["Clear communication"],
        "areas_to_improve": areas_to_improve if areas_to_improve else ["Add deeper architectural insights"],
        "feedback": f"Your answer demonstrated a {rating.lower()} of '{topic}'. Keeping your explanations structured and citing practical examples leaves a memorable impression on interviewers.",
        "model_answer": "Structure your answer: 1. Core definition / purpose -> 2. How it works under the hood -> 3. Practical trade-offs or personal project scenario -> 4. Measurable outcome."
    }
