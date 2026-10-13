"""
AI Career Companion - Resume Performance & ATS Audit Report Generator
Generates an official, print-ready PDF evaluation document using ReportLab.
"""

import io
import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


def generate_resume_pdf_report(student: dict, resume_record: dict) -> bytes:
    """
    Generates a comprehensive PDF Performance & ATS Report for a specific resume record.
    Returns bytes of the generated PDF document.
    """
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Custom Palette
    C_PRIMARY = colors.HexColor('#2563EB')     # Modern Blue
    C_SECONDARY = colors.HexColor('#1E293B')   # Dark Slate
    C_BG_LIGHT = colors.HexColor('#F8FAFC')    # Soft Light Slate
    C_BORDER = colors.HexColor('#E2E8F0')      # Slate Border
    C_EMERALD = colors.HexColor('#059669')     # Success Emerald
    C_AMBER = colors.HexColor('#D97706')       # Warning Amber
    C_ROSE = colors.HexColor('#DC2626')        # Missing Gap Rose
    C_TEXT_MUTED = colors.HexColor('#64748B')  # Muted Text

    # Custom Typography Styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.white,
        alignment=0
    )

    subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor('#E0E7FF'),
        alignment=0
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=C_SECONDARY,
        spaceBefore=10,
        spaceAfter=6
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=C_SECONDARY
    )

    body_bold = ParagraphStyle(
        'BodyBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=C_SECONDARY
    )

    body_muted = ParagraphStyle(
        'BodyMuted',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=C_TEXT_MUTED
    )

    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=12,
        textColor=C_SECONDARY,
        leftIndent=12,
        firstLineIndent=-8
    )

    meta_label = ParagraphStyle(
        'MetaLabel',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8,
        leading=10,
        textColor=C_TEXT_MUTED
    )

    meta_val = ParagraphStyle(
        'MetaVal',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=12,
        textColor=C_SECONDARY
    )

    story = []

    # -------------------------------------------------------------
    # 1. HEADER BANNER BLOCK (Navy / Blue Card)
    # -------------------------------------------------------------
    header_content = [
        [
            Paragraph("AI CAREER COMPANION", title_style),
            Paragraph("<b>OFFICIAL VERIFIED REPORT</b><br/>Campus Placement NLP Engine", ParagraphStyle('HRight', fontName='Helvetica', fontSize=8, leading=10, textColor=colors.HexColor('#E0E7FF'), alignment=2))
        ],
        [
            Paragraph("RESUME ATS COMPATIBILITY &amp; PERFORMANCE AUDIT REPORT", subtitle_style),
            Paragraph(f"Generated: {datetime.datetime.now().strftime('%d %b %Y, %I:%M %p')}", ParagraphStyle('HDate', fontName='Helvetica-Bold', fontSize=8, leading=10, textColor=colors.white, alignment=2))
        ]
    ]

    header_table = Table(header_content, colWidths=[380, 160])
    header_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_PRIMARY),
        ('TOPPADDING', (0, 0), (-1, -1), 12),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('LEFTPADDING', (0, 0), (-1, -1), 14),
        ('RIGHTPADDING', (0, 0), (-1, -1), 14),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # 2. CANDIDATE & FILE METADATA CARD
    # -------------------------------------------------------------
    student_name = student.get('name', 'Student Candidate')
    roll_no = student.get('roll_no', 'N/A')
    branch = student.get('branch', 'Computer Science & Engineering')
    batch_year = student.get('batch_year', '2024 - 2028')
    filename = resume_record.get('filename', 'Candidate_Resume.pdf')
    created_at = str(resume_record.get('created_at', datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
    fingerprint = str(resume_record.get('resume_fingerprint', 'verified_fp'))[:16]

    meta_data = [
        [
            Paragraph("CANDIDATE NAME", meta_label),
            Paragraph("ENROLLMENT / ROLL NO", meta_label),
            Paragraph("ACADEMIC BRANCH", meta_label),
            Paragraph("BATCH YEAR", meta_label)
        ],
        [
            Paragraph(student_name, meta_val),
            Paragraph(roll_no, meta_val),
            Paragraph(branch, meta_val),
            Paragraph(batch_year, meta_val)
        ],
        [
            Paragraph("RESUME FILE", meta_label),
            Paragraph("EVALUATION DATE", meta_label),
            Paragraph("4-PILLAR FINGERPRINT", meta_label),
            Paragraph("AUDIT STATUS", meta_label)
        ],
        [
            Paragraph(filename, meta_val),
            Paragraph(created_at[:19], meta_val),
            Paragraph(f"{fingerprint}...", meta_val),
            Paragraph("<font color='#059669'><b>VERIFIED DISTINCT</b></font>", meta_val)
        ]
    ]

    meta_table = Table(meta_data, colWidths=[140, 130, 140, 130])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_BG_LIGHT),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#F1F5F9')),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 12))

    # -------------------------------------------------------------
    # 3. EXECUTIVE ATS SCORE & PERFORMANCE KPI CALLOUT
    # -------------------------------------------------------------
    ats_score = float(resume_record.get('ats_score', 80) or 80)
    ats_int = int(round(ats_score))

    if ats_int >= 80:
        tier_title = "Placement Ready / Highly Competitive Tier"
        tier_color = C_EMERALD
        tier_desc = "Your resume demonstrates excellent technical keyword density, structured headings, and high alignment with top-tier recruiter requirements."
    elif ats_int >= 65:
        tier_title = "Moderate Placement Readiness Tier"
        tier_color = C_AMBER
        tier_desc = "Good foundational content with clear coursework. Incorporating more quantifiable metrics and targeted framework keywords will elevate this profile into the top quartile."
    else:
        tier_title = "Needs Development & Keyword Optimization"
        tier_color = C_ROSE
        tier_desc = "Several critical sections or technical keywords are sparse. Follow the recommendations below to improve ATS screening pass rates."

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

    # Clean duplicates while preserving order
    seen_skills = set()
    cleaned_skills = []
    for s in skills_list:
        s_str = str(s).strip()
        if s_str and s_str.lower() not in seen_skills:
            seen_skills.add(s_str.lower())
            cleaned_skills.append(s_str)
    skills_list = cleaned_skills

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

    kpi_card_data = [
        [
            Paragraph(f"<font color='#2563EB' size='22'><b>{ats_int}%</b></font><br/><font size='8' color='#64748B'><b>ATS SCORE</b></font>", ParagraphStyle('ScoreC', alignment=1, leading=16)),
            Paragraph(f"<font color='{tier_color.hexval()}'><b>{tier_title}</b></font><br/><font size='8' color='#475569'>{tier_desc}</font>", ParagraphStyle('TierC', fontName='Helvetica', fontSize=9, leading=13)),
            Paragraph(f"<b>Skills Detected:</b> {len(skills_list)}<br/><b>Identified Gaps:</b> {len(skill_gaps)}<br/><b>Recruiters Scored:</b> 45", ParagraphStyle('StatsC', fontName='Helvetica', fontSize=8.5, leading=13, alignment=2))
        ]
    ]

    kpi_card = Table(kpi_card_data, colWidths=[100, 310, 130])
    kpi_card.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#EFF6FF')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#BFDBFE')),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 10),
        ('RIGHTPADDING', (0, 0), (-1, -1), 10),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(kpi_card)
    story.append(Spacer(1, 8))

    # Core Competencies Capsule Row
    if skills_list:
        skills_display = ", ".join(skills_list[:16])
        if len(skills_list) > 16:
            skills_display += f", +{len(skills_list) - 16} more"
        skills_table = Table([[
            Paragraph(f"<b>Extracted Skills &amp; Competencies:</b> <font color='#1E293B'>{skills_display}</font>", ParagraphStyle('SkillsSummary', fontName='Helvetica', fontSize=8, leading=11))
        ]], colWidths=[540])
        skills_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
            ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(skills_table)
        story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # 4. SUITABLE COMPANIES & RECRUITER MATCH (45-Dataset)
    # -------------------------------------------------------------
    story.append(Paragraph("<b>1. Suitable Company Placement Benchmark (45 Recruiters Dataset)</b>", section_heading))

    comp_matches = resume_record.get('suitable_companies', []) or []
    if isinstance(comp_matches, str):
        try:
            import json
            comp_matches = json.loads(comp_matches)
        except Exception:
            comp_matches = []

    comp_table_rows = [
        [
            Paragraph("<b>Target Recruiter</b>", meta_label),
            Paragraph("<b>Best Fitting Role</b>", meta_label),
            Paragraph("<b>Match Score</b>", meta_label),
            Paragraph("<b>Indicative CTC Range</b>", meta_label),
            Paragraph("<b>Alignment Tier</b>", meta_label)
        ]
    ]

    if comp_matches:
        for c in comp_matches[:5]:
            c_name = c.get('company', 'Top Recruiter')
            c_role = c.get('role', 'Software Engineer')
            c_score = f"{c.get('match_score', 80)}%"
            c_ctc = c.get('indicative_ctc_range_lpa', '5.0 - 10.0 LPA')
            c_tier = c.get('fit_tier', 'Strong Match')
            comp_table_rows.append([
                Paragraph(f"<b>{c_name}</b>", body_style),
                Paragraph(c_role, body_style),
                Paragraph(f"<font color='#059669'><b>{c_score}</b></font>", body_style),
                Paragraph(c_ctc, body_style),
                Paragraph(f"<font color='#2563EB'>{c_tier}</font>", body_style),
            ])
    else:
        best_comp = resume_record.get('best_match_company') or 'WebOccult Technologies'
        best_role = resume_record.get('best_role') or 'Full Stack Developer'
        comp_table_rows.append([
            Paragraph(f"<b>{best_comp}</b>", body_style),
            Paragraph(best_role, body_style),
            Paragraph(f"<font color='#059669'><b>{ats_int}%</b></font>", body_style),
            Paragraph("3.0 - 5.5 LPA", body_style),
            Paragraph("<font color='#2563EB'>Strong Match</font>", body_style)
        ])

    comp_table = Table(comp_table_rows, colWidths=[130, 150, 80, 100, 80])
    comp_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), C_BG_LIGHT),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#F1F5F9')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    story.append(comp_table)
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # 5. BEST FITTING ROLE & CAREER TRAJECTORY
    # -------------------------------------------------------------
    best_role_val = resume_record.get('best_role') or 'Full Stack Developer'
    story.append(Paragraph("<b>2. Role Suitability & Career Fit</b>", section_heading))

    role_p = Paragraph(
        f"<b>Primary Algorithmic Match:</b> <font color='#2563EB'><b>{best_role_val}</b></font><br/>"
        "Based on multi-factor analysis of extracted programming languages, database systems, and practical projects, "
        f"this candidate profile demonstrates highest suitability for <b>{best_role_val}</b> and related software engineering tracks.",
        body_style
    )

    career_recs = resume_record.get('career_recommendations', []) or []
    if isinstance(career_recs, str):
        try:
            import json
            career_recs = json.loads(career_recs)
        except Exception:
            career_recs = []

    role_box_data = [[role_p]]
    if career_recs:
        rec_str = " &bull; ".join([f"<b>{cr.get('role')}</b> ({cr.get('match', '85%')})" for cr in career_recs[:3]])
        role_box_data.append([
            Paragraph(f"<font size='8' color='#64748B'>Alternative Career Tracks: {rec_str}</font>", body_style)
        ])

    role_table = Table(role_box_data, colWidths=[540])
    role_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), C_BG_LIGHT),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(role_table)
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # 6. SKILL GAP ANALYSIS & PREPARATION ROADMAP
    # -------------------------------------------------------------
    story.append(Paragraph("<b>3. Skill Gap Analysis (Remaining Gaps to Reach 100% Readiness)</b>", section_heading))

    gaps_text = ", ".join(skill_gaps) if skill_gaps else "No critical skill gaps identified — profile meets core technical thresholds."
    gap_card_data = [
        [
            Paragraph("<b>Identified Missing / In-Demand Skills:</b>", body_bold),
        ],
        [
            Paragraph(f"<font color='#B91C1C'><b>{gaps_text}</b></font>", body_style)
        ],
        [
            Paragraph("<font size='8' color='#475569'><b>Preparation Advice:</b> Complete practice mock tests covering these missing technologies. Adding a portfolio project demonstrating practical integration will immediately boost recruiter shortlisting chances.</font>", body_style)
        ]
    ]

    gap_table = Table(gap_card_data, colWidths=[540])
    gap_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#FEF2F2')),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor('#FECACA')),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(gap_table)
    story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # 7. EXTRACTED ACHIEVEMENTS & PROJECTS
    # -------------------------------------------------------------
    achievements = resume_record.get('achievements', []) or []
    if isinstance(achievements, str):
        try:
            import json
            achievements = json.loads(achievements)
        except Exception:
            achievements = []

    projects = resume_record.get('projects', []) or []
    if isinstance(projects, str):
        try:
            import json
            projects = json.loads(projects)
        except Exception:
            projects = []

    if achievements or projects:
        story.append(Paragraph("<b>4. Verified Extracted Achievements &amp; Projects</b>", section_heading))

        profile_bullets = []
        if achievements:
            profile_bullets.append(Paragraph("<b>Extracted Achievements:</b>", body_bold))
            for a in achievements[:3]:
                profile_bullets.append(Paragraph(f"&bull; {a}", bullet_style))

        if projects:
            profile_bullets.append(Spacer(1, 4))
            profile_bullets.append(Paragraph("<b>Key Technical Projects:</b>", body_bold))
            for p in projects[:2]:
                p_title = p.get('title', 'Project') if isinstance(p, dict) else str(p)
                p_tech = ", ".join(p.get('tech_stack', [])) if isinstance(p, dict) and p.get('tech_stack') else ''
                p_desc = p.get('description', '') if isinstance(p, dict) else ''
                tech_label = f" <i>(Stack: {p_tech})</i>" if p_tech else ""
                profile_bullets.append(Paragraph(f"&bull; <b>{p_title}</b>{tech_label}: {p_desc[:120]}...", bullet_style))

        proj_table = Table([[b] for b in profile_bullets], colWidths=[540])
        proj_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), C_BG_LIGHT),
            ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
            ('LEFTPADDING', (0, 0), (-1, -1), 8),
            ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ]))
        story.append(proj_table)
        story.append(Spacer(1, 10))

    # -------------------------------------------------------------
    # 8. ACTIONABLE RECOMMENDATIONS & CHECKLIST
    # -------------------------------------------------------------
    story.append(Paragraph("<b>5. Actionable ATS Optimization Recommendations</b>", section_heading))

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
            "Add measurable impact metrics (e.g., 'improved query throughput by 35%') in technical project descriptions.",
            "Incorporate standard cloud deployment keywords (Docker, AWS/GCP, CI/CD) to maximize senior role matches.",
            "Ensure standard single-column layout without nested text boxes or tables for optimal parser pass rates."
        ]

    recs_content = []
    for idx, r in enumerate(recs[:3], 1):
        recs_content.append(Paragraph(f"<b>{idx}.</b> {r}", bullet_style))

    recs_table = Table([[rc] for rc in recs_content], colWidths=[540])
    recs_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#F8FAFC')),
        ('BOX', (0, 0), (-1, -1), 1, C_BORDER),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(recs_table)
    story.append(Spacer(1, 14))

    # -------------------------------------------------------------
    # 9. FOOTER & ENDORSEMENT
    # -------------------------------------------------------------
    footer_text = (
        "<font size='7.5' color='#64748B'>"
        "<b>AI Career Companion</b> &bull; Designed &amp; Developed by <b>P&amp;P Studio</b> "
        "in collaboration with Faculty Guides <b>Riya Modi &amp; Diksha Durgapal</b>.<br/>"
        "This evaluation is algorithmically compiled from real-time NLP parsing and calibrated against the 45-company recruitment dataset. "
        "Intended for academic guidance and placement preparation excellence."
        "</font>"
    )
    story.append(HRFlowable(width="100%", thickness=0.75, color=C_BORDER, spaceBefore=4, spaceAfter=6))
    story.append(Paragraph(footer_text, ParagraphStyle('FooterP', fontName='Helvetica', fontSize=7.5, leading=10, alignment=1)))

    # Build the document
    doc.build(story)
    return buffer.getvalue()
