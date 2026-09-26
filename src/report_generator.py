"""
HealthSathi - Comprehensive Wellness Report Generator
Produces structured multi-page PDF reports (via ReportLab) and print-ready rich HTML/Markdown views.
Complies with Section 6 structure (13 sections) and strict non-diagnostic safety disclaimers.
"""

import os
from typing import Dict, Any, List
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
)


def generate_pdf_report(
    user_data: Dict[str, Any],
    scores: Dict[str, Any],
    recommendations: List[Dict[str, Any]],
    routine: List[Dict[str, str]],
    plants: List[Dict[str, Any]],
    sources_df: Any,
    output_pdf_path: str
) -> str:
    os.makedirs(os.path.dirname(os.path.abspath(output_pdf_path)), exist_ok=True)
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        rightMargin=36,
        leftMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("DocTitle", parent=styles["Heading1"], fontName="Helvetica-Bold", fontSize=20, leading=24, textColor=colors.HexColor("#1e5128"), spaceAfter=4)
    subtitle_style = ParagraphStyle("DocSubtitle", parent=styles["Normal"], fontName="Helvetica", fontSize=10, leading=13, textColor=colors.HexColor("#555555"), spaceAfter=12)
    h2_style = ParagraphStyle("SectionHeading", parent=styles["Heading2"], fontName="Helvetica-Bold", fontSize=13, leading=16, textColor=colors.HexColor("#1e5128"), spaceBefore=10, spaceAfter=6)
    body_style = ParagraphStyle("BodyTextCustom", parent=styles["Normal"], fontName="Helvetica", fontSize=9, leading=12, textColor=colors.HexColor("#264653"))
    bold_label_style = ParagraphStyle("BoldLabel", parent=body_style, fontName="Helvetica-Bold")
    disclaimer_style = ParagraphStyle("DisclaimerText", parent=styles["Normal"], fontName="Helvetica-Oblique", fontSize=8, leading=11, textColor=colors.HexColor("#7f1d1d"))

    elements = []
    elements.append(Paragraph("HealthSathi — IKS Personalized Wellness Report", title_style))
    elements.append(Paragraph("A Data-Driven Framework for Personalized Lifestyle Analytics Grounded in Indian Knowledge Systems (Ayurveda)", subtitle_style))
    elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#1e5128"), spaceAfter=10))

    disclaimer_box = [[Paragraph(
        "<b>IMPORTANT SAFETY & NON-DIAGNOSTIC DISCLAIMER:</b> HealthSathi is an educational and lifestyle wellness prototype, "
        "not a medical diagnostic or prescription system. It does not diagnose clinical conditions, prescribe medications, "
        "replace licensed medical practitioners, or advise changing any ongoing medical treatment. All self-reported conditions "
        "are treated strictly as lifestyle context.", disclaimer_style
    )]]
    t_disc = Table(disclaimer_box, colWidths=[540])
    t_disc.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#fee2e2")),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#ef4444")),
        ("PADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(t_disc)
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("1. User Profile & Lifestyle Metrics", h2_style))
    conds_str = ", ".join(user_data.get("health_conditions", ["None"]))
    profile_data = [
        [Paragraph(f"<b>Age:</b> {user_data.get('age', '-')}", body_style), Paragraph(f"<b>Gender:</b> {user_data.get('gender', '-')}", body_style), Paragraph(f"<b>Height:</b> {user_data.get('height_cm', '-')} cm", body_style), Paragraph(f"<b>Weight:</b> {user_data.get('weight_kg', '-')} kg", body_style)],
        [Paragraph(f"<b>BMI:</b> {user_data.get('bmi', '-')} ({user_data.get('bmi_category', '-')})", body_style), Paragraph(f"<b>Occupation:</b> {user_data.get('occupation', '-')}", body_style), Paragraph(f"<b>Sleep:</b> {user_data.get('sleep_duration_hrs', '-')}h ({user_data.get('sleep_quality', '-')})", body_style), Paragraph(f"<b>Bedtime:</b> {user_data.get('sleep_time_raw', '-')}", body_style)],
        [Paragraph(f"<b>Activity:</b> {user_data.get('physical_activity_min', '-')} min/day", body_style), Paragraph(f"<b>Sunlight:</b> {user_data.get('outdoor_time_min', '-')} min/day", body_style), Paragraph(f"<b>Water Intake:</b> {user_data.get('water_intake_liters', '-')} L", body_style), Paragraph(f"<b>Screen Time:</b> {user_data.get('screen_time_hrs', '-')} hrs", body_style)],
        [Paragraph(f"<b>Stress Level:</b> {user_data.get('stress_level', '-')}/10", body_style), Paragraph(f"<b>Mood:</b> {user_data.get('mood', '-')}", body_style), Paragraph(f"<b>Relaxation:</b> {'Yes' if user_data.get('relaxation_activity') else 'No'}", body_style), Paragraph(f"<b>Meals:</b> {user_data.get('meal_regularity', '-')}", body_style)],
        [Paragraph(f"<b>Self-Reported Health Context:</b> {conds_str}", body_style), "", "", ""]
    ]
    t_profile = Table(profile_data, colWidths=[135, 135, 135, 135])
    t_profile.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("SPAN", (0, 4), (3, 4)),
        ("PADDING", (0, 0), (-1, -1), 4),
    ]))
    elements.append(t_profile)
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("2. Derived Lifestyle Wellness Scores", h2_style))
    score_rows = [
        [Paragraph("<b>Overall Lifestyle Wellness Score</b>", bold_label_style), Paragraph(f"<b>{scores.get('overall_wellness_score', 0.0)} / 100</b>", bold_label_style), Paragraph(f"<b>{scores.get('wellness_band', '-')}</b>", bold_label_style)],
        [Paragraph("Sleep Score", body_style), Paragraph(f"{scores.get('sleep_score', 0)} / 100", body_style), Paragraph("Evaluates duration, quality, and circadian bedtime alignment", body_style)],
        [Paragraph("Physical Activity Score", body_style), Paragraph(f"{scores.get('activity_score', 0)} / 100", body_style), Paragraph("Movement minutes and outdoor sunlight exposure vs. screen time", body_style)],
        [Paragraph("Stress Management Score", body_style), Paragraph(f"{scores.get('stress_score', 0)} / 100", body_style), Paragraph("Autonomic balance, emotional tone, and mindfulness pauses", body_style)],
        [Paragraph("Hydration Balance Score", body_style), Paragraph(f"{scores.get('hydration_score', 0)} / 100", body_style), Paragraph("Fluid intake calibrated to weight and metabolic demand", body_style)],
        [Paragraph("Routine Consistency Score", body_style), Paragraph(f"{scores.get('routine_score', 0)} / 100", body_style), Paragraph("Adherence to consistent wake-up, meal, and work schedules", body_style)],
        [Paragraph("Nutrition / Diet Score", body_style), Paragraph(f"{scores.get('nutrition_score', 0)} / 100", body_style), Paragraph("Fresh food frequency, breakfast habit, and stimulant moderation", body_style)],
    ]
    t_scores = Table(score_rows, colWidths=[180, 90, 270])
    t_scores.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
        ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#ffffff")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("PADDING", (0, 0), (-1, -1), 4),
    ]))
    elements.append(t_scores)
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("3. Personalized Dinacharya (Daily Routine Schedule)", h2_style))
    routine_rows = [[Paragraph("<b>Time</b>", bold_label_style), Paragraph("<b>Ayurvedic Phase</b>", bold_label_style), Paragraph("<b>Recommended Action & Guidance</b>", bold_label_style)]]
    for item in routine[:8]:
        routine_rows.append([
            Paragraph(f"<b>{item['time']}</b>", body_style),
            Paragraph(f"{item['phase']}<br/><font color='#666'>({item.get('dosha_focus', '')})</font>", body_style),
            Paragraph(f"<b>{item['activity']}</b>: {item['details']}", body_style)
        ])
    t_routine = Table(routine_rows, colWidths=[70, 130, 340])
    t_routine.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1e5128")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("PADDING", (0, 0), (-1, -1), 4),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#f8fafc"), colors.white])
    ]))
    elements.append(t_routine)
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("4. Curated IKS Recommendations & Explainability", h2_style))
    if recommendations:
        for idx, rec in enumerate(recommendations[:4], start=1):
            exp = rec.get("explainability", {})
            src = rec.get("source", {})
            rec_box = [
                [Paragraph(f"<b>Recommendation {idx}: {rec.get('principle_name')} ({rec.get('iks_concept')})</b>", bold_label_style)],
                [Paragraph(f"<b>Guideline:</b> {rec.get('recommendation_text')}", body_style)],
                [Paragraph(f"<b>Why am I getting this?</b> <font color='#c2410c'>{exp.get('user_trigger', '')}</font> {exp.get('reasoning', '')}", body_style)],
                [Paragraph(f"<b>Authentic Source:</b> {src.get('name', 'Ayurvedic Classical Text')} | Ref: {exp.get('primary_source', '')}", body_style)]
            ]
            t_rec = Table(rec_box, colWidths=[540])
            t_rec.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#f0fdf4")),
                ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#86efac")),
                ("PADDING", (0, 0), (-1, -1), 4),
            ]))
            elements.append(t_rec)
            elements.append(Spacer(1, 5))

    elements.append(Paragraph("5. Traditional Botanical Wellness Information (Educational Reference)", h2_style))
    plant_rows = [[Paragraph("<b>Botanical / Sanskrit</b>", bold_label_style), Paragraph("<b>Traditional System & Profile</b>", bold_label_style), Paragraph("<b>Modern Research Note & Cautions</b>", bold_label_style)]]
    for p in plants[:3]:
        plant_rows.append([
            Paragraph(f"<b>{p.get('common_name')}</b><br/><i>{p.get('scientific_name')}</i><br/>({p.get('sanskrit_name')})", body_style),
            Paragraph(f"{p.get('traditional_information')}<br/><b>Attributes:</b> {p.get('rasa_virya_vipaka')}", body_style),
            Paragraph(f"{p.get('modern_research_summary')}<br/><b>Caution:</b> <font color='#991b1b'>{p.get('safety_notes')}</font>", body_style)
        ])
    t_plants = Table(plant_rows, colWidths=[130, 205, 205])
    t_plants.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#e2e8f0")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#cbd5e1")),
        ("PADDING", (0, 0), (-1, -1), 4),
    ]))
    elements.append(t_plants)
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("6. Authentic Sources & Institutional References", h2_style))
    sources_summary = [
        "1. Ministry of Ayush — Ayush Research Portal (https://arp.ayush.gov.in/researchabout)",
        "2. World Health Organization (WHO) — Global Traditional Medicine Strategy 2025–2034",
        "3. Charaka Samhita — Sutrasthana Ch. 21 (Nidra / Sleep) & Ch. 27 (Annapanavidhi / Diet)",
        "4. Astanga Hridaya — Sutrasthana Ch. 2 (Dinacharya / Daily Circadian Regimen)"
    ]
    for s in sources_summary:
        elements.append(Paragraph(f"• {s}", body_style))
    elements.append(Spacer(1, 10))

    elements.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor("#cbd5e1"), spaceAfter=6))
    elements.append(Paragraph("<b>Notice:</b> Generated automatically by HealthSathi Prototype. Always consult qualified Ayurvedic physicians and medical doctors for healthcare diagnoses, therapeutic decisions, or medical management.", disclaimer_style))

    doc.build(elements)
    return output_pdf_path


def generate_markdown_report(user_data, scores, recommendations, routine, plants):
    conds = ", ".join(user_data.get("health_conditions", ["None"]))
    md = []
    md.append("# 🌿 HealthSathi — Personalized Wellness & Lifestyle Report")
    md.append("*(An IKS-Based Personalized Health and Lifestyle Analytics System)*\n")
    md.append("> **IMPORTANT SAFETY & NON-DIAGNOSTIC DISCLAIMER:**  \n> HealthSathi is an educational and wellness prototype, not a medical diagnosis or treatment system. It does not prescribe medications, diagnose disease, or replace consultation with qualified healthcare professionals. Self-reported health conditions are treated solely as lifestyle context.\n")
    md.append("---")
    md.append("## 1. User Profile & Lifestyle Summary")
    md.append(f"| Metric | Reported Value | Metric | Reported Value |")
    md.append(f"| :--- | :--- | :--- | :--- |")
    md.append(f"| **Age** | {user_data.get('age')} | **Gender** | {user_data.get('gender')} |")
    md.append(f"| **Height / Weight** | {user_data.get('height_cm')} cm / {user_data.get('weight_kg')} kg | **BMI** | {user_data.get('bmi')} ({user_data.get('bmi_category')}) |")
    md.append(f"| **Occupation** | {user_data.get('occupation')} | **Sleep Duration** | {user_data.get('sleep_duration_hrs')} hrs ({user_data.get('sleep_quality')}) |")
    md.append(f"| **Sleep / Wake Times** | {user_data.get('sleep_time_raw')} / {user_data.get('wake_up_time_raw')} | **Physical Activity** | {user_data.get('physical_activity_min')} min/day |")
    md.append(f"| **Water Intake** | {user_data.get('water_intake_liters')} L | **Screen Time** | {user_data.get('screen_time_hrs')} hrs/day |")
    md.append(f"| **Reported Stress** | {user_data.get('stress_level')}/10 ({user_data.get('mood')} mood) | **Outdoor Sunlight** | {user_data.get('outdoor_time_min')} min/day |")
    md.append(f"| **Meal Regularity** | {user_data.get('meal_regularity')} | **Breakfast Habit** | {'Regular' if user_data.get('breakfast_regular') else 'Skipped'} |")
    md.append(f"\n**Self-Reported Health Context:** `{conds}`\n")
    md.append("---")
    md.append("## 2. Derived Lifestyle Wellness Scores")
    md.append(f"### **Overall Lifestyle Wellness Score: {scores.get('overall_wellness_score')} / 100** — *{scores.get('wellness_band')}*")
    md.append(f"_{scores.get('wellness_summary')}_\n")

    md.append("| Dimension | Score | Primary Evaluation Rationale |")
    md.append("| :--- | :---: | :--- |")
    md.append(f"| **Sleep Score** | **{scores.get('sleep_score')} / 100** | Duration adequacy, rest quality, and Ratricharya bedtime alignment |")
    md.append(f"| **Activity Score** | **{scores.get('activity_score')} / 100** | Physical movement (Vyayama) and outdoor sunlight vs. screen strain |")
    md.append(f"| **Stress Management Score** | **{scores.get('stress_score')} / 100** | Autonomic calm, mood balance, and relaxation activity buffering |")
    md.append(f"| **Hydration Balance Score** | **{scores.get('hydration_score')} / 100** | Body mass and activity calibrated fluid intake (Ushnodaka) |")
    md.append(f"| **Routine Consistency Score** | **{scores.get('routine_score')} / 100** | Adherence to fixed meal windows and early morning rhythm |")
    md.append(f"| **Nutrition & Diet Score** | **{scores.get('nutrition_score')} / 100** | Fresh fruit/veg frequency, breakfast habit, and processed food avoidance |")

    md.append("\n---")
    md.append("## 3. Personalized Daily Routine (Dinacharya)")
    md.append("| Time | Ayurvedic Phase | Suggested Action | Classical Focus |")
    md.append("| :--- | :--- | :--- | :--- |")
    for item in routine:
        md.append(f"| **{item['time']}** | `{item['phase']}` | **{item['activity']}**: {item['details']} | _{item.get('dosha_focus', '')}_ |")

    md.append("\n---")
    md.append("## 4. Curated IKS Recommendations & Explainability")
    if recommendations:
        for idx, rec in enumerate(recommendations, 1):
            exp = rec.get("explainability", {})
            src = rec.get("source", {})
            md.append(f"### {idx}. {rec.get('principle_name')} (`{rec.get('iks_concept')}`)")
            md.append(f"- **Ayurvedic Guideline:** {rec.get('recommendation_text')}")
            md.append(f"- 🔍 **Why am I getting this recommendation?**")
            md.append(f"  - **Your Trigger:** *{exp.get('user_trigger')}*")
            md.append(f"  - **IKS Rationale:** {exp.get('reasoning')}")
            md.append(f"- 📖 **Authentic Source:** [{src.get('name')}]({src.get('url')}) — *Ref: {exp.get('primary_source')}*\n")

    md.append("---")
    md.append("## 5. Traditional Botanical Wellness Information (Educational Reference)")
    for p in plants:
        md.append(f"### 🌿 {p.get('common_name')} (*{p.get('scientific_name')}* — Sanskrit: *{p.get('sanskrit_name')}*)")
        md.append(f"- **Traditional Attributes:** {p.get('rasa_virya_vipaka')}")
        md.append(f"- **Ayurvedic Profile:** {p.get('traditional_information')}")
        md.append(f"- **Modern Research Highlights:** {p.get('modern_research_summary')}")
        md.append(f"- **Research Citations:** _{p.get('research_references')}_")
        md.append(f"- ⚠️ **Safety / Caution:** {p.get('safety_notes')}\n")

    md.append("---")
    md.append("## 6. Authentic Sources & Institutional References")
    md.append("- [Ministry of Ayush — Ayush Research Portal](https://arp.ayush.gov.in/researchabout)")
    md.append("- [WHO — Global Traditional Medicine Strategy 2025–2034](https://www.who.int/teams/who-global-traditional-medicine-centre/traditional-medicine-strategy-2025-2034)")
    md.append("- [WHO — Traditional, Complementary and Integrative Medicine](https://www.who.int/teams/integrated-health-services/traditional-complementary-and-integrative-medicine/global-strategies)")
    md.append("- [WHO — Traditional Medicine Questions and Answers](https://www.who.int/news-room/questions-and-answers/item/traditional-medicine)")
    md.append("- Classical Treatises: *Charaka Samhita* (Sutrasthana 21 & 27), *Astanga Hridaya* (Dinacharya Adhyaya 2)\n")
    md.append("---")
    md.append("*(Report generated by HealthSathi Analytics Engine. For medical diagnoses or treatment, always consult a licensed physician.)*")
    return "\n".join(md)


def generate_docx_report(
    user_data: Dict[str, Any],
    scores: Dict[str, Any],
    recommendations: List[Dict[str, Any]],
    routine: List[Dict[str, str]],
    plants: List[Dict[str, Any]],
    sources_df: Any,
    output_docx_path: str
) -> str:
    """
    Generates a publication-grade Microsoft Word (.docx) personalized wellness report
    with full 13-section structure, styled callout boxes, tabular layouts, and non-diagnostic disclaimers.
    """
    import re
    import docx
    from docx import Document
    from docx.shared import Inches, Pt, RGBColor
    from docx.enum.text import WD_ALIGN_PARAGRAPH
    from docx.enum.table import WD_TABLE_ALIGNMENT
    from docx.oxml import parse_xml
    from docx.oxml.ns import nsdecls

    def clean_xml_str(val):
        if val is None:
            return ""
        s = str(val)
        return re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\x84\x86-\x9f]', '', s)

    def set_cell_background(cell, fill_hex):
        tcPr = cell._tc.get_or_add_tcPr()
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
        tcPr.append(shd)

    def set_cell_margins(cell, top=120, bottom=120, left=180, right=180):
        tcPr = cell._tc.get_or_add_tcPr()
        tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
        tcPr.append(tcMar)

    def style_table_header(row, col_widths, bg_hex="1E5128", text_color_rgb=RGBColor(255, 255, 255)):
        for idx, cell in enumerate(row.cells):
            set_cell_background(cell, bg_hex)
            set_cell_margins(cell, top=140, bottom=140, left=180, right=180)
            cell.width = col_widths[idx]
            for p in cell.paragraphs:
                p.alignment = WD_ALIGN_PARAGRAPH.LEFT
                for run in p.runs:
                    run.font.bold = True
                    run.font.color.rgb = text_color_rgb
                    run.font.name = "Calibri"
                    run.font.size = Pt(10)

    def style_table_row(row, col_widths, bg_hex="FFFFFF", is_alternate=False):
        fill = "F8FAFC" if is_alternate else bg_hex
        for idx, cell in enumerate(row.cells):
            if fill != "FFFFFF":
                set_cell_background(cell, fill)
            set_cell_margins(cell, top=100, bottom=100, left=180, right=180)
            cell.width = col_widths[idx]
            for p in cell.paragraphs:
                for run in p.runs:
                    run.font.name = "Calibri"
                    run.font.size = Pt(9.5)

    os.makedirs(os.path.dirname(os.path.abspath(output_docx_path)), exist_ok=True)
    doc = Document()

    for section in doc.sections:
        section.top_margin = Inches(0.75)
        section.bottom_margin = Inches(0.75)
        section.left_margin = Inches(0.75)
        section.right_margin = Inches(0.75)

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_title = p_title.add_run("HealthSathi — IKS Personalized Wellness Report")
    run_title.font.name = "Calibri"
    run_title.font.size = Pt(22)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(30, 81, 40)

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_sub = p_sub.add_run("A Data-Driven Framework for Personalized Lifestyle Analytics Grounded in Indian Knowledge Systems (Ayurveda)")
    run_sub.font.name = "Calibri"
    run_sub.font.size = Pt(11)
    run_sub.font.italic = True
    run_sub.font.color.rgb = RGBColor(78, 159, 61)

    p_meta = doc.add_paragraph()
    p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run_meta = p_meta.add_run("Generated by HealthSathi Digital Assistant | Scientific & Classical Knowledge Engine | Confidential Personal Wellness Brief")
    run_meta.font.name = "Calibri"
    run_meta.font.size = Pt(8.5)
    run_meta.font.color.rgb = RGBColor(100, 116, 139)

    doc.add_paragraph()

    # Safety Notice
    t_disc = doc.add_table(rows=1, cols=1)
    t_disc.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell_disc = t_disc.rows[0].cells[0]
    set_cell_background(cell_disc, "FEE2E2")
    set_cell_margins(cell_disc, top=140, bottom=140, left=200, right=200)
    p_disc = cell_disc.paragraphs[0]
    r_disc_title = p_disc.add_run("MANDATORY SAFETY & NON-DIAGNOSTIC NOTICE\n")
    r_disc_title.bold = True
    r_disc_title.font.size = Pt(9.5)
    r_disc_title.font.color.rgb = RGBColor(185, 28, 28)
    r_disc_body = p_disc.add_run(
        "HealthSathi is an educational and lifestyle wellness prototype, not a medical diagnostic or prescription system. "
        "It does NOT diagnose medical conditions, prescribe pharmaceutical or herbal medicines, replace licensed physicians, "
        "or advise altering any prescribed clinical treatments. All self-reported conditions are treated strictly as contextual "
        "lifestyle indicators to customize daily behavioral recommendations."
    )
    r_disc_body.font.size = Pt(9)
    r_disc_body.font.color.rgb = RGBColor(127, 29, 29)

    doc.add_paragraph()

    # 1. User Profile
    h1 = doc.add_heading(level=1)
    run_h1 = h1.add_run("1. User Profile & Baseline Lifestyle Metrics")
    run_h1.font.color.rgb = RGBColor(30, 81, 40)
    run_h1.font.bold = True

    t_prof = doc.add_table(rows=5, cols=4)
    t_prof.alignment = WD_TABLE_ALIGNMENT.CENTER
    widths_prof = [Inches(1.75), Inches(1.75), Inches(1.75), Inches(1.75)]

    prof_matrix = [
        [("Age", clean_xml_str(user_data.get("age"))), ("Gender", clean_xml_str(user_data.get("gender"))), ("Height", f"{user_data.get('height_cm')} cm"), ("Weight", f"{user_data.get('weight_kg')} kg")],
        [("BMI", f"{user_data.get('bmi')} kg/m²"), ("BMI Category", clean_xml_str(user_data.get("bmi_category"))), ("Occupation", clean_xml_str(user_data.get("occupation"))), ("Sleep Duration", f"{user_data.get('sleep_duration_hrs')} hrs")],
        [("Bedtime", clean_xml_str(user_data.get("sleep_time_raw"))), ("Wake-Up Time", clean_xml_str(user_data.get("wake_up_time_raw"))), ("Sleep Quality", clean_xml_str(user_data.get("sleep_quality"))), ("Work/Study Hours", f"{user_data.get('work_study_hrs')} hrs")],
        [("Screen Exposure", f"{user_data.get('screen_time_hrs')} hrs"), ("Physical Activity", f"{user_data.get('physical_activity_min')} min/day"), ("Water Intake", f"{user_data.get('water_intake_liters')} L/day"), ("Outdoor Sunlight", f"{user_data.get('outdoor_time_min')} min/day")],
        [("Reported Stress", f"{user_data.get('stress_level')}/10"), ("General Mood", clean_xml_str(user_data.get("mood"))), ("Relaxation Practice", "Yes" if user_data.get("relaxation_activity") else "No"), ("Meal Regularity", clean_xml_str(user_data.get("meal_regularity")))]
    ]

    for row_idx, row in enumerate(t_prof.rows):
        for col_idx, cell in enumerate(row.cells):
            label, val = prof_matrix[row_idx][col_idx]
            p = cell.paragraphs[0]
            r_lbl = p.add_run(f"{label}: ")
            r_lbl.bold = True
            r_lbl.font.size = Pt(9)
            r_lbl.font.color.rgb = RGBColor(71, 85, 105)
            r_val = p.add_run(val)
            r_val.font.size = Pt(9.5)
            r_val.font.bold = True
            r_val.font.color.rgb = RGBColor(15, 23, 42)
            set_cell_background(cell, "F8FAFC" if row_idx % 2 == 1 else "FFFFFF")
            set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
            cell.width = widths_prof[col_idx]

    conds_str = ", ".join(user_data.get("health_conditions", ["None"]))
    p_cond = doc.add_paragraph()
    r_c_lbl = p_cond.add_run("Self-Reported Health Context (Non-Diagnostic): ")
    r_c_lbl.bold = True
    r_c_lbl.font.size = Pt(9.5)
    r_c_lbl.font.color.rgb = RGBColor(30, 81, 40)
    r_c_val = p_cond.add_run(clean_xml_str(conds_str))
    r_c_val.font.size = Pt(9.5)
    r_c_val.font.italic = True

    doc.add_paragraph()

    # 2. Derived Scores
    h2 = doc.add_heading(level=1)
    run_h2 = h2.add_run("2. Derived Lifestyle Wellness Scores")
    run_h2.font.color.rgb = RGBColor(30, 81, 40)
    run_h2.font.bold = True

    t_overall = doc.add_table(rows=1, cols=1)
    t_overall.alignment = WD_TABLE_ALIGNMENT.CENTER
    c_ov = t_overall.rows[0].cells[0]
    set_cell_background(c_ov, "EBF5FB")
    set_cell_margins(c_ov, top=140, bottom=140, left=200, right=200)
    p_ov = c_ov.paragraphs[0]
    p_ov.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r_ov_lbl = p_ov.add_run("OVERALL LIFESTYLE WELLNESS SCORE: ")
    r_ov_lbl.font.size = Pt(11)
    r_ov_lbl.bold = True
    r_ov_lbl.font.color.rgb = RGBColor(30, 81, 40)
    r_ov_val = p_ov.add_run(f"{scores.get('overall_wellness_score')} / 100\n")
    r_ov_val.font.size = Pt(16)
    r_ov_val.bold = True
    r_ov_val.font.color.rgb = RGBColor(30, 81, 40)
    r_ov_band = p_ov.add_run(f"Status: {scores.get('wellness_band')} — {scores.get('wellness_summary')}")
    r_ov_band.font.size = Pt(9.5)
    r_ov_band.font.italic = True
    r_ov_band.font.color.rgb = RGBColor(51, 65, 85)

    doc.add_paragraph()

    t_scores = doc.add_table(rows=1, cols=4)
    t_scores.alignment = WD_TABLE_ALIGNMENT.CENTER
    widths_scores = [Inches(1.8), Inches(1.0), Inches(1.4), Inches(2.8)]
    headers_scores = ["Dimension", "Score", "Target Benchmark", "Primary Evaluation Rationale & IKS Pillar"]
    for idx, name in enumerate(headers_scores):
        t_scores.rows[0].cells[idx].paragraphs[0].add_run(name)
    style_table_header(t_scores.rows[0], widths_scores)

    score_breakdown = [
        ("Sleep Score", f"{scores.get('sleep_score')} / 100", "7.0–8.5 hrs (Bedtime < 10:30 PM)", "Evaluates sleep duration, subjective quality, and circadian bedtime alignment (Nidra Trayopasthambha)."),
        ("Physical Activity Score", f"{scores.get('activity_score')} / 100", "≥ 30 min daily (Vyayama)", "Measures physical exercise volume, outdoor daylight exposure, and screen time balance."),
        ("Stress Management Score", f"{scores.get('stress_score')} / 100", "Stress ≤ 4/10, Good Mood", "Assesses autonomic resilience, affective balance, and relaxation activity buffering (Sadvritta)."),
        ("Hydration Balance Score", f"{scores.get('hydration_score')} / 100", "2.0–3.5 L (Calibrated to mass)", "Evaluates adequate water consumption and warm fluid principles (Ushnodaka) for metabolic fire."),
        ("Routine Consistency Score", f"{scores.get('routine_score')} / 100", "Regular meal windows & early wake", "Calculates synchronization between sleep times, meal schedules, and diurnal solar cycles (Dinacharya)."),
        ("Nutrition & Diet Score", f"{scores.get('nutrition_score')} / 100", "High fruit/veg, Low junk", "Measures wholesome fresh nourishment, breakfast habit, and stimulant moderation (Ahara Vidhi).")
    ]

    for row_idx, item in enumerate(score_breakdown):
        row = t_scores.add_row()
        for c_idx in range(4):
            p = row.cells[c_idx].paragraphs[0]
            r = p.add_run(item[c_idx])
            if c_idx == 0:
                r.bold = True
            elif c_idx == 1:
                r.bold = True
                r.font.color.rgb = RGBColor(30, 81, 40)
        style_table_row(row, widths_scores, is_alternate=(row_idx % 2 == 1))

    doc.add_paragraph()

    # 3. Personalized Daily Routine
    h3 = doc.add_heading(level=1)
    run_h3 = h3.add_run("3. Personalized Daily Routine (Dinacharya)")
    run_h3.font.color.rgb = RGBColor(30, 81, 40)
    run_h3.font.bold = True

    p_rout_intro = doc.add_paragraph()
    p_rout_intro.add_run(
        "Dinacharya represents the classical Ayurvedic science of daily diurnal living, synchronizing human biological rhythms "
        "with natural solar cycles and the three doshic time periods (Kapha, Pitta, Vata)."
    )

    t_rout = doc.add_table(rows=1, cols=4)
    t_rout.alignment = WD_TABLE_ALIGNMENT.CENTER
    widths_rout = [Inches(1.1), Inches(1.5), Inches(3.2), Inches(1.2)]
    headers_rout = ["Time", "Ayurvedic Phase", "Action & Practical Guidance", "Classical Focus"]
    for idx, name in enumerate(headers_rout):
        t_rout.rows[0].cells[idx].paragraphs[0].add_run(name)
    style_table_header(t_rout.rows[0], widths_rout)

    for row_idx, item in enumerate(routine):
        row = t_rout.add_row()
        row.cells[0].paragraphs[0].add_run(clean_xml_str(item.get("time"))).bold = True
        row.cells[1].paragraphs[0].add_run(clean_xml_str(item.get("phase")))
        
        p_act = row.cells[2].paragraphs[0]
        r_act_title = p_act.add_run(f"{clean_xml_str(item.get('activity'))}: ")
        r_act_title.bold = True
        p_act.add_run(clean_xml_str(item.get("details")))

        p_dosha = row.cells[3].paragraphs[0]
        r_d = p_dosha.add_run(clean_xml_str(item.get("dosha_focus", "")))
        r_d.italic = True
        style_table_row(row, widths_rout, is_alternate=(row_idx % 2 == 1))

    doc.add_paragraph()

    # 4. Curated IKS Recommendations
    h4 = doc.add_heading(level=1)
    run_h4 = h4.add_run("4. Curated IKS Recommendations & Transparent Explainability")
    run_h4.font.color.rgb = RGBColor(30, 81, 40)
    run_h4.font.bold = True

    p_rec_intro = doc.add_paragraph()
    p_rec_intro.add_run(
        "HealthSathi employs a deterministic, transparent recommendation engine derived from classical texts rather than unconstrained "
        "LLM generation. Every recommendation provides explicit explainability: the specific user trigger, the classical physiological "
        "rationale, and the primary literature reference."
    )

    if recommendations:
        for idx, rec in enumerate(recommendations, 1):
            exp = rec.get("explainability", {})
            src = rec.get("source", {})
            
            t_rec = doc.add_table(rows=1, cols=1)
            t_rec.alignment = WD_TABLE_ALIGNMENT.CENTER
            c_r = t_rec.rows[0].cells[0]
            set_cell_background(c_r, "F0FDF4")
            set_cell_margins(c_r, top=120, bottom=120, left=180, right=180)
            
            p_r = c_r.paragraphs[0]
            r_title = p_r.add_run(f"Recommendation {idx}: {clean_xml_str(rec.get('principle_name'))} ({clean_xml_str(rec.get('iks_concept'))})\n")
            r_title.bold = True
            r_title.font.size = Pt(10.5)
            r_title.font.color.rgb = RGBColor(30, 81, 40)

            r_rec_lbl = p_r.add_run("Guideline: ")
            r_rec_lbl.bold = True
            r_rec_lbl.font.size = Pt(9.5)
            r_rec_txt = p_r.add_run(f"{clean_xml_str(rec.get('recommendation_text'))}\n\n")
            r_rec_txt.font.size = Pt(9.5)

            r_why_lbl = p_r.add_run("Why am I getting this recommendation?\n")
            r_why_lbl.bold = True
            r_why_lbl.font.size = Pt(9)
            r_why_lbl.font.color.rgb = RGBColor(194, 65, 12)

            r_trig = p_r.add_run(f"• User Lifestyle Trigger: {clean_xml_str(exp.get('user_trigger'))}\n")
            r_trig.font.size = Pt(9)
            r_trig.font.italic = True
            
            r_reas = p_r.add_run(f"• Classical IKS Rationale: {clean_xml_str(exp.get('reasoning'))}\n")
            r_reas.font.size = Pt(9)

            r_src = p_r.add_run(f"• Authentic Source: {clean_xml_str(src.get('name'))} | Ref: {clean_xml_str(exp.get('primary_source'))}")
            r_src.font.size = Pt(8.5)
            r_src.font.color.rgb = RGBColor(71, 85, 105)

            doc.add_paragraph()

    # 5. Traditional Botanical Reference
    h5 = doc.add_heading(level=1)
    run_h5 = h5.add_run("5. Traditional Botanical Wellness Information (Educational Reference)")
    run_h5.font.color.rgb = RGBColor(30, 81, 40)
    run_h5.font.bold = True

    p_plant_intro = doc.add_paragraph()
    p_plant_intro.add_run(
        "Ayurvedic Dravyaguna Vidya categorizes botanical substances by their experiential attributes (Rasa, Virya, Vipaka). "
        "The entries below are presented solely for educational reference and do not constitute personal medical prescriptions."
    )

    t_plants = doc.add_table(rows=1, cols=4)
    t_plants.alignment = WD_TABLE_ALIGNMENT.CENTER
    widths_plants = [Inches(1.5), Inches(1.5), Inches(2.2), Inches(1.8)]
    headers_plants = ["Plant & Sanskrit", "Classical Attributes", "Traditional & Modern Actions", "Safety Notes & Cautions"]
    for idx, name in enumerate(headers_plants):
        t_plants.rows[0].cells[idx].paragraphs[0].add_run(name)
    style_table_header(t_plants.rows[0], widths_plants)

    for row_idx, p in enumerate(plants[:5]):
        row = t_plants.add_row()
        p0 = row.cells[0].paragraphs[0]
        r_p0 = p0.add_run(f"{clean_xml_str(p.get('common_name'))}\n")
        r_p0.bold = True
        r_sci = p0.add_run(f"{clean_xml_str(p.get('scientific_name'))}\n")
        r_sci.italic = True
        p0.add_run(f"({clean_xml_str(p.get('sanskrit_name'))})")

        p1 = row.cells[1].paragraphs[0]
        p1.add_run(clean_xml_str(p.get('rasa_virya_vipaka', '')))

        p2 = row.cells[2].paragraphs[0]
        p2.add_run(f"{clean_xml_str(p.get('traditional_information'))}\n\n")
        r_res = p2.add_run(f"Modern Note: {clean_xml_str(p.get('modern_research_summary'))}")
        r_res.font.size = Pt(8.5)

        p3 = row.cells[3].paragraphs[0]
        r_saf = p3.add_run(clean_xml_str(p.get('safety_notes')))
        r_saf.font.color.rgb = RGBColor(185, 28, 28)
        r_saf.font.size = Pt(8.5)
        style_table_row(row, widths_plants, is_alternate=(row_idx % 2 == 1))

    doc.add_paragraph()

    # 6. Sources & Literature
    h6 = doc.add_heading(level=1)
    run_h6 = h6.add_run("6. Authentic Sources & Institutional References")
    run_h6.font.color.rgb = RGBColor(30, 81, 40)
    run_h6.font.bold = True

    sources_list = [
        ("Ministry of Ayush — Ayush Research Portal", "https://arp.ayush.gov.in/researchabout", "Official national database for indexed peer-reviewed Ayurvedic clinical trials and pharmacological research."),
        ("WHO Global Traditional Medicine Strategy 2025–2034", "https://www.who.int/teams/who-global-traditional-medicine-centre/traditional-medicine-strategy-2025-2034", "World Health Organization policy framework on evidence integration, digital health, and quality safety standardisation."),
        ("WHO Traditional, Complementary & Integrative Medicine", "https://www.who.int/teams/integrated-health-services/traditional-complementary-and-integrative-medicine/global-strategies", "Global strategies for standardizing safety, education, and health system integration of traditional modalities."),
        ("Charaka Samhita (Sutrasthana 21 & 27)", "https://www.carakasamhitaonline.com", "Classical treatise foundational chapters on sleep (Nidra Trayopasthambha) and dietary regimens (Annapanavidhi)."),
        ("Astanga Hridaya (Sutrasthana 2)", "https://vedicheritage.gov.in", "Foundational treatise on diurnal circadian lifestyle (Dinacharya Adhyaya) and seasonal living (Ritucharya)."),
        ("Bhavaprakasha Nighantu (Varivarga)", "https://vedicheritage.gov.in", "Classical pharmacopeia and hydrological treatise describing warm water intake (Ushnodaka) for metabolic fire and digestion."),
        ("Chandrasekhar et al. (2012) Indian J Psychol Med", "https://pubmed.ncbi.nlm.nih.gov/23439798/", "Randomized double-blind placebo-controlled study on Ashwagandha root extract reducing cortisol and perceived stress."),
        ("Hewlings & Kalman (2017) Foods", "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5664031/", "Curcumin: A Review of Its Effects on Human Health and Antioxidant Capacities."),
        ("Cohen (2014) J Ayurveda Integr Med", "https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4296439/", "Tulsi - Ocimum sanctum: A herb for all reasons in lifestyle and stress management."),
        ("Stough et al. (2001) Psychopharmacology", "https://pubmed.ncbi.nlm.nih.gov/11498727/", "Double-blind clinical trial on Bacopa monnieri (Brahmi) improving working memory and cognitive speed.")
    ]

    for name, url, desc in sources_list:
        p_s = doc.add_paragraph()
        r_sn = p_s.add_run(f"• {name}: ")
        r_sn.bold = True
        r_sn.font.size = Pt(9.5)
        r_sd = p_s.add_run(f"{desc} ")
        r_sd.font.size = Pt(9)
        r_su = p_s.add_run(f"[{url}]")
        r_su.font.size = Pt(8.5)
        r_su.font.color.rgb = RGBColor(2, 132, 199)

    doc.add_paragraph()

    # Final Notice
    p_fin = doc.add_paragraph()
    r_fin = p_fin.add_run(
        "Institutional Notice: Generated by the HealthSathi Digital Lifestyle Assistant prototype for educational and research evaluation. "
        "For medical inquiries, clinical diagnoses, or prescription therapies, always consult licensed healthcare professionals."
    )
    r_fin.font.italic = True
    r_fin.font.size = Pt(8.5)
    r_fin.font.color.rgb = RGBColor(100, 116, 139)

    doc.save(output_docx_path)
    return output_docx_path

