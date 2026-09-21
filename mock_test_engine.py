"""
AI Career Companion - Adaptive Skill & Certification Mock Test Engine
Fetches live technical questions from online knowledge APIs and generates
personalized 10-15 question mock assessments based on candidate resume skills and certifications.
"""

import random
import requests
import html
import re
from typing import List, Dict, Any, Optional

# Comprehensive technical question bank by skill / certification for instant offline/online synthesis
SKILL_QUESTION_REPOSITORY: Dict[str, List[Dict[str, Any]]] = {
    # --- Python Programming ---
    "python": [
        {
            "question": "What is the key difference between 'is' and '==' in Python?",
            "options": {
                "A": "'is' compares values; '==' compares memory identity",
                "B": "'is' checks memory address identity; '==' checks value equality",
                "C": "'is' is used only for primitive types; '==' for objects",
                "D": "'is' and '==' perform identical operations in Python 3"
            },
            "correct": "B",
            "skill": "Python",
            "difficulty": "Easy",
            "explanation": "'is' evaluates whether two variables point to the exact same object in memory (id(a) == id(b)), whereas '==' evaluates whether the values stored within the objects are equal."
        },
        {
            "question": "In Python, how does the Global Interpreter Lock (GIL) affect multithreading in CPython?",
            "options": {
                "A": "It allows multiple native threads to execute Python bytecodes simultaneously across CPU cores",
                "B": "It restricts execution to only one thread at a time for Python bytecode, impacting CPU-bound tasks",
                "C": "It prevents threads from performing asynchronous I/O operations",
                "D": "It automatically optimizes recursive functions to iterative calls"
            },
            "correct": "B",
            "skill": "Python",
            "difficulty": "Medium",
            "explanation": "The CPython GIL is a mutex that prevents multiple native threads from executing Python bytecodes at once. For CPU-bound tasks, multiprocessing or C-extensions are used instead of threading."
        },
        {
            "question": "What will be the output of [x for x in range(5) if x % 2 == 0] in Python?",
            "options": {
                "A": "[0, 2, 4]",
                "B": "[2, 4]",
                "C": "[1, 3, 5]",
                "D": "[0, 1, 2, 3, 4]"
            },
            "correct": "A",
            "skill": "Python",
            "difficulty": "Easy",
            "explanation": "range(5) yields integers 0, 1, 2, 3, 4. The condition x % 2 == 0 filters out odd numbers, returning list [0, 2, 4]."
        },
        {
            "question": "Which built-in Python keyword is used to create a generator object that produces values lazily on demand?",
            "options": {
                "A": "return",
                "B": "yield",
                "C": "async def",
                "D": "lambda"
            },
            "correct": "B",
            "skill": "Python",
            "difficulty": "Easy",
            "explanation": "'yield' suspends the function execution and sends a value back to the caller, maintaining enough state to resume where it left off."
        }
    ],

    # --- Java & OOP ---
    "java": [
        {
            "question": "In Java, what is the fundamental difference between String, StringBuilder, and StringBuffer?",
            "options": {
                "A": "String is mutable; StringBuilder and StringBuffer are immutable",
                "B": "String is immutable; StringBuilder is mutable (non-thread-safe); StringBuffer is mutable and thread-safe (synchronized)",
                "C": "StringBuffer is faster than StringBuilder because it is not synchronized",
                "D": "String cannot be stored in heap memory"
            },
            "correct": "B",
            "skill": "Java",
            "difficulty": "Medium",
            "explanation": "String objects are immutable. StringBuilder is mutable and faster for single-threaded operations. StringBuffer contains synchronized methods making it thread-safe."
        },
        {
            "question": "Which OOP principle ensures that a subclass can substitute its superclass without breaking client code?",
            "options": {
                "A": "Single Responsibility Principle (SRP)",
                "B": "Liskov Substitution Principle (LSP)",
                "C": "Interface Segregation Principle (ISP)",
                "D": "Dependency Inversion Principle (DIP)"
            },
            "correct": "B",
            "skill": "OOP / Java",
            "difficulty": "Medium",
            "explanation": "LSP states that objects of a superclass should be replaceable with objects of its subclasses without altering the correctness of the program."
        },
        {
            "question": "In Java's memory model, where are local primitive variables and method call frames stored versus object instances?",
            "options": {
                "A": "Primitive locals on Stack; Object instances on Heap",
                "B": "Primitive locals on Heap; Object instances on Stack",
                "C": "Both are stored exclusively in Metaspace",
                "D": "Both are stored in PermGen memory"
            },
            "correct": "A",
            "skill": "Java",
            "difficulty": "Medium",
            "explanation": "Local variables inside methods reside on Thread Stack. All object instances and arrays are allocated on the Heap."
        }
    ],

    # --- Data Structures & Algorithms ---
    "dsa": [
        {
            "question": "What is the worst-case time complexity of searching an element in a balanced Red-Black Tree or AVL Tree?",
            "options": {
                "A": "O(1)",
                "B": "O(log N)",
                "C": "O(N)",
                "D": "O(N log N)"
            },
            "correct": "B",
            "skill": "DSA",
            "difficulty": "Easy",
            "explanation": "Balanced binary search trees guarantee that tree height stays bounded by O(log N), ensuring lookup, insertion, and deletion run in worst-case O(log N) time."
        },
        {
            "question": "Which data structure is optimal for implementing an LRU (Least Recently Used) Cache with O(1) get and put operations?",
            "options": {
                "A": "Binary Heap + Array",
                "B": "Doubly Linked List + Hash Map",
                "C": "Singly Linked List + Binary Search Tree",
                "D": "Stack + Queue"
            },
            "correct": "B",
            "skill": "DSA",
            "difficulty": "Medium",
            "explanation": "A Hash Map provides O(1) key lookup to node references, and a Doubly Linked List allows O(1) removal and re-insertion of recently accessed nodes at the head."
        },
        {
            "question": "What is the primary advantage of Kadane's Algorithm for the Maximum Subarray Problem?",
            "options": {
                "A": "Kadane runs in O(N) linear time and O(1) space, while Divide & Conquer runs in O(N log N) time",
                "B": "Kadane works only with positive numbers",
                "C": "Kadane requires O(N) auxiliary memory",
                "D": "Kadane computes all permutations explicitly"
            },
            "correct": "A",
            "skill": "DSA",
            "difficulty": "Medium",
            "explanation": "Kadane's dynamic programming approach solves maximum contiguous subarray sum in a single O(N) pass with O(1) space."
        },
        {
            "question": "In a directed graph, which algorithm determines the topological ordering of vertices and detects cycles in O(V + E) time?",
            "options": {
                "A": "Dijkstra's Algorithm",
                "B": "Kahn's Algorithm (BFS with In-degrees) or DFS with recursion stack tracking",
                "C": "Prim's Algorithm",
                "D": "Floyd-Warshall Algorithm"
            },
            "correct": "B",
            "skill": "DSA",
            "difficulty": "Medium",
            "explanation": "Kahn's algorithm tracks vertex in-degrees. If the number of processed vertices in topological order is less than |V|, a cycle is detected."
        }
    ],

    # --- React & Frontend ---
    "react": [
        {
            "question": "In React, what is the purpose of the useEffect hook's cleanup return function?",
            "options": {
                "A": "To re-render child components when parent state changes",
                "B": "To cancel network subscriptions, timers, or event listeners before unmounting or re-running",
                "C": "To update state directly without triggering a re-render",
                "D": "To force garbage collection of DOM elements"
            },
            "correct": "B",
            "skill": "React",
            "difficulty": "Easy",
            "explanation": "The cleanup function returned inside useEffect runs before unmounting and before subsequent effect executions to prevent memory leaks."
        },
        {
            "question": "What is the Virtual DOM in React and why does it enhance performance?",
            "options": {
                "A": "It is an exact replica of browser memory that replaces HTML",
                "B": "It is a lightweight JavaScript representation of real DOM used for diffing and batching updates",
                "C": "It is a server-side compiler that converts CSS to WebAssembly",
                "D": "It executes code directly in the browser kernel"
            },
            "correct": "B",
            "skill": "React / Web",
            "difficulty": "Medium",
            "explanation": "React maintains an in-memory Virtual DOM. When state changes, it computes the minimal diff between trees and batches updates to the real DOM."
        },
        {
            "question": "Which React hook should you use to memoize an expensive calculated value across renders unless dependencies change?",
            "options": {
                "A": "useCallback",
                "B": "useMemo",
                "C": "useRef",
                "D": "useReducer"
            },
            "correct": "B",
            "skill": "React",
            "difficulty": "Easy",
            "explanation": "useMemo memoizes the result of an expensive calculation, whereas useCallback memoizes the callback function definition itself."
        }
    ],

    # --- JavaScript & TypeScript ---
    "javascript": [
        {
            "question": "What is the output of typeof null and typeof NaN in JavaScript?",
            "options": {
                "A": "'null' and 'nan'",
                "B": "'object' and 'number'",
                "C": "'undefined' and 'number'",
                "D": "'object' and 'undefined'"
            },
            "correct": "B",
            "skill": "JavaScript",
            "difficulty": "Easy",
            "explanation": "In JavaScript, typeof null === 'object' due to early language implementation history. NaN stands for Not-a-Number, but its type is 'number'."
        },
        {
            "question": "In JavaScript Event Loop, how are Microtasks (Promise.then) prioritized against Macrotasks (setTimeout)?",
            "options": {
                "A": "Macrotasks execute before pending microtasks",
                "B": "All microtasks in the microtask queue are drained completely before the next macrotask is processed",
                "C": "Microtasks and macrotasks alternate 1-to-1",
                "D": "Promises run in separate background OS threads"
            },
            "correct": "B",
            "skill": "JavaScript",
            "difficulty": "Medium",
            "explanation": "After each macrotask completes, JavaScript exhausts all jobs in the Microtask queue before picking the next macrotask."
        },
        {
            "question": "What is the key difference between TypeScript interface and type alias?",
            "options": {
                "A": "Interface supports declaration merging; type alias cannot be reopened for declaration merging",
                "B": "Type alias only supports string literals; interface supports objects",
                "C": "Interface compiles directly into runtime JavaScript code",
                "D": "Type aliases cannot define union types"
            },
            "correct": "A",
            "skill": "TypeScript",
            "difficulty": "Medium",
            "explanation": "TypeScript interfaces support declaration merging where multiple declarations combine their members. Type aliases cannot be reopened."
        }
    ],

    # --- SQL & Databases ---
    "sql": [
        {
            "question": "What is the difference between INNER JOIN, LEFT JOIN, and FULL OUTER JOIN in SQL?",
            "options": {
                "A": "INNER JOIN returns matching rows in both; LEFT JOIN returns all left rows plus matched right; FULL OUTER returns all rows from both tables",
                "B": "LEFT JOIN filters out NULL values from left table",
                "C": "INNER JOIN returns duplicates while LEFT JOIN removes duplicates",
                "D": "FULL OUTER JOIN only works on primary keys"
            },
            "correct": "A",
            "skill": "SQL / Databases",
            "difficulty": "Easy",
            "explanation": "INNER JOIN returns matched records. LEFT JOIN returns all left records and matched right records. FULL OUTER JOIN returns all rows from both tables."
        },
        {
            "question": "In database ACID properties, what does 'Isolation' guarantee?",
            "options": {
                "A": "Data changes are permanently written to disk",
                "B": "Concurrent transactions execute independently without interfering with intermediate state",
                "C": "All operations in a transaction either complete entirely or roll back completely",
                "D": "Data schema conforms strictly to 3NF"
            },
            "correct": "B",
            "skill": "DBMS",
            "difficulty": "Medium",
            "explanation": "Isolation ensures concurrent transactions result in a state that would be obtained if transactions executed sequentially."
        },
        {
            "question": "What data structure is most widely used by default in MySQL InnoDB and PostgreSQL for indexing?",
            "options": {
                "A": "Hash Index",
                "B": "B+ Tree Index",
                "C": "R-Tree Spatial Index",
                "D": "Inverted Full-Text Index"
            },
            "correct": "B",
            "skill": "Databases",
            "difficulty": "Medium",
            "explanation": "B+ Trees store records at leaf nodes linked sequentially, optimizing both point lookups and range scans."
        }
    ],

    # --- Cloud & DevOps ---
    "cloud": [
        {
            "question": "In Docker containerization, what is the fundamental difference between an Image and a Container?",
            "options": {
                "A": "An image is a running process; a container is a read-only template",
                "B": "An image is an immutable read-only template; a container is a running instance with a writable layer",
                "C": "A container includes a full guest OS kernel; an image does not",
                "D": "Docker images only run on Linux servers"
            },
            "correct": "B",
            "skill": "Docker / DevOps",
            "difficulty": "Easy",
            "explanation": "A Docker Image is an immutable snapshot with instructions. A container is a live instance with an added read-write layer."
        },
        {
            "question": "In Kubernetes, which controller ensures that a specified number of identical pod replicas are running at all times?",
            "options": {
                "A": "Ingress Controller",
                "B": "ReplicaSet / Deployment Controller",
                "C": "Kubelet Service Daemon",
                "D": "ConfigMap Manager"
            },
            "correct": "B",
            "skill": "Kubernetes / Cloud",
            "difficulty": "Medium",
            "explanation": "A Deployment manages ReplicaSets, which maintain the desired count of replica Pods running across the cluster."
        },
        {
            "question": "In AWS Cloud Architecture, which storage service provides scalable object storage accessed via HTTP/REST APIs with 99.999999999% (11 9's) durability?",
            "options": {
                "A": "Amazon EBS",
                "B": "Amazon S3",
                "C": "Amazon EFS",
                "D": "Amazon RDS"
            },
            "correct": "B",
            "skill": "AWS / Cloud",
            "difficulty": "Easy",
            "explanation": "Amazon S3 is an object storage service designed to store and protect data with 11 9's durability."
        },
        {
            "question": "In CI/CD automation, what is the distinction between Continuous Delivery and Continuous Deployment?",
            "options": {
                "A": "Continuous Delivery requires manual approval before releasing to production; Continuous Deployment automates release without human intervention",
                "B": "Continuous Delivery runs unit tests; Continuous Deployment does not",
                "C": "Continuous Deployment applies only to mobile apps",
                "D": "Continuous Delivery requires Docker; Continuous Deployment requires Kubernetes"
            },
            "correct": "A",
            "skill": "CI/CD / DevOps",
            "difficulty": "Medium",
            "explanation": "In Continuous Delivery, code changes are automatically tested and staged for manual 1-click release. In Continuous Deployment, validated changes deploy to production automatically."
        }
    ],

    # --- AI, Machine Learning & Data Science ---
    "ai_ml": [
        {
            "question": "In Machine Learning classification, what does the ROC-AUC score measure?",
            "options": {
                "A": "The training loss curve convergence speed",
                "B": "The model's ability to distinguish between positive and negative classes across all decision thresholds",
                "C": "The exact mean squared error between predictions and target labels",
                "D": "The percentage of outliers in the dataset"
            },
            "correct": "B",
            "skill": "Machine Learning",
            "difficulty": "Medium",
            "explanation": "ROC-AUC evaluates how well the classifier ranks positive instances higher than negative instances across all decision thresholds."
        },
        {
            "question": "What is the primary purpose of the Self-Attention mechanism in Transformer architectures?",
            "options": {
                "A": "To compress image resolutions in convolutional layers",
                "B": "To dynamically weight contextual relationships of each token with every other token in the sequence in parallel",
                "C": "To replace backpropagation with genetic algorithms",
                "D": "To enforce strict sequential token processing"
            },
            "correct": "B",
            "skill": "Deep Learning / NLP",
            "difficulty": "Hard",
            "explanation": "Self-attention computes Query-Key-Value interactions, allowing the model to attend to relevant tokens across the entire context window in parallel."
        },
        {
            "question": "What technique is commonly used to prevent overfitting in Deep Neural Networks by randomly deactivating neuron activations during training?",
            "options": {
                "A": "Batch Normalization",
                "B": "Dropout Regularization",
                "C": "Gradient Clipping",
                "D": "Learning Rate Decay"
            },
            "correct": "B",
            "skill": "Deep Learning",
            "difficulty": "Easy",
            "explanation": "Dropout randomly deactivates a fraction of neurons during training, preventing co-adaptation of features."
        }
    ],

    # --- Certifications (AWS Certified, Azure, Meta, Python Institute) ---
    "certifications": [
        {
            "question": "[AWS Certified Solutions Architect] Which AWS service should be used to decouple components of a distributed microservices architecture asynchronously?",
            "options": {
                "A": "AWS Direct Connect",
                "B": "Amazon SQS (Simple Queue Service) or Amazon SNS",
                "C": "Amazon Route 53",
                "D": "AWS IAM"
            },
            "correct": "B",
            "skill": "AWS Certification",
            "difficulty": "Medium",
            "explanation": "Amazon SQS provides secure, scalable message queuing that decouples microservice components, enabling asynchronous communication."
        },
        {
            "question": "[Azure Fundamentals / Developer] In Microsoft Azure, what provides serverless event-driven compute without provisioning virtual machines?",
            "options": {
                "A": "Azure Virtual Machines (IaaS)",
                "B": "Azure Functions",
                "C": "Azure ExpressRoute",
                "D": "Azure Blob Storage"
            },
            "correct": "B",
            "skill": "Azure Certification",
            "difficulty": "Easy",
            "explanation": "Azure Functions is an event-driven serverless compute service that executes code in response to HTTP requests, queues, or timers."
        },
        {
            "question": "[Python Institute / PCAP Certified] What exception is raised in Python when attempting to access a dictionary key that does not exist?",
            "options": {
                "A": "IndexError",
                "B": "KeyError",
                "C": "ValueError",
                "D": "AttributeError"
            },
            "correct": "B",
            "skill": "Python Certification",
            "difficulty": "Easy",
            "explanation": "Accessing a missing key via dict[key] raises KeyError. Using dict.get(key) returns None or a default value instead."
        }
    ]
}


def fetch_online_opentdb_questions(count: int = 5) -> List[Dict[str, Any]]:
    """
    Fetches live verified computer science questions from Open Trivia DB / Online API.
    Category 18 = Science: Computers
    """
    url = f"https://opentdb.com/api.php?amount={count}&category=18&type=multiple"
    online_questions = []

    try:
        resp = requests.get(url, timeout=3.5)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("response_code") == 0 and "results" in data:
                for idx, item in enumerate(data["results"]):
                    q_text = html.unescape(item.get("question", ""))
                    correct_ans = html.unescape(item.get("correct_answer", ""))
                    incorrect_answers = [html.unescape(ans) for ans in item.get("incorrect_answers", [])]

                    # Shuffle and map to A, B, C, D
                    all_options = incorrect_answers + [correct_ans]
                    random.shuffle(all_options)

                    correct_letter = "A"
                    options_dict = {}
                    letters = ["A", "B", "C", "D"]
                    for i, opt in enumerate(all_options[:4]):
                        letter = letters[i]
                        options_dict[letter] = opt
                        if opt == correct_ans:
                            correct_letter = letter

                    diff = item.get("difficulty", "medium").title()
                    online_questions.append({
                        "question": q_text,
                        "options": options_dict,
                        "correct": correct_letter,
                        "skill": "Computer Science & IT (Live Web)",
                        "difficulty": diff,
                        "explanation": f"The correct answer is '{correct_ans}'. This question was fetched live from online technical assessment repositories."
                    })
    except Exception as e:
        print(f"[Online Tech Questions Fetch Note]: {e}")

    return online_questions


def generate_tailored_mock_test(
    skills: Optional[List[str]] = None,
    certifications: Optional[List[str]] = None,
    target_role: Optional[str] = None,
    difficulty: str = "all",
    count: int = 12
) -> List[Dict[str, Any]]:
    """
    Generates an adaptive, skill-tailored 10-15 question technical mock test.
    Combines candidate resume skills, certifications, online tech questions, and core CS assessment pools.
    """
    # Enforce 10-15 questions requirement
    count = max(10, min(15, int(count or 12)))

    skills = [s.strip().lower() for s in (skills or []) if s.strip()]
    certifications = [c.strip().lower() for c in (certifications or []) if c.strip()]
    target_role = (target_role or "Software Engineer").lower()

    selected_pool: List[Dict[str, Any]] = []

    # Map candidate skills to question categories
    skill_category_map = {
        "python": "python",
        "django": "python",
        "flask": "python",
        "fastapi": "python",
        "java": "java",
        "spring": "java",
        "spring boot": "java",
        "dsa": "dsa",
        "data structures": "dsa",
        "algorithms": "dsa",
        "c++": "dsa",
        "react": "react",
        "react.js": "react",
        "next.js": "react",
        "javascript": "javascript",
        "typescript": "javascript",
        "node.js": "javascript",
        "sql": "sql",
        "mysql": "sql",
        "postgresql": "sql",
        "dbms": "sql",
        "aws": "cloud",
        "docker": "cloud",
        "kubernetes": "cloud",
        "ci/cd": "cloud",
        "azure": "cloud",
        "machine learning": "ai_ml",
        "deep learning": "ai_ml",
        "ai": "ai_ml",
        "data science": "ai_ml"
    }

    matched_categories = set()
    for s in skills:
        for key, cat in skill_category_map.items():
            if key in s:
                matched_categories.add(cat)

    if certifications or "certified" in target_role or "aws" in " ".join(skills):
        matched_categories.add("certifications")

    # If no specific category matched, default to balanced core tech set
    if not matched_categories:
        matched_categories = {"dsa", "python", "javascript", "sql", "cloud"}

    # 1. Gather skill-tailored questions
    for cat in matched_categories:
        if cat in SKILL_QUESTION_REPOSITORY:
            selected_pool.extend(SKILL_QUESTION_REPOSITORY[cat])

    # 2. Fetch live online questions from internet (OpenTDB Computer Science)
    online_count = min(5, max(3, count // 3))
    online_qs = fetch_online_opentdb_questions(count=online_count)
    selected_pool.extend(online_qs)

    # 3. If pool is smaller than required count, add all remaining categories
    for cat, qs in SKILL_QUESTION_REPOSITORY.items():
        if len(selected_pool) >= count * 2:
            break
        selected_pool.extend(qs)

    # 4. Filter by difficulty if requested
    if difficulty.lower() in ["easy", "medium", "hard"]:
        filtered = [q for q in selected_pool if q.get("difficulty", "").lower() == difficulty.lower()]
        if len(filtered) >= count:
            selected_pool = filtered

    # Shuffle and pick exactly count questions
    random.shuffle(selected_pool)
    final_questions = selected_pool[:count]

    # Format output with unique IDs and standard structure
    formatted_output = []
    for idx, q in enumerate(final_questions, 1):
        formatted_output.append({
            "id": idx,
            "question": q["question"],
            "options": q["options"],
            "correct_option": q["correct"],
            "skill_tag": q.get("skill", "General Tech"),
            "difficulty": q.get("difficulty", "Medium"),
            "explanation": q.get("explanation", "The selected option correctly applies core technical principles.")
        })

    return formatted_output
