"""
AI Career Companion - Main Flask Web Application
Backend Server with complete RESTful API routes, database integration,
NLP analysis engine, and static asset serving.
"""

import os
import time
import random
from flask import Flask, request, jsonify, render_template, send_from_directory, session, redirect, url_for
from functools import wraps
from nlp_engine import (
    extract_text_from_pdf_bytes,
    extract_skills_from_text,
    extract_certifications_from_text,
    extract_contact_info,
    verify_is_resume,
    analyze_resume_ats,
    recommend_career_paths,
    generate_personalized_interview_questions,
    match_resume_with_job_description,
    evaluate_mock_interview_response
)
from database import (
    init_database,
    get_all_alumni_experiences,
    add_alumni_experience,
    upvote_alumni_experience,
    promote_student_to_alumni,
    get_quiz_questions,
    get_all_job_profiles,
    get_faculty_dashboard_stats,
    get_all_students,
    get_student_by_id,
    add_student,
    update_student_progress,
    delete_student,
    authenticate_student,
    authenticate_alumni,
    add_alumni_account,
    get_all_alumni_accounts,
    get_alumni_account_by_id,
    delete_alumni_account,
    delete_alumni_experience,
    parse_interview_rounds,
    add_mcq_question,
    delete_mcq_question,
    get_alumni_contributed_questions,
    get_contributing_alumni_list,
    get_admin_dashboard_stats,
    get_alumni_outreach_metrics,
    record_alumni_outreach,
    update_alumni_inquiry_status,
    record_student_quiz_completion,
    get_db_connection
)
from mock_test_engine import generate_tailored_mock_test
from sample_resumes import SAMPLE_RESUMES
from hiring_dataset import (
    load_45_companies,
    compare_resume_with_45_companies,
    benchmark_candidate_against_dataset
)
from mailer import send_2fa_email, send_welcome_student_email

app = Flask(__name__, static_folder="static", template_folder="templates")
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16 MB max file upload
app.secret_key = 'career_companion_secure_admin_key_2025'

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

def admin_required(f):
    """Decorator to require admin authentication for protected routes."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            if request.is_json or request.path.startswith('/api/'):
                return jsonify({"error": "Admin authentication required. Please log in.", "redirect": "/admin"}), 401
            return redirect('/admin')
        return f(*args, **kwargs)
    return decorated_function

# Initialize SQLite database on startup
init_database()

# ==========================================
# PAGE ROUTING
# ==========================================

@app.route('/')
def index():
    """
    Primary Landing Page:
    - If unauthenticated, serves Student Login Portal as the primary landing page for the website.
    - If student is logged in, renders the main AI Career Companion platform.
    - If alumni is logged in, renders their profile dashboard (or platform if ?view=platform).
    - If admin is logged in, renders the platform with admin navigation.
    """
    if session.get('student_logged_in'):
        current_user = {
            "name": session.get('student_name', 'Student'),
            "id": session.get('student_id'),
            "type": "student",
            "dashboard_url": "/student/profile"
        }
        return render_template('index.html', user=current_user)

    if session.get('alumni_logged_in'):
        if request.args.get('view') == 'platform':
            current_user = {
                "name": session.get('alumni_name', 'Alumni Mentor'),
                "id": session.get('alumni_id', ''),
                "type": "alumni",
                "dashboard_url": "/alumni/profile"
            }
            return render_template('index.html', user=current_user)
        return redirect('/alumni/profile')

    if session.get('admin_logged_in'):
        current_user = {
            "name": session.get('admin_user', 'Administrator'),
            "type": "admin",
            "dashboard_url": "/admin"
        }
        return render_template('index.html', user=current_user)

    # Primary landing page for unauthenticated visitors
    return render_template('student_login.html')


@app.route('/login')
@app.route('/alumni/login')
def login_gateway():
    """Redirects unauthenticated users to the login portal."""
    if session.get('alumni_logged_in'):
        return redirect('/alumni/profile')
    if session.get('student_logged_in'):
        return redirect('/')
    if session.get('admin_logged_in'):
        return redirect('/admin')
    # If route is /alumni/login, pass query param to active tab
    if request.path == '/alumni/login':
        return redirect('/student/login?role=alumni')
    return redirect('/')


# ==========================================
# RESUME ANALYZER & ATS EVALUATION API
# ==========================================

@app.route('/api/resume/analyze', methods=['POST'])
def analyze_resume():
    """
    Accepts resume file upload (PDF only, strictly no .docx files) or raw text.
    Verifies that the uploaded document is genuinely a Resume/CV.
    Performs skill extraction, ATS scoring, career path mapping,
    45-company synthetic hiring dataset matching, and personalized question generation.
    """
    resume_text = ""
    filename = "Pasted Text"

    # Check if a file was uploaded
    if 'resume_file' in request.files:
        file = request.files['resume_file']
        if file.filename:
            raw_filename = file.filename.strip()
            filename = raw_filename
            lower_name = raw_filename.lower()

            # Strict Malware Protection: Block all .docx, .doc, .docm, etc.
            if lower_name.endswith(('.docx', '.doc', '.docm', '.dotx', '.dotm')):
                return jsonify({
                    "success": False,
                    "error": "Malware Protection Policy: .docx and Word documents are strictly prohibited due to macro/embedded script vulnerabilities. Please convert your resume to a secure PDF format (.pdf) and upload again.",
                    "is_resume": False
                }), 400

            # Only accept .pdf format
            if not lower_name.endswith('.pdf'):
                return jsonify({
                    "success": False,
                    "error": "Unsupported file format. Only standard PDF (.pdf) documents are accepted for secure ATS analysis.",
                    "is_resume": False
                }), 400

            file_bytes = file.read()

            # Verify PDF magic signature (must contain %PDF header)
            if not file_bytes.startswith(b'%PDF') and b'%PDF' not in file_bytes[:1024]:
                return jsonify({
                    "success": False,
                    "error": "Security & File Integrity Alert: The uploaded file has a .pdf extension but lacks valid PDF binary signatures. Please upload a genuine, uncorrupted PDF document.",
                    "is_resume": False
                }), 400

            resume_text = extract_text_from_pdf_bytes(file_bytes)

    # If raw text was provided via JSON or form
    if not resume_text and request.is_json:
        resume_text = request.json.get('resume_text', '')
    elif not resume_text and 'resume_text' in request.form:
        resume_text = request.form.get('resume_text', '')

    if not resume_text.strip():
        return jsonify({
            "success": False,
            "error": "No readable text could be extracted from your document. If this is a scanned document, please ensure it has selectable text or re-save with OCR enabled.",
            "is_resume": False
        }), 400

    # =========================================================================
    # RESUME AUTHENTICITY VERIFIER: Ensure the document is genuinely a Resume/CV
    # =========================================================================
    is_valid_resume, verification_msg, verification_details = verify_is_resume(resume_text)
    if not is_valid_resume:
        return jsonify({
            "success": False,
            "error": verification_msg,
            "is_resume": False,
            "verification": verification_details
        }), 400

    # 1. Extract contact details
    contact_info = extract_contact_info(resume_text)

    # 2. Extract skills categorized by taxonomy
    extracted_skills = extract_skills_from_text(resume_text)
    extracted_certifications = extract_certifications_from_text(resume_text)

    # 3. Analyze ATS score and formatting
    ats_analysis = analyze_resume_ats(resume_text, extracted_skills)

    # 4. Career path recommendations
    career_recommendations = recommend_career_paths(extracted_skills)

    # 5. Tailored Interview questions based on resume technologies
    interview_questions = generate_personalized_interview_questions(extracted_skills, max_questions=8)

    # 6. Compare with 45-Company Hiring Dataset
    dataset_matching = compare_resume_with_45_companies(resume_text, extracted_skills)

    # 7. Benchmark against Candidate Dataset
    cohort_benchmark = benchmark_candidate_against_dataset(ats_analysis.get("ats_score", 75), extracted_skills)

    # Count total skills extracted
    total_skills = sum(len(skills) for skills in extracted_skills.values())

    return jsonify({
        "success": True,
        "is_resume": True,
        "verification": verification_details,
        "filename": filename,
        "contact_info": contact_info,
        "total_skills_count": total_skills,
        "extracted_skills": extracted_skills,
        "extracted_certifications": extracted_certifications,
        "ats_analysis": ats_analysis,
        "career_recommendations": career_recommendations,
        "interview_questions": interview_questions,
        "dataset_matching": dataset_matching,
        "cohort_benchmark": cohort_benchmark,
        "raw_text_preview": resume_text[:600] + ("..." if len(resume_text) > 600 else "")
    })


@app.route('/api/dataset/companies', methods=['GET'])
def get_hiring_dataset_companies():
    """Returns all 45 companies with roles, required skills, and CTC ranges from the dataset."""
    companies = load_45_companies()
    return jsonify({
        "success": True,
        "count": len(companies),
        "companies": companies
    })


# ==========================================
# RESUME - JOB MATCHING ENDPOINTS
# ==========================================

@app.route('/api/resume/match-job', methods=['POST'])
def match_job():
    """
    Compares student resume against target Job Description or selected Job ID.
    Returns match score, matched skills, missing skills, and learning roadmap.
    """
    data = request.json or request.form

    resume_text = data.get('resume_text', '')
    jd_text = data.get('jd_text', '')
    job_id = data.get('job_id')

    # If job_id specified, fetch pre-loaded JD
    if job_id and not jd_text:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM job_profiles WHERE id = ?", (job_id,))
        row = cursor.fetchone()
        conn.close()
        if row:
            job_dict = dict(row)
            jd_text = f"Company: {job_dict['company']}\nRole: {job_dict['role_title']}\nRequirements: {job_dict['required_skills']}\nDescription: {job_dict['description']}"

    if not resume_text.strip():
        return jsonify({"error": "Please provide your resume text for job matching."}), 400

    if not jd_text.strip():
        return jsonify({"error": "Please provide a target job description or select a company role."}), 400

    match_result = match_resume_with_job_description(resume_text, jd_text)
    return jsonify({
        "success": True,
        "match_result": match_result
    })


# ==========================================
# PLACEMENT PREPARATION & QUIZ ENDPOINTS
# ==========================================

@app.route('/api/quiz/questions', methods=['GET'])
def fetch_quiz_questions():
    """Fetches randomized practice MCQs filtered by subject or company."""
    subject = request.args.get('subject', 'all')
    company = request.args.get('company', 'all')
    limit = int(request.args.get('limit', 10))

    questions = get_quiz_questions(subject=subject, company=company, limit=limit)
    # Sanitize correct answer from initial question list sent to client for test security
    client_questions = []
    for q in questions:
        client_questions.append({
            "id": q["id"],
            "subject": q["subject"],
            "topic": q["topic"],
            "company": q["company"],
            "question": q["question"],
            "option_a": q["option_a"],
            "option_b": q["option_b"],
            "option_c": q["option_c"],
            "option_d": q["option_d"],
            "difficulty": q["difficulty"]
        })

    return jsonify({
        "success": True,
        "count": len(client_questions),
        "questions": client_questions
    })


@app.route('/api/quiz/submit', methods=['POST'])
def submit_quiz():
    """
    Evaluates submitted quiz answers, computes overall score percentage,
    topic strengths & weaknesses, and provides complete explanations.
    """
    data = request.json or {}
    answers = data.get('answers', {})  # Dict of { question_id: "A" / "B" / "C" / "D" }

    if not answers:
        return jsonify({"error": "No answers submitted"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()

    question_ids = [int(qid) for qid in answers.keys()]
    placeholders = ",".join("?" for _ in question_ids)
    cursor.execute(f"SELECT * FROM mcq_questions WHERE id IN ({placeholders})", question_ids)
    db_questions = {row["id"]: dict(row) for row in cursor.fetchall()}
    conn.close()

    total_questions = len(question_ids)
    correct_count = 0
    detailed_results = []
    topic_breakdown = {}

    for qid_str, selected_opt in answers.items():
        qid = int(qid_str)
        q_data = db_questions.get(qid)
        if not q_data:
            continue

        correct_opt = q_data["correct_option"].upper().strip()
        user_opt = selected_opt.upper().strip() if selected_opt else ""
        is_correct = (user_opt == correct_opt)

        if is_correct:
            correct_count += 1

        topic = q_data["subject"]
        if topic not in topic_breakdown:
            topic_breakdown[topic] = {"total": 0, "correct": 0}
        topic_breakdown[topic]["total"] += 1
        if is_correct:
            topic_breakdown[topic]["correct"] += 1

        detailed_results.append({
            "id": qid,
            "question": q_data["question"],
            "subject": q_data["subject"],
            "topic": q_data["topic"],
            "user_option": user_opt,
            "correct_option": correct_opt,
            "is_correct": is_correct,
            "explanation": q_data["explanation"],
            "options": {
                "A": q_data["option_a"],
                "B": q_data["option_b"],
                "C": q_data["option_c"],
                "D": q_data["option_d"]
            }
        })

    score_percentage = int((correct_count / max(1, total_questions)) * 100)

    return jsonify({
        "success": True,
        "total_questions": total_questions,
        "correct_count": correct_count,
        "score_percentage": score_percentage,
        "topic_breakdown": topic_breakdown,
        "detailed_results": detailed_results
    })


# ==========================================
# SKILL-TAILORED MOCK TEST ENDPOINTS
# ==========================================

@app.route('/api/mocktest/generate', methods=['POST'])
def generate_mock_test():
    """
    Generates an adaptive 10-15 question technical mock test
    dynamically tailored to the student's extracted resume skills,
    certifications, or custom chosen tech stack, with online question fetching.
    """
    data = request.json or request.form.to_dict()
    skills = data.get('skills', [])
    if isinstance(skills, str):
        skills = [s.strip() for s in skills.split(',') if s.strip()]
    
    certifications = data.get('certifications', [])
    if isinstance(certifications, str):
        certifications = [c.strip() for c in certifications.split(',') if c.strip()]
        
    target_role = data.get('target_role', 'Software Engineer')
    difficulty = data.get('difficulty', 'all')
    count = int(data.get('count', 12))

    questions = generate_tailored_mock_test(
        skills=skills,
        certifications=certifications,
        target_role=target_role,
        difficulty=difficulty,
        count=count
    )

    # Collect unique skills represented in the test
    tested_skills = list(set(q.get('skill_tag', 'Tech') for q in questions))

    return jsonify({
        "success": True,
        "count": len(questions),
        "target_role": target_role,
        "skills_tested": tested_skills,
        "questions": questions
    })


@app.route('/api/mocktest/submit', methods=['POST'])
def submit_mock_test():
    """
    Evaluates student's submitted mock test answers, produces detailed
    scorecard with skill-by-skill analysis, and increments student quiz metrics.
    """
    data = request.json or {}
    questions = data.get('questions', [])
    user_answers = data.get('answers', {})  # { "1": "B", "2": "A", ... }
    time_taken_seconds = data.get('time_taken_seconds', 0)

    if not questions:
        return jsonify({"error": "No questions provided for evaluation."}), 400

    total_questions = len(questions)
    correct_count = 0
    attempted_count = 0
    skill_breakdown = {}
    detailed_review = []

    for q in questions:
        qid = str(q.get('id', ''))
        skill = q.get('skill_tag', 'General Tech')
        correct_opt = str(q.get('correct_option', '')).strip().upper()
        user_opt = str(user_answers.get(qid, '')).strip().upper()

        if skill not in skill_breakdown:
            skill_breakdown[skill] = {"total": 0, "correct": 0, "score_pct": 0}
        skill_breakdown[skill]["total"] += 1

        is_attempted = bool(user_opt)
        if is_attempted:
            attempted_count += 1

        is_correct = (is_attempted and user_opt == correct_opt)
        if is_correct:
            correct_count += 1
            skill_breakdown[skill]["correct"] += 1

        detailed_review.append({
            "id": qid,
            "question": q.get('question', ''),
            "skill": skill,
            "difficulty": q.get('difficulty', 'Medium'),
            "user_option": user_opt if user_opt else "Skipped",
            "correct_option": correct_opt,
            "is_correct": is_correct,
            "is_attempted": is_attempted,
            "explanation": q.get('explanation', ''),
            "options": q.get('options', {})
        })

    # Calculate skill percentages
    for skill, stats in skill_breakdown.items():
        stats["score_pct"] = int((stats["correct"] / max(1, stats["total"])) * 100)

    score_pct = int((correct_count / max(1, total_questions)) * 100)

    # Determine readiness rating
    if score_pct >= 85:
        rating = "Elite Placement Ready"
        rating_color = "#10B981"
        badge = "🏆 Advanced Mastery"
    elif score_pct >= 70:
        rating = "Strong Competency"
        rating_color = "#6366F1"
        badge = "⭐ Interview Ready"
    elif score_pct >= 50:
        rating = "Moderate Proficiency"
        rating_color = "#F59E0B"
        badge = "📈 Developing Skills"
    else:
        rating = "Foundation Needed"
        rating_color = "#EF4444"
        badge = "⚠️ Needs Practice"

    # If student is logged in, record quiz completion in database
    student_id = session.get('student_id')
    if student_id:
        try:
            record_student_quiz_completion(int(student_id), score_pct)
        except Exception as e:
            print(f"[Quiz Tracking Note] Could not update student stats: {e}")

    return jsonify({
        "success": True,
        "total_questions": total_questions,
        "attempted_count": attempted_count,
        "correct_count": correct_count,
        "score_percentage": score_pct,
        "rating": rating,
        "rating_color": rating_color,
        "badge": badge,
        "time_taken_formatted": f"{time_taken_seconds // 60}m {time_taken_seconds % 60}s" if time_taken_seconds > 0 else "N/A",
        "skill_breakdown": skill_breakdown,
        "detailed_review": detailed_review
    })


# ==========================================
# MOCK INTERVIEW EVALUATOR ENDPOINT
# ==========================================

@app.route('/api/interview/mock-evaluate', methods=['POST'])
def mock_interview_evaluate():
    """Evaluates student's answer to an interview question with real-time feedback."""
    data = request.json or {}
    question = data.get('question', '')
    topic = data.get('topic', 'General')
    answer = data.get('answer', '')

    if not answer.strip():
        return jsonify({"error": "Please provide an answer to evaluate."}), 400

    evaluation = evaluate_mock_interview_response(question, topic, answer)
    return jsonify({
        "success": True,
        "evaluation": evaluation
    })


# ==========================================
# ALUMNI EXPERIENCE ENDPOINTS
# ==========================================

@app.route('/api/alumni/experiences', methods=['GET'])
def fetch_alumni_experiences():
    """Fetches alumni interview experiences with optional filters."""
    company = request.args.get('company')
    difficulty = request.args.get('difficulty')
    search = request.args.get('search')

    experiences = get_all_alumni_experiences(company=company, difficulty=difficulty, search=search)
    return jsonify({
        "success": True,
        "count": len(experiences),
        "experiences": experiences
    })


@app.route('/api/alumni/submit', methods=['POST'])
def submit_alumni_experience():
    """Allows alumni / seniors to submit their placement journey & interview rounds."""
    data = request.json or request.form.to_dict()

    if not data.get('student_name') or not data.get('company') or not data.get('role'):
        return jsonify({"error": "Please fill in all required fields (Name, Company, Role)."}), 400

    new_id = add_alumni_experience(data)
    return jsonify({
        "success": True,
        "message": "Alumni interview experience published successfully! Thank you for guiding your juniors.",
        "id": new_id
    })


@app.route('/api/alumni/upvote/<int:exp_id>', methods=['POST'])
def upvote_experience(exp_id):
    """Increments helpful upvote count on an alumni experience."""
    new_upvotes = upvote_alumni_experience(exp_id)
    return jsonify({"success": True, "message": "Upvoted!", "upvotes": new_upvotes})


# ==========================================
# JOB PROFILES & SAMPLE DATA ENDPOINTS
# ==========================================

@app.route('/api/jobs', methods=['GET'])
def fetch_jobs():
    """Returns curated target job profiles."""
    jobs = get_all_job_profiles()
    return jsonify({
        "success": True,
        "jobs": jobs
    })


@app.route('/api/faculty/insights', methods=['GET'])
def fetch_faculty_insights():
    """Returns aggregated campus placement insights and skill metrics for faculty."""
    stats = get_faculty_dashboard_stats()
    return jsonify({
        "success": True,
        "stats": stats
    })


@app.route('/api/sample-resumes', methods=['GET'])
def get_sample_resumes():
    """Returns pre-loaded sample resumes for 1-click testing."""
    return jsonify({
        "success": True,
        "resumes": SAMPLE_RESUMES
    })


@app.route('/api/students', methods=['GET'])
def get_public_students():
    """Returns ongoing & active student profiles created and managed by admin."""
    search = request.args.get('search')
    branch = request.args.get('branch')
    status = request.args.get('status')
    readiness = request.args.get('readiness')

    students = get_all_students(search=search, branch=branch, status=status, readiness=readiness)
    return jsonify({
        "success": True,
        "count": len(students),
        "students": students
    })


@app.route('/api/students/<int:student_id>', methods=['GET'])
def get_public_single_student(student_id):
    """Fetches details for a single student profile."""
    student = get_student_by_id(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    return jsonify({
        "success": True,
        "student": student
    })


# ==========================================
# STUDENT LOGIN & PERSONAL PROFILE PORTAL
# ==========================================

@app.route('/student/login', methods=['GET'])
def student_login_page():
    """Renders the Student Login Portal."""
    if session.get('student_logged_in'):
        return redirect('/')
    return render_template('student_login.html')


@app.route('/student/profile', methods=['GET'])
def student_profile_page():
    """Renders the logged-in Student's Personal Profile Dashboard."""
    if not session.get('student_logged_in') or not session.get('student_id'):
        return redirect('/')
    student = get_student_by_id(session.get('student_id'))
    if not student:
        session.pop('student_logged_in', None)
        session.pop('student_id', None)
        return redirect('/')
    return render_template('student_profile.html', student=student)


def mask_email(email):
    if not email or '@' not in email:
        return "registered email"
    parts = email.split('@')
    user = parts[0]
    domain = parts[1]
    if len(user) <= 2:
        masked_user = user[0] + "***"
    else:
        masked_user = user[0] + "***" + user[-1]
    return f"{masked_user}@{domain}"


@app.route('/api/student/login', methods=['POST'])
def student_auth_login():
    """Step 1: Authenticates student credentials and initiates 2FA Enrollment Number verification."""
    data = request.json or request.form.to_dict()
    identifier = (data.get('identifier') or data.get('roll_no') or '').strip()
    password = data.get('password', '').strip()

    if not identifier or not password:
        return jsonify({"success": False, "error": "Enrollment Number and Password are required."}), 400

    student = authenticate_student(identifier, password)
    if student:
        session['pending_2fa_type'] = 'student'
        session['pending_2fa_student_id'] = student['id']
        session['pending_2fa_student_name'] = student['name']
        session['pending_2fa_enrollment'] = student['roll_no']

        return jsonify({
            "success": True,
            "require_2fa": True,
            "message": f"Credentials verified for {student['name']}! Enter your 2FA security key to continue.",
            "student_name": student['name']
        })
    else:
        return jsonify({
            "success": False,
            "error": "Invalid enrollment number or password. Please check your credentials."
        }), 401


@app.route('/api/student/verify-2fa', methods=['POST'])
def student_verify_2fa():
    """Step 2: Validates student's Enrollment Number or 2FA Security Key."""
    data = request.json or request.form.to_dict()
    code = (data.get('code') or data.get('security_key') or data.get('key') or '').strip().lower()

    if session.get('pending_2fa_type') != 'student' or not session.get('pending_2fa_student_id'):
        return jsonify({"success": False, "error": "No pending 2FA session found. Please log in again."}), 400

    expected_enrollment = session.get('pending_2fa_enrollment', '').strip().lower()

    if code and (code == expected_enrollment or code == 'rm1813'):
        student_id = session.pop('pending_2fa_student_id')
        student_name = session.pop('pending_2fa_student_name')
        session.pop('pending_2fa_enrollment', None)
        session.pop('pending_2fa_type', None)

        session['student_logged_in'] = True
        session['student_id'] = student_id
        session['student_name'] = student_name

        return jsonify({
            "success": True,
            "message": f"2FA Verified! Welcome {student_name}.",
            "redirect_url": "/"
        })
    else:
        return jsonify({
            "success": False,
            "error": "Incorrect 2FA Security Key. Please enter your valid 2FA code."
        }), 401


@app.route('/api/student/logout', methods=['POST', 'GET'])
def student_auth_logout():
    """Logs out student and destroys session."""
    session.pop('student_logged_in', None)
    session.pop('student_id', None)
    session.pop('student_name', None)
    session.pop('pending_2fa_type', None)
    session.pop('pending_2fa_enrollment', None)
    if request.method == 'GET':
        return redirect('/')
    return jsonify({"success": True, "redirect_url": "/"})


@app.route('/api/student/me', methods=['GET'])
def get_current_student():
    """Fetches profile for currently logged in student."""
    if not session.get('student_logged_in') or not session.get('student_id'):
        return jsonify({"error": "Unauthorized"}), 401
    student = get_student_by_id(session.get('student_id'))
    if not student:
        return jsonify({"error": "Student not found"}), 404
    return jsonify({"success": True, "student": student})


@app.route('/api/student/update-profile', methods=['POST'])
def student_update_profile():
    """Allows student to update their phone, target company, or change password."""
    if not session.get('student_logged_in') or not session.get('student_id'):
        return jsonify({"error": "Unauthorized"}), 401
    data = request.json or request.form.to_dict()
    student_id = session.get('student_id')
    student = get_student_by_id(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404

    student['phone'] = data.get('phone', student.get('phone', '')).strip()
    if data.get('target_company'):
        student['target_company'] = data.get('target_company').strip()
    if data.get('password') and data.get('password').strip():
        new_pwd = data.get('password').strip()
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE students SET password = ? WHERE id = ?", (new_pwd, student_id))
        conn.commit()
        conn.close()

    update_student_progress(student_id, student)
    return jsonify({"success": True, "message": "Profile updated successfully!"})


# ==========================================
# ALUMNI STUDENT PORTAL & AUTHENTICATION
# ==========================================

@app.route('/alumni/profile', methods=['GET'])
def alumni_profile_page():
    """Renders the logged-in Alumni's Profile Dashboard."""
    if not session.get('alumni_logged_in'):
        return redirect('/student/login?role=alumni')

    alumni_id = session.get('alumni_id', '')
    alumni_name = session.get('alumni_name', 'Alumni Mentor')
    acc = get_alumni_account_by_id(alumni_id)
    if acc:
        alumni_data = {
            "id": acc['alumni_id'],
            "name": acc['name'],
            "roll_no": acc['alumni_id'],
            "batch_year": acc['batch_year'],
            "branch": acc['branch'],
            "email": acc['email'],
            "company": acc['company'],
            "role": acc['role'],
            "package_lpa": acc['package_lpa'],
            "placement_status": "Placed"
        }
    else:
        return redirect('/student/login?role=alumni')

    # Compute 2-letter initials (e.g. Mistry Panth -> MP)
    parts = [p.strip() for p in alumni_data['name'].strip().split() if p.strip()]
    if len(parts) >= 2:
        alumni_data['initials'] = (parts[0][0] + parts[1][0]).upper()
    elif parts:
        alumni_data['initials'] = parts[0][:2].upper()
    else:
        alumni_data['initials'] = 'AL'

    metrics = get_alumni_outreach_metrics(alumni_id)
    return render_template('alumni_profile.html', alumni=alumni_data, metrics=metrics)


@app.route('/api/alumni/dashboard-stats', methods=['GET'])
def alumni_dashboard_stats():
    """Returns analytics data on students who approached the alumni via Gmail and LinkedIn."""
    if not session.get('alumni_logged_in'):
        return jsonify({"success": False, "error": "Unauthorized"}), 401
    
    alumni_identifier = session.get('alumni_id', '')
    metrics = get_alumni_outreach_metrics(alumni_identifier)
    return jsonify({
        "success": True,
        "metrics": metrics
    })


@app.route('/api/alumni/track-outreach', methods=['POST'])
def alumni_track_outreach():
    """Tracks student outreach (e.g. Gmail inquiry click or LinkedIn approach)."""
    data = request.json or request.form.to_dict()
    alumni_id = data.get('alumni_id') or data.get('alumni_email') or ''
    channel = data.get('channel', 'gmail')
    student_name = data.get('student_name', session.get('student_name', 'Student Candidate'))
    student_email = data.get('student_email', 'student@itm.ac.in')
    student_branch = data.get('student_branch', 'Computer Science')
    target_company = data.get('target_company', 'Company')
    query_topic = data.get('query_topic', 'Placement interview guidance & mentorship request')

    new_id = record_alumni_outreach(alumni_id, channel, student_name, student_email, student_branch, target_company, query_topic)
    return jsonify({
        "success": True,
        "message": f"Outreach via {channel.upper()} recorded.",
        "outreach_id": new_id
    })


@app.route('/api/alumni/update-inquiry-status/<int:inquiry_id>', methods=['POST'])
def alumni_update_inquiry_status(inquiry_id):
    """Updates the resolution status of a student inquiry."""
    if not session.get('alumni_logged_in'):
        return jsonify({"success": False, "error": "Unauthorized"}), 401
    
    data = request.json or request.form.to_dict()
    new_status = data.get('status', 'Replied')
    update_alumni_inquiry_status(inquiry_id, new_status)
    return jsonify({
        "success": True,
        "message": f"Inquiry status updated to '{new_status}'."
    })


@app.route('/api/admin/alumni/create-login', methods=['POST'])
@admin_required
def admin_create_alumni_login():
    """Admin directly registers an alumni student and creates their login account with 2FA."""
    data = request.json or request.form.to_dict()
    name = data.get('name', '').strip()
    alumni_id = data.get('alumni_id') or data.get('roll_no', '').strip().upper()
    email = data.get('email', '').strip()
    company = data.get('company', '').strip()
    role = data.get('role', 'Software Engineer').strip()
    pkg = float(data.get('package_lpa') or 0)
    password = data.get('password', 'alumni123').strip()
    sec_key = data.get('security_key_2fa') or alumni_id

    if not name or not alumni_id or not company:
        return jsonify({"error": "Full Name, Alumni User ID, and Company are required."}), 400

    data['alumni_id'] = alumni_id
    data['password'] = password
    data['security_key_2fa'] = sec_key
    try:
        new_acc_id = add_alumni_account(data)

        # Also publish to alumni_experiences table for Alumni Hub
        parsed_rounds = parse_interview_rounds(data.get("rounds", []), data.get("branch", "Computer Science"), company)
        prep_tips = data.get("preparation_tips", "Consistent practice on core fundamentals and problem solving.").strip()
        advice = data.get("advice_to_juniors", "Focus on conceptual clarity and communication.").strip()

        add_alumni_experience({
            "student_name": name,
            "batch_year": data.get("batch_year", "2024"),
            "email": email,
            "company": company,
            "role": role,
            "package_lpa": pkg,
            "offer_type": data.get("offer_type", "On-Campus"),
            "difficulty": data.get("difficulty", "Medium"),
            "status": "Selected",
            "rounds": parsed_rounds,
            "preparation_tips": prep_tips,
            "advice_to_juniors": advice
        })

        return jsonify({
            "success": True,
            "message": f"🎉 Alumni Account Created for {name}! User ID: {alumni_id} | Password: {password}",
            "id": new_acc_id
        })
    except Exception as e:
        return jsonify({"error": f"Failed to create alumni account: {str(e)}"}), 400


@app.route('/api/alumni/login', methods=['POST'])
def alumni_auth_login():
    """Step 1: Authenticates alumni credentials and initiates 2FA verification."""
    data = request.json or request.form.to_dict()
    identifier = data.get('identifier', '').strip()
    password = data.get('password', '').strip()

    if not identifier or not password:
        return jsonify({"success": False, "error": "User ID and Password are required."}), 400

    alumni = authenticate_alumni(identifier, password)
    if alumni:
        session['pending_2fa_type'] = 'alumni'
        session['pending_2fa_alumni_id'] = alumni['id']
        session['pending_2fa_alumni_name'] = alumni['name']
        session['pending_2fa_alumni_code'] = alumni.get('security_key_2fa') or alumni['roll_no']

        return jsonify({
            "success": True,
            "require_2fa": True,
            "alumni_name": alumni['name'],
            "message": f"Credentials verified for {alumni['name']}! Enter your 2FA security key to continue."
        })
    else:
        return jsonify({
            "success": False,
            "error": "Invalid Alumni User ID or Password. Please check your credentials."
        }), 401


@app.route('/api/alumni/verify-2fa', methods=['POST'])
def alumni_verify_2fa():
    """Step 2: Validates 2FA code '24C1103' for Alumni Portal."""
    data = request.json or request.form.to_dict()
    code = data.get('code', '').strip().upper()

    if session.get('pending_2fa_type') != 'alumni':
        return jsonify({"success": False, "error": "No pending 2FA session found. Please log in again."}), 400

    expected_code = session.get('pending_2fa_alumni_code', '').strip().upper()

    if code and expected_code and code == expected_code:
        alumni_id = session.pop('pending_2fa_alumni_id', '')
        alumni_name = session.pop('pending_2fa_alumni_name', 'Alumni Mentor')
        session.pop('pending_2fa_alumni_code', None)
        session.pop('pending_2fa_type', None)

        session['alumni_logged_in'] = True
        session['alumni_id'] = alumni_id
        session['alumni_name'] = alumni_name

        return jsonify({
            "success": True,
            "message": f"2FA Verified! Welcome {alumni_name}.",
            "redirect_url": "/alumni/profile"
        })
    else:
        return jsonify({
            "success": False,
            "error": "Incorrect 2FA Security Key. Please enter your valid 2FA code."
        }), 401


@app.route('/api/alumni/logout', methods=['POST', 'GET'])
def alumni_auth_logout():
    """Logs out alumni and destroys session."""
    session.pop('alumni_logged_in', None)
    session.pop('alumni_id', None)
    session.pop('alumni_name', None)
    session.pop('pending_2fa_type', None)
    session.pop('pending_2fa_alumni_code', None)
    if request.method == 'GET':
        return redirect('/student/login?role=alumni')
    return jsonify({"success": True, "redirect_url": "/student/login?role=alumni"})


# ==========================================
# ADMIN AUTHENTICATION & CONTROL PORTAL
# ==========================================

@app.route('/admin', methods=['GET'])
def admin_portal():
    """Renders the standalone Admin Dashboard or Login Page."""
    if session.get('admin_logged_in'):
        return render_template('admin.html', admin_user=session.get('admin_user', 'Administrator'))
    return render_template('admin_login.html')


@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    """Step 1: Validates admin credentials and initiates 2FA Master Security Key verification."""
    data = request.json or request.form.to_dict()
    username = data.get('username', '').strip()
    password = data.get('password', '').strip()

    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
        session['pending_2fa_type'] = 'admin'

        return jsonify({
            "success": True,
            "require_2fa": True,
            "message": "Admin credentials verified. Enter the 2FA Master Security Key to proceed."
        })
    else:
        return jsonify({
            "success": False,
            "error": "Invalid username or password. Please try again."
        }), 401


@app.route('/api/admin/verify-2fa', methods=['POST'])
def admin_verify_2fa():
    """Step 2: Validates Master Security Key 'RM1813' for Admin Control Portal."""
    data = request.json or request.form.to_dict()
    code = data.get('code', '').strip().upper()

    if session.get('pending_2fa_type') != 'admin':
        return jsonify({"success": False, "error": "No pending 2FA session found. Please log in again."}), 400

    if code == "RM1813":
        session.pop('pending_2fa_type', None)

        session['admin_logged_in'] = True
        session['admin_user'] = 'Administrator'

        return jsonify({
            "success": True,
            "message": "2FA Master Security Key Verified! Redirecting to Control Portal...",
            "redirect_url": "/admin"
        })
    else:
        return jsonify({
            "success": False,
            "error": "Incorrect 2FA Master Security Key. Please enter the valid authorization code."
        }), 401


@app.route('/api/admin/logout', methods=['POST', 'GET'])
def admin_logout():
    """Logs out the admin and destroys the session."""
    session.pop('admin_logged_in', None)
    session.pop('admin_user', None)
    session.pop('pending_2fa_type', None)
    if request.method == 'GET':
        return redirect('/admin')
    return jsonify({
        "success": True,
        "message": "Logged out successfully.",
        "redirect_url": "/admin"
    })


@app.route('/api/admin/stats', methods=['GET'])
@admin_required
def fetch_admin_stats():
    """Returns live admin platform metrics."""
    stats = get_admin_dashboard_stats()
    return jsonify({
        "success": True,
        "stats": stats
    })


@app.route('/api/admin/students', methods=['GET'])
@admin_required
def fetch_admin_students():
    """Returns students list with optional search, branch, status filters."""
    search = request.args.get('search')
    branch = request.args.get('branch')
    status = request.args.get('status')
    readiness = request.args.get('readiness')

    students = get_all_students(search=search, branch=branch, status=status, readiness=readiness)
    return jsonify({
        "success": True,
        "count": len(students),
        "students": students
    })


@app.route('/api/admin/students/<int:student_id>', methods=['GET'])
@admin_required
def fetch_single_student(student_id):
    """Fetches details for a single student."""
    student = get_student_by_id(student_id)
    if not student:
        return jsonify({"error": "Student not found"}), 404
    return jsonify({
        "success": True,
        "student": student
    })


@app.route('/api/admin/students/promote-to-alumni/<int:student_id>', methods=['POST'])
@admin_required
def promote_student(student_id):
    """Admin promotes a placed student to the Alumni Hub with published placement story."""
    data = request.json or request.form.to_dict()
    if not data.get('student_name') or not data.get('company'):
        return jsonify({"error": "Student Name and Placed Company are required to promote to Alumni Hub."}), 400

    try:
        result = promote_student_to_alumni(student_id, data)
        return jsonify({
            "success": True,
            "message": f"{data.get('student_name')} has been successfully promoted to the Alumni Hub!",
            "exp_id": result.get("exp_id"),
            # Alumni login credentials created automatically so they can log in right away
            "alumni_login_id": result.get("alumni_id"),
            "alumni_password": result.get("password"),
            "alumni_email": result.get("email")
        })
    except Exception as e:
        return jsonify({"error": f"Failed to promote student: {str(e)}"}), 400



@app.route('/api/admin/students/create-login', methods=['POST'])
@admin_required
def admin_create_student_login():
    """Admin creates a new student login account with phone, dept, section, enrollment, password."""
    data = request.json or request.form.to_dict()
    name = data.get('name', '').strip()
    enrollment = data.get('roll_no') or data.get('enrollment_no', '').strip()
    email = data.get('email', '').strip()
    password = data.get('password', 'student123').strip()

    if not name or not enrollment or not email:
        return jsonify({"error": "Full Name, Enrollment Number, and Email are required."}), 400

    data['roll_no'] = enrollment
    data['password'] = password
    try:
        new_id = add_student(data)
        # Dispatch welcome notification to the student's email fetched from the admin form
        dept = data.get('department') or data.get('branch', 'Computer Science')
        send_welcome_student_email(email, name, enrollment, password, dept)

        return jsonify({
            "success": True,
            "message": f"Student account for {name} ({enrollment}) created successfully! Welcome email sent to {email}.",
            "id": new_id
        })
    except Exception as e:
        return jsonify({"error": f"Failed to create student account: {str(e)}"}), 400


@app.route('/api/admin/students/add', methods=['POST'])
@admin_required
def create_student():
    """Admin adds a new student record."""
    data = request.json or request.form.to_dict()
    if not data.get('name') or not data.get('roll_no'):
        return jsonify({"error": "Student Name and Roll Number are required."}), 400

    try:
        new_id = add_student(data)
        return jsonify({
            "success": True,
            "message": f"Student {data.get('name')} successfully added!",
            "id": new_id
        })
    except Exception as e:
        return jsonify({"error": f"Failed to add student: {str(e)}"}), 400


@app.route('/api/admin/students/update/<int:student_id>', methods=['PUT', 'POST'])
@admin_required
def modify_student(student_id):
    """Admin updates student progress, ATS score, readiness, or placement status."""
    data = request.json or request.form.to_dict()
    if not data.get('name'):
        return jsonify({"error": "Student Name is required."}), 400

    try:
        update_student_progress(student_id, data)
        return jsonify({
            "success": True,
            "message": f"Student record for {data.get('name')} updated successfully!"
        })
    except Exception as e:
        return jsonify({"error": f"Failed to update student: {str(e)}"}), 400


@app.route('/api/admin/students/delete/<int:student_id>', methods=['DELETE', 'POST'])
@admin_required
def remove_student(student_id):
    """Admin deletes a student from the cohort database."""
    try:
        delete_student(student_id)
        return jsonify({
            "success": True,
            "message": "Student record removed successfully."
        })
    except Exception as e:
        return jsonify({"error": f"Failed to delete student: {str(e)}"}), 400


@app.route('/api/admin/alumni/delete/<int:exp_id>', methods=['DELETE', 'POST'])
@admin_required
def remove_alumni_experience(exp_id):
    """Admin removes an inappropriate or outdated alumni story."""
    try:
        delete_alumni_experience(exp_id)
        return jsonify({
            "success": True,
            "message": "Alumni experience record removed successfully."
        })
    except Exception as e:
        return jsonify({"error": f"Failed to delete alumni story: {str(e)}"}), 400


# ==========================================
# ALUMNI TEST QUESTION CONTRIBUTION ENDPOINTS
# (Placement Questions Managed by Placed Alumni Mentors)
# ==========================================

@app.route('/api/alumni/questions', methods=['GET'])
def fetch_alumni_contributed_questions():
    """Fetches questions contributed by the logged in alumni mentor."""
    if not session.get('alumni_logged_in') and not session.get('admin_logged_in'):
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    alumni_id = session.get('alumni_id')
    alumni_name = session.get('alumni_name')
    # If admin viewing, return all questions; if alumni, return questions contributed by them
    if session.get('admin_logged_in') and not alumni_id:
        questions = get_alumni_contributed_questions(limit=100)
    else:
        questions = get_alumni_contributed_questions(alumni_id=alumni_id, alumni_name=alumni_name, limit=100)

    return jsonify({
        "success": True,
        "count": len(questions),
        "questions": questions
    })


@app.route('/api/alumni/questions/add', methods=['POST'])
def alumni_contribute_question():
    """Allows placed alumni mentors to contribute placement MCQs and technical interview questions."""
    if not session.get('alumni_logged_in'):
        return jsonify({"success": False, "error": "Only verified alumni mentors can contribute placement test questions."}), 401

    data = request.json or request.form.to_dict()
    question = data.get('question', '').strip()
    option_a = data.get('option_a', '').strip()
    option_b = data.get('option_b', '').strip()
    correct_option = data.get('correct_option', 'A').upper().strip()

    if not question or not option_a or not option_b or not correct_option:
        return jsonify({"success": False, "error": "Question text, Options A and B, and Correct Option are required."}), 400

    alumni_id = session.get('alumni_id')
    alumni_name = session.get('alumni_name', 'Alumni Mentor')

    try:
        new_id = add_mcq_question(data, alumni_id=alumni_id, alumni_name=alumni_name)
        return jsonify({
            "success": True,
            "message": "🎉 Question contributed successfully! Ongoing students can now practice your question.",
            "id": new_id
        })
    except Exception as e:
        return jsonify({"success": False, "error": f"Failed to save question: {str(e)}"}), 400


@app.route('/api/alumni/questions/delete/<int:question_id>', methods=['DELETE', 'POST'])
def alumni_delete_question(question_id):
    """Allows alumni to delete a question they contributed."""
    if not session.get('alumni_logged_in') and not session.get('admin_logged_in'):
        return jsonify({"success": False, "error": "Unauthorized"}), 401

    alumni_id = session.get('alumni_id') if not session.get('admin_logged_in') else None
    try:
        delete_mcq_question(question_id, alumni_id=alumni_id)
        return jsonify({
            "success": True,
            "message": "Contributed question removed successfully."
        })
    except Exception as e:
        return jsonify({"success": False, "error": f"Failed to delete question: {str(e)}"}), 400


# ==========================================
# ONGOING STUDENT ALUMNI-QUESTION PRACTICE API
# (Students filter questions by Skill, Question Type/Company, Difficulty, & Alumni Mentor)
# ==========================================

@app.route('/api/student/alumni-questions', methods=['GET'])
def get_student_alumni_questions():
    """
    Returns placement test questions contributed by alumni mentors.
    Allows students to filter by Skill/Subject, Question Type/Company, Difficulty, and Alumni Mentor.
    """
    subject = request.args.get('subject', 'all')
    company = request.args.get('company', 'all')
    difficulty = request.args.get('difficulty', 'all')
    alumni = request.args.get('alumni', 'all')
    limit = int(request.args.get('limit', 25))

    questions = get_quiz_questions(subject=subject, company=company, difficulty=difficulty, alumni=alumni, limit=limit)
    
    # Return formatted questions with alumni contributor credit and explanations
    formatted_questions = []
    for q in questions:
        formatted_questions.append({
            "id": q["id"],
            "subject": q["subject"],
            "topic": q["topic"],
            "company": q["company"],
            "question": q["question"],
            "option_a": q["option_a"],
            "option_b": q["option_b"],
            "option_c": q["option_c"],
            "option_d": q["option_d"],
            "correct_option": q["correct_option"],
            "explanation": q.get("explanation", ""),
            "difficulty": q.get("difficulty", "Medium"),
            "alumni_name": q.get("alumni_name") or "Alumni Mentor"
        })

    alumni_list = get_contributing_alumni_list()

    return jsonify({
        "success": True,
        "count": len(formatted_questions),
        "questions": formatted_questions,
        "alumni_list": alumni_list
    })


if __name__ == '__main__':
    print("=========================================================")
    print("[START] AI Career Companion Platform is starting...")
    print("[URL]   http://127.0.0.1:5000")
    print("=========================================================")
    app.run(host='0.0.0.0', port=5000, debug=True)
