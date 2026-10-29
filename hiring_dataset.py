"""
AI Career Companion - Company Hiring & Recruiter Matching Module
Provides automated resume matching across registered recruiters, skill-gap analysis,
CTC benchmarking, and candidate evaluation.
Connects dynamically to the job_profiles database table and recruiter profiles.
"""

import os
import json
import csv
import re
from typing import Dict, List, Any, Optional

# Base directory for dataset files (if custom dataset is uploaded)
DATASET_DIR = os.path.join(os.path.dirname(__file__), 'data', 'ITM_SLS_45_Company_Hiring_Dataset', 'itm_sls_45_company_hiring_dataset')

def _clean_skills_list(skills_str: str) -> List[str]:
    """Parses semicolon or comma-separated skill strings into clean lists."""
    if not skills_str:
        return []
    parts = re.split(r'[;,]', skills_str)
    return [p.strip() for p in parts if p.strip()]


def _parse_ctc_range(ctc_str: str) -> Dict[str, float]:
    """Parses CTC range string like '4.5-7.0' into min and max float values."""
    try:
        cleaned = str(ctc_str).replace('₹', '').replace('LPA', '').replace('lpa', '').strip()
        if '-' in cleaned:
            parts = cleaned.split('-')
            return {"min": float(parts[0].strip()), "max": float(parts[1].strip())}
        val = float(cleaned)
        return {"min": val, "max": val}
    except Exception:
        return {"min": 4.0, "max": 7.0}


def load_45_companies() -> List[Dict[str, Any]]:
    """
    Loads active company hiring profiles from database job_profiles table.
    Clean slate: returns an empty list if no companies have been registered yet.
    """
    try:
        from database import get_db_connection
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM job_profiles ORDER BY company ASC")
        rows = cursor.fetchall()
        conn.close()

        if rows:
            companies = []
            for r in rows:
                item = dict(r) if hasattr(r, 'keys') else r
                req_skills = _clean_skills_list(item.get("required_skills", ""))
                ctc_info = _parse_ctc_range(item.get("ctc_range", "Competitive"))
                companies.append({
                    "job_id": item.get("id", ""),
                    "company": item.get("company", ""),
                    "role": item.get("role_title", "Software Engineer"),
                    "required_skills": req_skills,
                    "required_skills_raw": item.get("required_skills", ""),
                    "indicative_ctc_range_lpa": item.get("ctc_range", "Competitive"),
                    "min_ctc": ctc_info["min"],
                    "max_ctc": ctc_info["max"],
                    "location": item.get("location", "PAN India"),
                    "experience_level": item.get("experience_level", "Fresher"),
                    "job_description_snippet": item.get("description", "")[:280],
                    "job_requirement_full": item.get("description", "")
                })
            return companies
    except Exception as e:
        print(f"[DB Notice] Could not load companies from job_profiles: {e}")

    # Fallback to file if user uploads a JSON map in the future
    json_path = os.path.join(DATASET_DIR, '45_company_hiring_map.json')
    if os.path.exists(json_path):
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                raw_data = json.load(f)
            companies = []
            for item in raw_data:
                ctc_info = _parse_ctc_range(item.get("indicative_ctc_range_lpa", "4.0-6.5"))
                req_skills = _clean_skills_list(item.get("required_skills", ""))
                companies.append({
                    "job_id": item.get("job_id", ""),
                    "company": item.get("company", ""),
                    "role": item.get("role", "Software Engineer"),
                    "required_skills": req_skills,
                    "required_skills_raw": item.get("required_skills", ""),
                    "indicative_ctc_range_lpa": item.get("indicative_ctc_range_lpa", "4.5-7.0"),
                    "min_ctc": ctc_info["min"],
                    "max_ctc": ctc_info["max"],
                    "candidate_id": item.get("candidate_id", ""),
                    "job_description_snippet": f"Role at {item.get('company')} requiring {item.get('required_skills')}",
                    "job_requirement_full": ""
                })
            return companies
        except Exception:
            pass

    return []


def load_dataset_candidates() -> List[Dict[str, Any]]:
    """Loads candidate records from CSV if available, otherwise returns empty list."""
    csv_path = os.path.join(DATASET_DIR, 'candidates_with_45_companies.csv')
    if not os.path.exists(csv_path):
        return []
    try:
        candidates = []
        with open(csv_path, 'r', encoding='utf-8', errors='ignore') as f:
            reader = csv.DictReader(f)
            for row in reader:
                candidates.append({
                    "candidate_id": row.get("candidate_id", ""),
                    "name": row.get("name", ""),
                    "degree": row.get("degree", ""),
                    "target_role": row.get("target_role", ""),
                    "skills": _clean_skills_list(row.get("skills", "")),
                    "resume_score": float(row.get("resume_score", 75) or 75),
                    "employer": row.get("employer", ""),
                    "job_title": row.get("job_title", ""),
                    "indicative_ctc_lpa": float(row.get("indicative_ctc_lpa", 4.0) or 4.0)
                })
        return candidates
    except Exception:
        return []


def compare_resume_with_45_companies(resume_text: str, extracted_skills: Dict[str, List[str]]) -> Dict[str, Any]:
    """
    Compares the candidate's extracted skills & text against registered company job profiles.
    If no companies are currently registered, builds candidate skill intelligence directly from the resume.
    """
    # Flatten user's extracted skills into a lowercase set
    user_skills_flat = set()
    candidate_skills_list = []
    seen_cand = set()
    for cat, skills in extracted_skills.items():
        for s in skills:
            s_clean = s.strip()
            user_skills_flat.add(s_clean.lower())
            if s_clean and s_clean.lower() not in seen_cand:
                seen_cand.add(s_clean.lower())
                candidate_skills_list.append(s_clean)

    companies = load_45_companies()

    # If no companies are registered, gracefully return clean baseline intelligence
    if not companies:
        return {
            "top_matches": [],
            "all_matches": [],
            "total_companies_evaluated": 0,
            "average_match_score": 0,
            "high_fit_count": 0,
            "best_match_company": None,
            "company_skills_intelligence": {
                "target_companies_required_skills": [],
                "matched_company_skills": candidate_skills_list[:8],
                "missing_company_skills": [],
                "assessment_target_skills": candidate_skills_list[:12],
                "total_skills_demanded": 0,
                "matched_count": len(candidate_skills_list[:8]),
                "missing_count": 0,
                "readiness_ratio_pct": 100.0 if candidate_skills_list else 0.0
            }
        }

    resume_text_lower = resume_text.lower() if resume_text else ""
    company_matches = []

    for comp in companies:
        required_skills = comp.get("required_skills", [])
        req_count = len(required_skills)
        if req_count == 0:
            continue

        matched_skills = []
        missing_skills = []

        for req in required_skills:
            req_lower = req.lower().strip()
            is_matched = False
            if req_lower in user_skills_flat:
                is_matched = True
            elif any(req_lower == u or req_lower in u or u in req_lower for u in user_skills_flat):
                is_matched = True
            elif re.search(r'\b' + re.escape(req_lower) + r'\b', resume_text_lower):
                is_matched = True

            if is_matched:
                matched_skills.append(req)
            else:
                missing_skills.append(req)

        skill_match_pct = (len(matched_skills) / req_count) * 100.0

        role_bonus = 0.0
        role_lower = comp.get("role", "").lower()
        if any(w in resume_text_lower for w in role_lower.split() if len(w) > 3):
            role_bonus += 8.0

        if any(w in resume_text_lower for w in comp.get("company", "").lower().split() if len(w) > 3):
            role_bonus += 4.0

        final_match_score = min(100.0, round(skill_match_pct * 0.85 + role_bonus, 1))

        if final_match_score >= 75.0:
            fit_tier = "High Fit"
            tier_badge = "Excellent Match"
        elif final_match_score >= 50.0:
            fit_tier = "Moderate Fit"
            tier_badge = "Good Opportunity"
        else:
            fit_tier = "Developing Fit"
            tier_badge = "Skill Gap Exists"

        company_matches.append({
            "job_id": comp.get("job_id", ""),
            "company": comp.get("company", ""),
            "role": comp.get("role", ""),
            "match_score": final_match_score,
            "matched_skills": matched_skills,
            "missing_skills": missing_skills,
            "fit_tier": fit_tier,
            "tier_badge": tier_badge,
            "indicative_ctc": comp.get("indicative_ctc_range_lpa", "Competitive"),
            "required_skills_count": req_count,
            "matched_skills_count": len(matched_skills),
            "missing_skills_count": len(missing_skills),
            "snippet": comp.get("job_description_snippet", "")
        })

    company_matches.sort(key=lambda x: x["match_score"], reverse=True)
    top_matches = company_matches[:10]
    high_fit_companies = [c for c in company_matches if c["fit_tier"] == "High Fit"]
    avg_score = round(sum(c["match_score"] for c in company_matches) / len(company_matches), 1) if company_matches else 0.0

    all_req_skills = []
    seen_req = set()
    matched_skills_set = set()
    missing_skills_set = set()

    for comp in top_matches:
        for r_skill in comp.get("required_skills", []):
            r_clean = r_skill.strip()
            if r_clean and r_clean.lower() not in seen_req:
                seen_req.add(r_clean.lower())
                all_req_skills.append(r_clean)
        for m_skill in comp.get("matched_skills", []):
            matched_skills_set.add(m_skill.strip())
        for mis_skill in comp.get("missing_skills", []):
            missing_skills_set.add(mis_skill.strip())

    assessment_target_skills = []
    seen_assess = set()
    for s in list(matched_skills_set) + candidate_skills_list[:6] + list(missing_skills_set)[:4]:
        if s and s.lower() not in seen_assess:
            seen_assess.add(s.lower())
            assessment_target_skills.append(s)

    company_skills_intelligence = {
        "target_companies_required_skills": all_req_skills,
        "matched_company_skills": sorted(list(matched_skills_set)),
        "missing_company_skills": sorted(list(missing_skills_set)),
        "assessment_target_skills": assessment_target_skills[:12],
        "total_skills_demanded": len(all_req_skills),
        "matched_count": len(matched_skills_set),
        "missing_count": len(missing_skills_set),
        "readiness_ratio_pct": round((len(matched_skills_set) / max(1, len(all_req_skills))) * 100, 1)
    }

    return {
        "top_matches": top_matches,
        "all_matches": company_matches,
        "total_companies_evaluated": len(company_matches),
        "best_match_company": company_matches[0] if company_matches else None,
        "high_fit_count": len(high_fit_companies),
        "average_match_score": avg_score,
        "company_skills_intelligence": company_skills_intelligence
    }


def benchmark_candidate_against_dataset(ats_score: float, extracted_skills: Dict[str, List[str]]) -> Dict[str, Any]:
    """
    Computes cohort benchmark. If no external dataset is active, computes realistic percentile
    based on student resume ATS quality and skills breadth.
    """
    candidates = load_dataset_candidates()
    if not candidates:
        # Realistic algorithmic percentile benchmark based on ATS score
        user_skill_count = sum(len(skills) for skills in extracted_skills.values())
        calculated_percentile = min(98.0, max(25.0, round(ats_score * 0.9 + min(15.0, user_skill_count * 1.5), 1)))
        return {
            "percentile_rank": calculated_percentile,
            "cohort_total": 0,
            "similar_candidate": None,
            "cohort_avg_ats": 75.0
        }

    total_candidates = len(candidates)
    user_skill_count = sum(len(skills) for skills in extracted_skills.values())
    scores_below = sum(1 for c in candidates if c.get("resume_score", 75) <= ats_score)
    percentile = round((scores_below / total_candidates) * 100.0, 1)
    percentile = max(5.0, min(99.0, percentile))

    return {
        "percentile_rank": percentile,
        "cohort_total": total_candidates,
        "cohort_avg_ats": round(sum(c.get("resume_score", 75) for c in candidates) / total_candidates, 1),
        "similar_candidate": None
    }
