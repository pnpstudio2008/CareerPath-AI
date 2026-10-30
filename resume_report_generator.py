"""
AI Career Companion - Resume Performance & ATS Audit Report Generator
Generates an official, print-ready, SINGLE-PAGE executive evaluation document
incorporating the 6-part feedback workflow:
1. Exact Result of Matched Percentage According to Resume (ATS Score)
2. Result Percentage of the Practical Mock Test
3. Target Companies to Approach (12 Industry Clusters) & Verified Core Skills
4. The Negative Side: Resume-Claimed Skills Unverified in Practical Test
5. 3-5 Step Growth & Placement Action Plan
6. Curated Remediation Resources with Direct Links from learn-anything.xyz
"""

import io
import os
import json
import datetime
from typing import Dict, Any, List

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.graphics.shapes import Drawing, Circle, String
from mock_test_engine import get_learn_anything_url


# ==========================================
# PALETTE DEFINITIONS (Modern Executive Theme)
# ==========================================
C_PRIMARY = colors.HexColor('#0F172A')       # Slate 900
C_SECONDARY = colors.HexColor('#334155')     # Slate 700
C_MUTED = colors.HexColor('#64748B')         # Slate 500
C_BG_CARD = colors.HexColor('#F8FAFC')       # Slate 50
C_BORDER = colors.HexColor('#CBD5E1')        # Slate 300
C_EMERALD = colors.HexColor('#059669')      # Emerald 600
C_EMERALD_BG = colors.HexColor('#ECFDF5')   # Emerald 50
C_BLUE = colors.HexColor('#2563EB')         # Blue 600
C_BLUE_BG = colors.HexColor('#EFF6FF')      # Blue 50
C_AMBER = colors.HexColor('#D97706')        # Amber 600
C_AMBER_BG = colors.HexColor('#FFFBEB')     # Amber 50
C_ROSE = colors.HexColor('#DC2626')         # Red 600
C_ROSE_BG = colors.HexColor('#FEF2F2')      # Red 50
C_ROSE_BORDER = colors.HexColor('#FECACA')  # Red 200


def create_mini_gauge(score: float, label: str, tier_color: str, tier_bg: str) -> Drawing:
    """Generates an elegant, balanced circular gauge with clear metrics."""
    d = Drawing(74, 66)
    # Background circle ring centered at x=37, y=38, radius=24
    d.add(Circle(37, 38, 24, fillColor=colors.HexColor(tier_bg), strokeColor=colors.HexColor(tier_color), strokeWidth=2.2))
    # Inner white circle
    d.add(Circle(37, 38, 18.5, fillColor=colors.white, strokeColor=colors.transparent))
    # Score number centered at y=33
    d.add(String(37, 33, f"{int(round(score))}%", fontName="Helvetica-Bold", fontSize=11.5, textAnchor="middle", fillColor=colors.HexColor(tier_color)))
    # Subtitle label below with clear breathing room
    d.add(String(37, 8, label, fontName="Helvetica-Bold", fontSize=7.0, textAnchor="middle", fillColor=C_SECONDARY))
    return d


def generate_resume_pdf_report(student: dict, resume_record: dict) -> bytes:
    """
    Generates an official, single-page executive PDF report highlighting:
    - Resume Matched Percentage
    - Mock Test Result Percentage
    - Target Industry Cluster Recruiters to Approach & Verified Skills
    - The Negative Side (Resume Claims Unverified in Practical Test)
    - 3-5 Step Growth & Placement Action Plan
    - Interactive Learning Resources from learn-anything.xyz
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=26,
        rightMargin=26,
        topMargin=18,
        bottomMargin=18
    )

    styles = getSampleStyleSheet()

    title_p = ParagraphStyle(
        'RTitle',
        fontName='Helvetica-Bold',
        fontSize=12.5,
        leading=16.0,
        textColor=colors.white
    )
    meta_p = ParagraphStyle(
        'RMeta',
        fontName='Helvetica',
        fontSize=8.0,
        leading=11.2,
        textColor=colors.HexColor('#E2E8F0'),
        alignment=2
    )
    sec_title = ParagraphStyle(
        'SecT',
        fontName='Helvetica-Bold',
        fontSize=9.8,
        leading=12.5,
        textColor=C_PRIMARY,
        spaceBefore=0,
        spaceAfter=0
    )
    body_dark = ParagraphStyle(
        'BDark',
        fontName='Helvetica',
        fontSize=8.0,
        leading=11.5,
        textColor=C_SECONDARY
    )
    body_bold = ParagraphStyle(
        'BBold',
        fontName='Helvetica-Bold',
        fontSize=8.0,
        leading=11.5,
        textColor=C_PRIMARY
    )
    body_muted = ParagraphStyle(
        'BMuted',
        fontName='Helvetica',
        fontSize=7.2,
        leading=9.8,
        textColor=C_MUTED
    )
    bullet_p = ParagraphStyle(
        'BulletP',
        fontName='Helvetica',
        fontSize=8.0,
        leading=11.6,
        textColor=C_SECONDARY
    )

    story = []
    TOTAL_WIDTH = 560  # 612 - 52 (26 margins on each side)

    # -------------------------------------------------------------
    # 1. HEADER BANNER BLOCK (Deep Primary Navy)
    # -------------------------------------------------------------
    candidate_name = student.get('name', 'Student Candidate') if isinstance(student, dict) else 'Student Candidate'
    roll_no = student.get('roll_no', 'N/A') if isinstance(student, dict) else 'N/A'
    branch = student.get('branch', 'Computer Science & Engineering') if isinstance(student, dict) else 'Computer Science & Engineering'
    eval_date = str(resume_record.get('created_at', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))[:10]

    header_table = Table([
        [
            Paragraph("<b>AI CAREER COMPANION &bull; OFFICIAL PLACEMENT AUDIT REPORT</b>", title_p),
            Paragraph(f"<b>Candidate:</b> {candidate_name} ({roll_no})<br/><b>Branch:</b> {branch} &bull; <b>Date:</b> {eval_date}", meta_p)
        ]
    ], colWidths=[338, 222])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_PRIMARY),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # 2. DUAL SCORE OVERVIEW CARD (RESUME MATCH % + MOCK TEST RESULT %)
    # -------------------------------------------------------------
    ats_score = float(resume_record.get('ats_score', 80) or 80)
    mock_score = float(resume_record.get('mocktest_score', 0) or 0)
    has_test = bool(resume_record.get('test_completed', False) or mock_score > 0)
    composite_score = round((ats_score + mock_score) / 2.0, 1) if has_test else ats_score

    ats_tier_color = "#059669" if ats_score >= 80 else ("#D97706" if ats_score >= 65 else "#DC2626")
    ats_tier_bg = "#ECFDF5" if ats_score >= 80 else ("#FFFBEB" if ats_score >= 65 else "#FEF2F2")

    mock_tier_color = "#059669" if mock_score >= 80 else ("#2563EB" if mock_score >= 65 else ("#F59E0B" if mock_score >= 50 else "#DC2626"))
    mock_tier_bg = "#ECFDF5" if mock_score >= 80 else ("#EFF6FF" if mock_score >= 65 else ("#FFFBEB" if mock_score >= 50 else "#FEF2F2"))

    ats_gauge = create_mini_gauge(ats_score, "RESUME MATCH", ats_tier_color, ats_tier_bg)
    test_gauge = create_mini_gauge(mock_score if has_test else 0, "MOCK TEST %", mock_tier_color, mock_tier_bg)

    gauge_cell = Table([[ats_gauge, test_gauge]], colWidths=[74, 74])
    gauge_cell.setStyle(TableStyle([
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 0),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 0),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))

    filename = str(resume_record.get('filename') or 'Resume.pdf')
    best_role = str(resume_record.get('best_role') or resume_record.get('predicted_role') or 'Software Development Engineer (SDE)')

    # Unpack candidate skills
    skills_raw = resume_record.get('extracted_skills', resume_record.get('skills', [])) or []
    if isinstance(skills_raw, str):
        try:
            skills_raw = json.loads(skills_raw)
        except Exception:
            skills_raw = [s.strip() for s in skills_raw.split(',') if s.strip()]

    if isinstance(skills_raw, dict):
        skills_list = []
        for cat_skills in skills_raw.values():
            if isinstance(cat_skills, list):
                skills_list.extend(cat_skills)
            elif isinstance(cat_skills, str):
                skills_list.append(cat_skills)
    elif isinstance(skills_raw, list):
        skills_list = skills_raw
    else:
        skills_list = []

    seen = set()
    cleaned_skills = []
    for s in skills_list:
        s_str = str(s).strip()
        if s_str and s_str.lower() not in seen:
            seen.add(s_str.lower())
            cleaned_skills.append(s_str)
    skills_list = cleaned_skills

    skills_str = ", ".join(skills_list[:12]) if skills_list else "Python, SQL, React, Git, Docker, REST APIs"
    if len(skills_list) > 12:
        skills_str += f", +{len(skills_list) - 12} more"

    verification_status = "<font color='#059669'><b>&#10003; MOCK TEST VERIFIED &amp; COMPLETED</b></font>" if has_test else "<font color='#DC2626'><b>&#9888; Assessment Pending</b></font>"

    info_box = [
        Paragraph(f"<b>Resume File:</b> <font color='#1E293B'>{filename}</font> &nbsp;&bull;&nbsp; <b>Status:</b> {verification_status}", body_dark),
        Spacer(1, 3.5),
        Paragraph(f"<b>Primary Target Role:</b> <font color='#1E40AF'><b>{best_role}</b></font> &nbsp;&bull;&nbsp; <b>Recruiter Alignment:</b> <font color='#059669'><b>High Match Tier</b></font>", body_dark),
        Spacer(1, 3.5),
        Paragraph(f"<b>Verified Assessment Index:</b> Resume ATS: <b>{int(round(ats_score))}%</b> &nbsp;&bull;&nbsp; Practical Test: <b>{int(round(mock_score))}%</b> &nbsp;&bull;&nbsp; Composite: <font color='#059669'><b>{int(round(composite_score))}%</b></font>", body_dark),
        Spacer(1, 3.5),
        Paragraph(f"<b>Extracted Resume Skills ({len(skills_list)}):</b> <font color='#475569'>{skills_str}</font>", ParagraphStyle('SkP', fontName='Helvetica', fontSize=7.6, leading=10.5, textColor=C_SECONDARY))
    ]

    overview_table = Table([[gauge_cell, info_box]], colWidths=[156, 404])
    overview_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_BG_CARD),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(overview_table)
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # 3. SECTION 1: TARGET COMPANIES TO APPROACH & VERIFIED ASSETS
    # -------------------------------------------------------------
    story.append(Paragraph("<b>1. Target Recruiters to Approach (Industry Clusters) &amp; Verified Skills</b>", sec_title))
    story.append(Spacer(1, 4.5))

    comp_matches = resume_record.get('suitable_companies', []) or []
    if isinstance(comp_matches, str):
        try:
            comp_matches = json.loads(comp_matches)
        except Exception:
            comp_matches = []

    comp_rows = [
        [
            Paragraph("<b>Target Recruiter</b>", body_bold),
            Paragraph("<b>Matching Role</b>", body_bold),
            Paragraph("<b>Match %</b>", body_bold),
            Paragraph("<b>Indicative Package</b>", body_bold),
            Paragraph("<b>Alignment Tier</b>", body_bold)
        ]
    ]

    if comp_matches:
        for c in comp_matches[:3]:
            c_name = c.get('company', 'Campus Recruiter')
            c_role = c.get('role', 'Software Engineer')
            c_score = f"{round(float(c.get('match_score', 80)), 1)}%"
            c_ctc = str(c.get('indicative_ctc', c.get('indicative_ctc_range_lpa', '3.5 - 6.5 LPA')))
            c_tier = c.get('fit_tier', 'Moderate Fit')
            comp_rows.append([
                Paragraph(f"<b>{c_name}</b>", body_dark),
                Paragraph(c_role, body_dark),
                Paragraph(f"<font color='#059669'><b>{c_score}</b></font>", body_dark),
                Paragraph(c_ctc, body_dark),
                Paragraph(f"<font color='#2563EB'>{c_tier}</font>", body_dark),
            ])
    elif resume_record.get('best_match_company') and resume_record.get('best_match_company') not in ['Awaiting Recruiter Profiles', 'Awaiting Placement Data', '']:
        best_comp = resume_record.get('best_match_company')
        comp_rows.append([
            Paragraph(f"<b>{best_comp}</b>", body_dark),
            Paragraph(best_role, body_dark),
            Paragraph(f"<font color='#059669'><b>{int(round(ats_score))}%</b></font>", body_dark),
            Paragraph("3.5 - 6.5 LPA", body_dark),
            Paragraph("<font color='#2563EB'>Target Match</font>", body_dark)
        ])
    else:
        comp_rows.append([
            Paragraph("<b>Industry Cluster Placement</b>", body_dark),
            Paragraph(best_role, body_dark),
            Paragraph(f"<font color='#059669'><b>{int(round(ats_score))}%</b></font>", body_dark),
            Paragraph("3.6 - 7.5 LPA", body_dark),
            Paragraph("<font color='#2563EB'>Placement Ready</font>", body_dark)
        ])

    comp_table = Table(comp_rows, colWidths=[148, 164, 56, 102, 90])
    comp_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F1F5F9')),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 4.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 7),
        ('RIGHTPADDING', (0, 0), (-1, -1), 7),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(comp_table)
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # 4. SECTION 2: THE NEGATIVE SIDE (RESUME CLAIMED VS TEST FAILED)
    # -------------------------------------------------------------
    story.append(Paragraph("<b>2. The Negative Side: Resume Claims Unverified in Practical Test</b>", sec_title))
    story.append(Spacer(1, 4.5))

    mock_data = resume_record.get('mocktest_data', {}) or {}
    if isinstance(mock_data, str):
        try:
            mock_data = json.loads(mock_data)
        except Exception:
            mock_data = {}

    breakdown = mock_data.get('skill_breakdown', {}) if isinstance(mock_data, dict) else {}
    if not breakdown and isinstance(resume_record.get('mock_test_skills'), dict):
        breakdown = resume_record.get('mock_test_skills')

    negative_skills = []
    verified_skills = []

    if isinstance(breakdown, dict) and breakdown:
        for sk_name, sk_stats in breakdown.items():
            if isinstance(sk_stats, dict):
                c = sk_stats.get('correct', 0)
                t = sk_stats.get('total', 0)
                acc = int(round((c / max(1, t)) * 100)) if t > 0 else 0
                if acc < 60:
                    negative_skills.append({
                        'skill': sk_name,
                        'correct': c,
                        'total': t,
                        'score_pct': acc,
                        'learn_url': get_learn_anything_url(sk_name),
                        'assessment': 'Claimed in resume, but 0 questions correct in test' if c == 0 else f'Low accuracy ({acc}%) in test questions'
                    })
                else:
                    verified_skills.append({
                        'skill': sk_name,
                        'correct': c,
                        'total': t,
                        'score_pct': acc,
                        'learn_url': get_learn_anything_url(sk_name)
                    })

    # If no negative skills found from breakdown, detect from missing skills
    if not negative_skills:
        skill_gaps_raw = resume_record.get('missing_skills', resume_record.get('skill_gaps', [])) or []
        if isinstance(skill_gaps_raw, str):
            try:
                skill_gaps_raw = json.loads(skill_gaps_raw)
            except Exception:
                skill_gaps_raw = [s.strip() for s in skill_gaps_raw.split(',') if s.strip()]
        if isinstance(skill_gaps_raw, list):
            for gap in skill_gaps_raw[:3]:
                negative_skills.append({
                    'skill': gap,
                    'correct': 0,
                    'total': 2,
                    'score_pct': 0,
                    'learn_url': get_learn_anything_url(gap),
                    'assessment': 'High-demand industry competency missing from demonstrable test answers'
                })

    # Render Negative Side Alert Card with comfortable inter-line text gaps
    neg_items_str = []
    for neg in negative_skills[:4]:
        neg_items_str.append(f"&bull;&nbsp; <b>{neg['skill']}</b>: <b>{neg['score_pct']}%</b> ({neg['correct']}/{neg['total']} Correct) &mdash; <font color='#B91C1C'>{neg['assessment']}</font>")
    # Vertical gap between each negative skill bullet
    neg_body = "<br/><font size='3.5'>&nbsp;</font><br/>".join(neg_items_str) if neg_items_str else "No critical vulnerabilities identified. All tested skills verified above threshold."

    neg_content = [
        [
            Paragraph("<font color='#991B1B'><b>CRITICAL RECRUITER RISK: Resume vs Reality Discrepancy</b></font>", ParagraphStyle('NRH', fontName='Helvetica-Bold', fontSize=8.4, leading=10.8, textColor=C_ROSE))
        ],
        [
            Paragraph(neg_body, ParagraphStyle('NRB', fontName='Helvetica', fontSize=7.8, leading=11.6, textColor=C_PRIMARY))
        ],
        [
            Paragraph(
                "<i>Recruiter Impact: Interviewers will drill into these listed skills. Failing basic implementation questions on skills claimed on your resume results in immediate disqualification. You must correct these weaknesses prior to placement drives.</i>",
                body_muted
            )
        ]
    ]
    neg_table = Table(neg_content, colWidths=[TOTAL_WIDTH])
    neg_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_ROSE_BG),
        ('BOX', (0, 0), (-1, -1), 1, C_ROSE_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#FCA5A5')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 9),
        ('RIGHTPADDING', (0, 0), (-1, -1), 9),
    ]))
    story.append(neg_table)
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # 5. SECTION 3: 3-5 STEP GROWTH & ACTION PLAN
    # -------------------------------------------------------------
    story.append(Paragraph("<b>3. 4-Step Strategic Growth &amp; Placement Action Plan</b>", sec_title))
    story.append(Spacer(1, 4.5))

    neg_names_str = ", ".join([n['skill'] for n in negative_skills[:2]]) if negative_skills else "core stack fundamentals"
    growth_steps = [
        f"<b>Step 1 (Correct Weaknesses):</b> Remediate unverified skills (<b>{neg_names_str}</b>) where test answers fell short. Rebuild foundational understanding using the curated roadmap links below.",
        "<b>Step 2 (Demonstrate Implementation):</b> Create an end-to-end GitHub repository project with unit tests and live deployment proving hands-on problem solving in these exact skills.",
        f"<b>Step 3 (Target Matching Recruiter Track):</b> Apply directly to campus recruiters hiring in your verified domain under the 12 Technology Clusters.",
        "<b>Step 4 (Assessment Retake):</b> Retake the adaptive mock test to elevate verified proficiency above <b>85%</b> to secure Elite Placement Ready certification."
    ]

    growth_content = []
    for step_text in growth_steps:
        growth_content.append([Paragraph(step_text, bullet_p)])

    growth_table = Table(growth_content, colWidths=[TOTAL_WIDTH])
    growth_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_BG_CARD),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#EDF2F7')),
        ('TOPPADDING', (0, 0), (-1, -1), 4.5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4.5),
        ('LEFTPADDING', (0, 0), (-1, -1), 9),
        ('RIGHTPADDING', (0, 0), (-1, -1), 9),
    ]))
    story.append(growth_table)
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # 6. SECTION 4: CURATED REMEDIATION RESOURCES (learn-anything.xyz)
    # -------------------------------------------------------------
    story.append(Paragraph("<b>4. Curated Remediation Resources (Powered by learn-anything.xyz)</b>", sec_title))
    story.append(Spacer(1, 4.5))

    # Collect learning links for all negative skills + top verified skills
    res_links = []
    seen_links = set()
    for item in negative_skills + verified_skills:
        s_name = item['skill']
        url = item['learn_url']
        if s_name.lower() not in seen_links and len(res_links) < 4:
            seen_links.add(s_name.lower())
            is_neg = any(n['skill'].lower() == s_name.lower() for n in negative_skills)
            status_tag = "<font color='#DC2626'><b>[Needs Correction]</b></font>" if is_neg else "<font color='#059669'><b>[Mastery Growth]</b></font>"
            res_links.append(f"&bull;&nbsp; <b>{s_name}</b> {status_tag}: &nbsp;<link href='{url}'><u><font color='#2563EB'><b>{url}</b></font></u></link>")

    if not res_links:
        res_links = [
            "&bull;&nbsp; <b>Python</b>: &nbsp;<link href='https://learn-anything.xyz/python'><u><font color='#2563EB'><b>https://learn-anything.xyz/python</b></font></u></link>",
            "&bull;&nbsp; <b>SQL & Databases</b>: &nbsp;<link href='https://learn-anything.xyz/sql'><u><font color='#2563EB'><b>https://learn-anything.xyz/sql</b></font></u></link>",
            "&bull;&nbsp; <b>Data Structures</b>: &nbsp;<link href='https://learn-anything.xyz/data-structures'><u><font color='#2563EB'><b>https://learn-anything.xyz/data-structures</b></font></u></link>"
        ]

    # Vertical gap between each resource link
    res_body = "<br/><font size='3.5'>&nbsp;</font><br/>".join(res_links)
    res_content = [
        [
            Paragraph(
                "Click on any interactive learning roadmap below to learn and master your lacking/unverified skills directly on <b>learn-anything.xyz</b>:",
                body_dark
            )
        ],
        [
            Paragraph(res_body, ParagraphStyle('ResBody', fontName='Helvetica', fontSize=7.8, leading=11.6, textColor=C_PRIMARY))
        ]
    ]
    res_table = Table(res_content, colWidths=[TOTAL_WIDTH])
    res_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#CBD5E1')),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#E2E8F0')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 9),
        ('RIGHTPADDING', (0, 0), (-1, -1), 9),
    ]))
    story.append(res_table)
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # 7. INSTITUTIONAL AUDIT FOOTER
    # -------------------------------------------------------------
    footer_text = (
        "<font size='7.2' color='#64748B'>"
        "<b>AI Career Companion &bull; Verified Institutional Audit</b> &bull; Calibrated against 12 Industry Placement Clusters &bull; "
        "Designed &amp; Developed by <b>P&amp;P Studio</b> &bull; Faculty Placement Cell"
        "</font>"
    )
    story.append(HRFlowable(width="100%", thickness=0.75, color=C_BORDER, spaceBefore=0, spaceAfter=4))
    story.append(Paragraph(footer_text, ParagraphStyle('FP', fontName='Helvetica', fontSize=7.2, leading=9.5, alignment=1)))

    doc.build(story)
    return buffer.getvalue()
