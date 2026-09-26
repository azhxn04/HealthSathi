# 🌿 HealthSathi: An IKS-Based Personalized Health and Lifestyle Analytics System

[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/deploy?repository=azhxn04/HealthSathi&branch=main&mainModule=app.py)
[![GitHub Repository](https://img.shields.io/badge/GitHub-azhxn04%2FHealthSathi-181717?logo=github)](https://github.com/azhxn04/HealthSathi)
[![Python Version](https://img.shields.io/badge/Python-3.10%2B-1e5128.svg)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Streamlit-FF4B4B.svg)](https://streamlit.io/)
[![Knowledge System](https://img.shields.io/badge/Domain-Indian%20Knowledge%20Systems%20(Ayurveda)-d4a373.svg)](https://arp.ayush.gov.in/)
[![Scope](https://img.shields.io/badge/Scope-Wellness%20%26%20Education%20(Non--Diagnostic)-green.svg)](#safety-and-scope-rules)

---

## 1. Project Overview
**HealthSathi** is an explainable, data-driven lifestyle and wellness analytics platform that unites modern data science with classical **Indian Knowledge Systems (IKS)**—specifically authentic Ayurvedic principles of *Dinacharya* (circadian daily routine), *Nidra* (sleep hygiene), *Ahara Vidhi* (dietary discipline), and *Sadvritta* (mental equilibrium).

Users input daily habits across sleep, physical activity, nutrition, hydration, screen exposure, stress levels, and self-reported health conditions. HealthSathi:
1. Calculates a composite **Lifestyle Wellness Score (0–100)** across six distinct lifestyle dimensions.
2. Identifies behavioral lifestyle archetypes using **unsupervised Machine Learning (K-Means)**.
3. Dynamically generates an **individualized 24-hour daily routine (Dinacharya)** synchronized with solar dosha cycles (Kapha, Pitta, Vata).
4. Matches habits to curated, transparent Ayurvedic recommendations equipped with explicit **"Why am I getting this recommendation?"** explainability cards.
5. Provides a searchable **Medicinal Plant Explorer** and publishes verifiable multi-page **PDF Wellness Reports**.

> **⚠️ IMPORTANT SAFETY & NON-DIAGNOSTIC NOTICE:**  
> HealthSathi is strictly an educational and wellness analytics prototype, **NOT** a medical diagnostic or clinical prescription system. It does not diagnose illnesses, prescribe medications, or replace licensed medical practitioners. All self-reported conditions are treated solely as passive lifestyle context.

---

## 2. Research Paper & Public Science Article
Included in the `research/` directory:
- **Research Paper Title:**  
  *“HealthSathi: A Data-Driven Framework for Personalized Wellness Using Indian Knowledge Systems and Ayurvedic Lifestyle Principles”*  
  Format: [`research/research_paper.md`](research/research_paper.md) and [`research/research_paper.docx`](research/research_paper.docx) (Full 14-section academic paper).
- **Public Science Article Title:**  
  *“HealthSathi: Bringing Indian Traditional Wellness Knowledge into a Data-Driven Digital Lifestyle Assistant”*  
  Format: [`research/article.md`](research/article.md) and [`research/article.docx`](research/article.docx) (12-section popular science article).

---

## 3. Four-Layer System Architecture
1. **User Lifestyle Layer:** Captures 24+ primary lifestyle variables spanning sleep, movement, hydration, screen exposure, diet, stress, and self-reported conditions.
2. **Data Science & Scoring Layer:** Cleans, engineers circadian metrics, and calculates 6 dimension scores (0–100) and an overall composite Lifestyle Wellness Score.
3. **Curated IKS Knowledge Base:** Houses deterministic, curated rules from foundational treatises (*Charaka Samhita*, *Astanga Hridaya*, *Bhavaprakasha*) and institutional sources (Ministry of Ayush, WHO).
4. **Actionable Output Layer:** Delivers interactive visual dashboards, dynamic daily routines, transparent recommendation rationales, and downloadable PDF reports.

---

## 4. Mathematical Scoring Formulations
1. **Sleep Score ($S_{sleep}$):** Evaluates duration against optimal rest (7.0–8.5 hrs, -22 pts/hr deficit), quality offsets, and bedtime circadian penalties (sleeping after 11:30 PM incurs penalties as it disrupts nocturnal cellular detoxification).
2. **Activity Score ($S_{act}$):** Rewards physical exercise up to half-capacity ($A/45 \times 70$), outdoor natural sunlight ($O/30 \times 30$), and deducts sedentary screen time over 8 hours.
3. **Stress Score ($S_{stress}$):** Scales inverse stress level $(11 - L) \times 10$, buffered by mood offsets and dedicated mindfulness practices.
4. **Hydration Score ($S_{hyd}$):** Calibrated to body weight ($35\text{ ml/kg}$) and physical activity. Optimal range $\rho \in [0.90, 1.30]$ scores 95–100.
5. **Routine Consistency Score ($S_{rout}$):** Evaluates meal regularity, consistent eating windows, screen limits, and morning rising rhythm.
6. **Nutrition Score ($S_{nut}$):** Combines breakfast habit ($+20$), fresh fruit/vegetable frequency ($+40$), processed food minimization ($+30$), and caffeine moderation ($+10$).
7. **Composite Lifestyle Wellness Score ($LWS$):**
   $$LWS = 0.22 \cdot S_{sleep} + 0.20 \cdot S_{stress} + 0.18 \cdot S_{act} + 0.18 \cdot S_{nut} + 0.12 \cdot S_{rout} + 0.10 \cdot S_{hyd}$$

---

## 5. Installation & Quickstart

### Prerequisites
- Python 3.10, 3.11, or 3.12 installed.

### 1. Clone Repository
```bash
git clone https://github.com/azhxn04/HealthSathi.git
cd HealthSathi
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run Automated System Test Suite
```bash
python test_system.py
```
*Expected Output: `Ran 6 tests ... OK`*

### 4. Launch the Streamlit Web Application
```bash
streamlit run app.py
```
Open your browser at `http://localhost:8501`.

---

## 6. Streamlit Navigation Walkthrough
1. **🏠 Overview & Architecture:** Understand the project mission, four-layer architecture, and safety disclaimer.
2. **📝 Health Profile Input:** Enter your 24+ lifestyle factors or click **Quick Load Demonstration Presets** (e.g. *Corporate Tech Worker*, *College Student*, or *Balanced Practitioner*).
3. **📊 Wellness Dashboard:** View your 0–100 Lifestyle Wellness Score gauge, 6-Dimension Hexagonal Radar, Sleep vs Reference Bar, 7-Day Stress Dynamics, Activity comparison, and ML Archetype classification.
4. **⏰ Personalized Daily Routine:** Explore your tailored 24-hour *Dinacharya* schedule mapped to Kapha, Pitta, and Vata diurnal cycles.
5. **📚 IKS Knowledge & Plants:** Search the 10+ botanical database with scientific binomials, classical Sanskrit names, attributes (*Rasa-Virya-Vipaka*), published research references, and safety notes.
6. **📑 My Wellness Report (PDF):** Review the 13-section report preview, inspect explainability cards, and download an official formatted PDF report.
7. **🔬 Research & Documentation:** Read and download the complete academic research paper and public science article in `.docx` and `.md` formats.

---

## 7. Key Institutional References & Grounding
- **Ministry of Ayush (Govt. of India) — Ayush Research Portal:** https://arp.ayush.gov.in/researchabout
- **WHO Global Traditional Medicine Strategy 2025–2034:** https://www.who.int/teams/who-global-traditional-medicine-centre/traditional-medicine-strategy-2025-2034
- **WHO Traditional, Complementary and Integrative Medicine:** https://www.who.int/teams/integrated-health-services/traditional-complementary-and-integrative-medicine/global-strategies
- **WHO Traditional Medicine Q&A:** https://www.who.int/news-room/questions-and-answers/item/traditional-medicine
- **Classical Treatises:** *Charaka Samhita* (*Sutrasthana* Ch. 21 & 27), *Astanga Hridaya* (*Sutrasthana* Ch. 2), and *Bhavaprakasha Nighantu*.

---

## 8. License & Ethics
HealthSathi is released under the **MIT Open Source License**. Developed for academic evaluation, cultural digital preservation, and educational health literacy. Always consult qualified healthcare professionals for medical diagnoses or clinical treatments.
