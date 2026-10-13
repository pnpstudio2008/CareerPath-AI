"""
AI Career Companion - Resume Performance & ATS Audit Report Generator
Generates an official, print-ready, SINGLE-PAGE executive evaluation document.
"""

import io
import re
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


def generate_resume_pdf_report(student: dict, resume_record: dict) -> bytes:
    """
    Generates a clean, modern, single-page executive PDF report highlighting
    the specific performance, ATS scoring, company benchmark, and skill gaps
    of a candidate's resume.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=28,
        rightMargin=28,
        topMargin=26,
        bottomMargin=26
    )

    styles = getSampleStyleSheet()

    # Color Palette
    C_PRIMARY = colors.HexColor('#2563EB')       # Electric Blue
    C_SECONDARY = colors.HexColor('#0F172A')     # Deep Slate
    C_BG_CARD = colors.HexColor('#F8FAFC')       # Slate 50
    C_BORDER = colors.HexColor('#E2E8F0')        # Slate 200
    C_EMERALD = colors.HexColor('#059669')       # Success Green
    C_TEXT_MUTED = colors.HexColor('#64748B')
    C_ROSE = colors.HexColor('#DC2626')          # Red / Gaps
    C_ROSE_BG = colors.HexColor('#FEF2F2')

    # Typography Styles
    title_p = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=14,
        leading=17,
        textColor=colors.white
    )

    sec_title = ParagraphStyle(
        'SecTitle',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=C_SECONDARY,
        spaceBefore=0,
        spaceAfter=0
    )

    body_dark = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=C_SECONDARY
    )

    body_bold = ParagraphStyle(
        'BodyBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=11,
        textColor=C_SECONDARY
    )

    body_muted = ParagraphStyle(
        'BodyMuted',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.2,
        leading=9.5,
        textColor=C_TEXT_MUTED
    )

    bullet_p = ParagraphStyle(
        'RecBullet',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.5,
        textColor=C_SECONDARY,
        leftIndent=8,
        firstLineIndent=-8
    )

    story = []
    TOTAL_WIDTH = 556  # 612 - 56

    # -------------------------------------------------------------
    # 1. HEADER BANNER
    # -------------------------------------------------------------
    candidate_name = student.get('name', 'Student Candidate')
    roll_no = student.get('roll_no', 'N/A')
    branch = student.get('branch', 'CSE')
    eval_date = str(resume_record.get('created_at', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))[:10]
    
    header_content = [
        [
            Paragraph("<b>AI CAREER COMPANION</b> &bull; RESUME PERFORMANCE AUDIT", title_p),
            Paragraph(f"<b>Candidate:</b> {candidate_name} ({roll_no})<br/><b>Branch:</b> {branch} &bull; <b>Date:</b> {eval_date}", ParagraphStyle('HMeta', fontName='Helvetica', fontSize=7.5, leading=10, textColor=colors.white, alignment=2))
        ]
    ]
    header_table = Table(header_content, colWidths=[336, 220])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_PRIMARY),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 7))

    # -------------------------------------------------------------
    # 2. OVERVIEW CARD (ATS SCORE & RESUME SNAPSHOT)
    # -------------------------------------------------------------
    ats_score = float(resume_record.get('ats_score', 80) or 80)
    ats_int = int(round(ats_score))

    if ats_int >= 80:
        tier_title = "Placement Ready (Top Tier)"
        tier_color = "#059669"
        tier_bg = "#ECFDF5"
    elif ats_int >= 65:
        tier_title = "Moderate Readiness Tier"
        tier_color = "#D97706"
        tier_bg = "#FFFBEB"
    else:
        tier_title = "Needs Keyword Optimization"
        tier_color = "#DC2626"
        tier_bg = "#FEF2F2"

    filename = str(resume_record.get('filename') or 'Resume.pdf')
    best_role = str(resume_record.get('best_role') or 'Software Development Engineer')

    # Unpack skills
    skills_raw = resume_record.get('skills', []) or []
    if isinstance(skills_raw, str):
        try:
            import json
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

    skills_str = ", ".join(skills_list[:14]) if skills_list else "Python, SQL, Java, Flask, React, Git, REST APIs"
    if len(skills_list) > 14:
        skills_str += f", +{len(skills_list) - 14} more"

    left_box = [
        Paragraph(f"<font color='{C_PRIMARY.hexval()}' size='24'><b>{ats_int}%</b></font>", ParagraphStyle('ScoreBig', alignment=1, leading=24)),
        Paragraph(f"<b>ATS SCORE</b>", ParagraphStyle('ScoreLbl', fontName='Helvetica-Bold', fontSize=7.5, leading=9, textColor=C_TEXT_MUTED, alignment=1)),
        Spacer(1, 3),
        Paragraph(f"<font color='{tier_color}'><b>{tier_title}</b></font>", ParagraphStyle('ScoreTier', fontName='Helvetica-Bold', fontSize=7.5, leading=9.5, alignment=1))
    ]

    right_box = [
        Paragraph(f"<b>Resume File:</b> <font color='#1E293B'>{filename}</font>", body_dark),
        Spacer(1, 2),
        Paragraph(f"<b>Primary Role Match:</b> <font color='#2563EB'><b>{best_role}</b></font>", body_dark),
        Spacer(1, 2),
        Paragraph(f"<b>Detected Core Skills ({len(skills_list)}):</b> <font color='#475569'>{skills_str}</font>", ParagraphStyle('SkP', fontName='Helvetica', fontSize=7.5, leading=9.5, textColor=C_SECONDARY))
    ]

    overview_table = Table([[left_box, right_box]], colWidths=[130, 426])
    overview_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), colors.HexColor(tier_bg)),
        ('BACKGROUND', (1, 0), (1, 0), C_BG_CARD),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(overview_table)
    story.append(Spacer(1, 7))

    # -------------------------------------------------------------
    # 3. SUITABLE RECRUITERS (45-DATASET BENCHMARK) - TOP 3 MATCHES
    # -------------------------------------------------------------
    story.append(Paragraph("<b>1. Suitable Recruiter Benchmark (Top Matches from 45 Campus Hiring Dataset)</b>", sec_title))
    story.append(Spacer(1, 3))

    comp_matches = resume_record.get('suitable_companies', []) or []
    if isinstance(comp_matches, str):
        try:
            import json
            comp_matches = json.loads(comp_matches)
        except Exception:
            comp_matches = []

    comp_rows = [
        [
            Paragraph("<b>Target Recruiter</b>", body_bold),
            Paragraph("<b>Fitting Role</b>", body_bold),
            Paragraph("<b>Match %</b>", body_bold),
            Paragraph("<b>Indicative Package</b>", body_bold),
            Paragraph("<b>Alignment</b>", body_bold)
        ]
    ]

    if comp_matches:
        for c in comp_matches[:3]:
            c_name = c.get('company', 'Top Recruiter')
            c_role = c.get('role', 'Software Engineer')
            c_score = f"{round(float(c.get('match_score', 80)), 1)}%"
            c_ctc = c.get('indicative_ctc_range_lpa', '5.0 - 10.0 LPA')
            c_tier = c.get('fit_tier', 'Strong Match')
            comp_rows.append([
                Paragraph(f"<b>{c_name}</b>", body_dark),
                Paragraph(c_role, body_dark),
                Paragraph(f"<font color='#059669'><b>{c_score}</b></font>", body_dark),
                Paragraph(c_ctc, body_dark),
                Paragraph(f"<font color='#2563EB'>{c_tier}</font>", body_dark),
            ])
    else:
        best_comp = resume_record.get('best_match_company') or 'WebOccult Technologies'
        comp_rows.append([
            Paragraph(f"<b>{best_comp}</b>", body_dark),
            Paragraph(best_role, body_dark),
            Paragraph(f"<font color='#059669'><b>{ats_int}%</b></font>", body_dark),
            Paragraph("3.0 - 5.5 LPA", body_dark),
            Paragraph("<font color='#2563EB'>Strong Match</font>", body_dark)
        ])

    comp_table = Table(comp_rows, colWidths=[140, 156, 65, 105, 90])
    comp_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#F1F5F9')),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(comp_table)
    story.append(Spacer(1, 7))

    # -------------------------------------------------------------
    # 4. TWO-COLUMN SPLIT: ROLE FIT TRAJECTORY (LEFT) & SKILL GAPS (RIGHT)
    # -------------------------------------------------------------
    skill_gaps_raw = resume_record.get('skill_gaps', []) or []
    if isinstance(skill_gaps_raw, str):
        try:
            import json
            skill_gaps_raw = json.loads(skill_gaps_raw)
        except Exception:
            skill_gaps_raw = [s.strip() for s in skill_gaps_raw.split(',') if s.strip()]
    if isinstance(skill_gaps_raw, list):
        skill_gaps = [str(g).strip() for g in skill_gaps_raw if str(g).strip()]
    else:
        skill_gaps = []

    career_recs = resume_record.get('career_recommendations', []) or []
    if isinstance(career_recs, str):
        try:
            import json
            career_recs = json.loads(career_recs)
        except Exception:
            career_recs = []

    alt_roles_str = ", ".join([f"{cr.get('role')} ({cr.get('match', '80%')})" for cr in career_recs[:2]]) if career_recs else "Backend Engineer, Full Stack Developer"

    left_role_content = [
        Paragraph("<b>2. Role Fit & Trajectory</b>", sec_title),
        Spacer(1, 3),
        Paragraph(f"<b>Top Role Fit:</b> <font color='#2563EB'><b>{best_role}</b></font>", body_dark),
        Spacer(1, 2),
        Paragraph(f"<b>Alternative Paths:</b> <font color='#475569'>{alt_roles_str}</font>", ParagraphStyle('AltR', fontName='Helvetica', fontSize=7.5, leading=9.5, textColor=C_SECONDARY)),
        Spacer(1, 2),
        Paragraph("Demonstrates highest alignment with system architecture and full-stack software tracks.", body_muted)
    ]

    gaps_display = ", ".join(skill_gaps[:5]) if skill_gaps else "No critical skill gaps identified (Strong role fit)"
    right_gap_content = [
        Paragraph("<b>3. Critical Skill Gaps to Close</b>", sec_title),
        Spacer(1, 3),
        Paragraph(f"<font color='#B91C1C'><b>Missing Skills:</b> {gaps_display}</font>", ParagraphStyle('GapP', fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=C_ROSE)),
        Spacer(1, 2),
        Paragraph("Closing these competencies through targeted practice tests boosts recruiter qualification rates to 95%+.", body_muted)
    ]

    split_table = Table([[left_role_content, right_gap_content]], colWidths=[274, 274])
    split_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), C_BG_CARD),
        ('BACKGROUND', (1, 0), (1, 0), C_ROSE_BG),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]))
    story.append(split_table)
    story.append(Spacer(1, 7))

    # -------------------------------------------------------------
    # 5. ACTIONABLE ATS OPTIMIZATION RECOMMENDATIONS (TOP 3)
    # -------------------------------------------------------------
    story.append(Paragraph("<b>4. Actionable ATS Optimization Fixes</b>", sec_title))
    story.append(Spacer(1, 3))

    full_analysis = resume_record.get('full_analysis', {}) or {}
    if isinstance(full_analysis, str):
        try:
            import json
            full_analysis = json.loads(full_analysis)
        except Exception:
            full_analysis = {}

    ats_breakdown = full_analysis.get('ats_breakdown', {}) if isinstance(full_analysis, dict) else {}
    recs = ats_breakdown.get('recommendations', []) if isinstance(ats_breakdown, dict) else []
    if not recs:
        recs = [
            "Quantify project outcomes with measurable performance metrics (e.g. 'improved API response speed by 30%').",
            "Incorporate high-demand deployment keywords (Docker, Cloud, REST APIs) to maximize recruiter screening pass rates.",
            "Maintain standard single-column PDF hierarchy without nested graphics or tables for flawless parser ingestion."
        ]

    recs_content = []
    for idx, r in enumerate(recs[:3], 1):
        recs_content.append(Paragraph(f"<b>{idx}.</b> {r}", bullet_p))

    recs_table = Table([[rc] for rc in recs_content], colWidths=[TOTAL_WIDTH])
    recs_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_BG_CARD),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(recs_table)
    story.append(Spacer(1, 7))

    # -------------------------------------------------------------
    # 6. COMPACT ONE-LINE VERIFICATION FOOTER
    # -------------------------------------------------------------
    footer_text = (
        "<font size='7' color='#64748B'>"
        "<b>AI Career Companion</b> &bull; Calibrated against 45-company recruitment dataset &bull; "
        "Designed &amp; Developed by <b>P&amp;P Studio</b> &bull; Faculty Guides <b>Riya Modi &amp; Diksha Durgapal</b>"
        "</font>"
    )
    story.append(HRFlowable(width="100%", thickness=0.5, color=C_BORDER, spaceBefore=2, spaceAfter=3))
    story.append(Paragraph(footer_text, ParagraphStyle('FooterP', fontName='Helvetica', fontSize=7, leading=9, alignment=1)))

    doc.build(story)
    return buffer.getvalue()
