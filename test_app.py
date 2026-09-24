"""
Verification Test Script for AI Career Companion
Tests NLP Engine, Database, and Flask REST API endpoints.
"""

import unittest
import json
from app import app
from nlp_engine import (
    extract_skills_from_text,
    analyze_resume_ats,
    recommend_career_paths,
    match_resume_with_job_description,
    evaluate_mock_interview_response
)
from sample_resumes import SAMPLE_RESUMES

class TestCareerCompanion(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True

    def test_nlp_skill_extraction(self):
        sample = SAMPLE_RESUMES["fullstack"]["content"]
        skills = extract_skills_from_text(sample)
        self.assertIn("languages", skills)
        self.assertTrue(len(skills["languages"]) > 0)
        self.assertTrue(any("React" in s or "React.Js" in s for s in skills["frameworks_libraries"]))
        print("[OK] NLP Skill Extraction Passed")

    def test_ats_analyzer(self):
        sample = SAMPLE_RESUMES["fullstack"]["content"]
        skills = extract_skills_from_text(sample)
        ats = analyze_resume_ats(sample, skills)
        self.assertGreaterEqual(ats["ats_score"], 70)
        self.assertIn("section_breakdown", ats)
        self.assertIn("recommendations", ats)
        print(f"[OK] ATS Analyzer Passed (Score: {ats['ats_score']})")

    def test_job_matcher_and_roadmap(self):
        sample = SAMPLE_RESUMES["fullstack"]["content"]
        jd = "We are seeking a Backend Engineer with Python, FastAPI, Docker, Kubernetes, AWS, and PostgreSQL experience."
        match = match_resume_with_job_description(sample, jd)
        self.assertIn("match_score", match)
        self.assertIn("matched_skills", match)
        self.assertIn("missing_skills", match)
        self.assertIn("roadmap", match)
        self.assertTrue(len(match["roadmap"]) > 0)
        print(f"[OK] JD Matcher & Roadmap Passed (Match: {match['match_score']}%, Missing: {match['missing_skills']})")

    def test_mock_interview_eval(self):
        question = "Explain the difference between deep copy and shallow copy in Python."
        answer = "A shallow copy creates a new collection object and populates it with references to the child objects in the original. In contrast, a deep copy recursively duplicates every object referenced by the parent."
        eval_res = evaluate_mock_interview_response(question, "Python", answer)
        self.assertGreaterEqual(eval_res["score"], 60)
        self.assertIn("strengths", eval_res)
        print(f"[OK] Mock Interview Evaluator Passed (Score: {eval_res['score']})")

    def test_flask_endpoints(self):
        # 1. Test Home Page
        res = self.app.get('/')
        self.assertEqual(res.status_code, 200)

        # 2. Test Resume Analyze Endpoint
        res = self.app.post('/api/resume/analyze', json={'resume_text': SAMPLE_RESUMES["aiml"]["content"]})
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        self.assertGreaterEqual(data["ats_analysis"]["ats_score"], 60)

        # 3. Test Quiz Questions Endpoint
        res = self.app.get('/api/quiz/questions?subject=DSA&limit=5')
        self.assertEqual(res.status_code, 200)
        quiz_data = res.get_json()
        self.assertTrue(quiz_data["success"])
        self.assertTrue(len(quiz_data["questions"]) > 0)

        # 4. Test Quiz Submit Endpoint
        first_q = quiz_data["questions"][0]
        sub_res = self.app.post('/api/quiz/submit', json={'answers': {str(first_q["id"]): "B"}})
        self.assertEqual(sub_res.status_code, 200)
        sub_data = sub_res.get_json()
        self.assertTrue(sub_data["success"])

        # 5. Test Alumni Experiences Endpoint
        res = self.app.get('/api/alumni/experiences')
        self.assertEqual(res.status_code, 200)
        exp_data = res.get_json()
        self.assertTrue(exp_data["success"])
        self.assertTrue(len(exp_data["experiences"]) >= 5)

        # 6. Test Alumni Upvote Endpoint
        first_exp = exp_data["experiences"][0]
        res = self.app.post(f'/api/alumni/upvote/{first_exp["id"]}')
        self.assertEqual(res.status_code, 200)

        # 7. Test Faculty Insights Endpoint
        res = self.app.get('/api/faculty/insights')
        self.assertEqual(res.status_code, 200)
        fac_data = res.get_json()
        self.assertTrue(fac_data["success"])

        print("[OK] All Flask REST API Endpoints Passed (200 OK)")

if __name__ == '__main__':
    unittest.main()
