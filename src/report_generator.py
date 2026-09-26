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
