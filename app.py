"""
HealthSathi: An IKS-Based Personalized Health and Lifestyle Analytics System
Full Stack Streamlit Application combining Data Science, Ayurvedic Principles,
Interactive Dashboards, Personalized Dinacharya Routine, and PDF Report Generation.
"""

import os
import streamlit as st
import pandas as pd
import numpy as np

# Local imports
from src.preprocessing import clean_user_input, format_hours_to_time, parse_time_to_hours
from src.scoring import calculate_all_scores
from src.recommendations import RecommendationEngine
from src.visualizations import (
    create_wellness_gauge, create_sleep_reference_chart, create_stress_trend_chart,
    create_activity_chart, create_lifestyle_radar_chart, create_weekly_comparison_chart
)
from src.report_generator import generate_pdf_report, generate_markdown_report
from src.ml_models import LifestyleMLAnalytics


st.set_page_config(
    page_title="HealthSathi | IKS Lifestyle Analytics",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded"
)

CUSTOM_CSS = """
<style>
    :root {
        --primary: #1e5128;
        --secondary: #2a9d8f;
        --accent: #d4a373;
        --bg-light: #fafaf8;
        --text-dark: #1f2937;
    }
    .main-title {
        font-family: 'Inter', sans-serif;
        color: #1e5128;
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }
    .sub-title {
        font-size: 1.05rem;
        color: #4b5563;
        margin-bottom: 1.2rem;
    }
    .disclaimer-banner {
        background-color: #fee2e2;
        border-left: 5px solid #ef4444;
        padding: 0.85rem 1.1rem;
        border-radius: 6px;
        color: #7f1d1d;
        font-size: 0.9rem;
        margin-bottom: 1.5rem;
        line-height: 1.4;
    }
    .iks-badge {
        background: #e6f4ea;
        color: #137333;
        padding: 3px 8px;
        border-radius: 12px;
        font-size: 0.78rem;
        font-weight: 600;
    }
    .routine-row {
        background: #ffffff;
        border-left: 4px solid #2a9d8f;
        padding: 0.8rem 1rem;
        margin-bottom: 0.6rem;
        border-radius: 4px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
    }
</style>
"""
st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


@st.cache_resource
def load_engines():
    rec_engine = RecommendationEngine()
    ml_analytics = LifestyleMLAnalytics()
    return rec_engine, ml_analytics

rec_engine, ml_analytics = load_engines()

PRESETS = {
    "Select a preset or customize below...": None,
    "💼 Corporate Tech Worker (Sedentary & High Stress)": {
        "age": 28, "gender": "Male", "height_cm": 174.0, "weight_kg": 76.0,
        "occupation": "Working Professional (IT/Corporate)",
        "sleep_duration_hrs": 5.5, "sleep_time_raw": "01:00 AM", "wake_up_time_raw": "06:30 AM",
        "sleep_quality": "Poor", "work_study_hrs": 10.0, "screen_time_hrs": 9.5,
        "physical_activity_min": 15.0, "water_intake_liters": 1.5, "meal_regularity": "Irregular",
        "outdoor_time_min": 15.0, "stress_level": 8, "mood": "Low", "relaxation_activity": False,
        "breakfast_regular": False, "fruit_veg_intake": "Low", "processed_food_freq": "High",
        "caffeine_freq": "High", "meal_timing_consistency": "Irregular",
        "health_conditions": ["Anxiety/stress-related concerns", "Digestive problems"]
    },
    "🎓 College Student (Sleep Debt & Late Bedtime)": {
        "age": 20, "gender": "Female", "height_cm": 162.0, "weight_kg": 54.0,
        "occupation": "Student",
        "sleep_duration_hrs": 5.0, "sleep_time_raw": "02:00 AM", "wake_up_time_raw": "07:00 AM",
        "sleep_quality": "Moderate", "work_study_hrs": 8.5, "screen_time_hrs": 8.0,
        "physical_activity_min": 20.0, "water_intake_liters": 1.8, "meal_regularity": "Irregular",
        "outdoor_time_min": 20.0, "stress_level": 7, "mood": "Neutral", "relaxation_activity": False,
        "breakfast_regular": False, "fruit_veg_intake": "Medium", "processed_food_freq": "High",
        "caffeine_freq": "High", "meal_timing_consistency": "Irregular",
        "health_conditions": ["Migraine"]
    },
    "🧘 Balanced Dinacharya Practitioner (Healthy Baseline)": {
        "age": 34, "gender": "Female", "height_cm": 165.0, "weight_kg": 60.0,
        "occupation": "Educator / Academic",
        "sleep_duration_hrs": 7.5, "sleep_time_raw": "10:30 PM", "wake_up_time_raw": "06:00 AM",
        "sleep_quality": "Good", "work_study_hrs": 7.5, "screen_time_hrs": 4.5,
        "physical_activity_min": 45.0, "water_intake_liters": 2.8, "meal_regularity": "Regular",
        "outdoor_time_min": 45.0, "stress_level": 3, "mood": "Good", "relaxation_activity": True,
        "breakfast_regular": True, "fruit_veg_intake": "High", "processed_food_freq": "Low",
        "caffeine_freq": "Low", "meal_timing_consistency": "Regular",
        "health_conditions": ["None"]
    }
}

if "user_profile" not in st.session_state:
    st.session_state.user_profile = PRESETS["💼 Corporate Tech Worker (Sedentary & High Stress)"].copy()

with st.sidebar:
    if os.path.exists("assets/logo.png"):
        st.image("assets/logo.png", use_container_width=True)
    else:
        st.title("🌿 HealthSathi")
    
    st.caption("**An IKS-Based Personalized Lifestyle & Wellness Analytics System**")
    st.markdown("---")

    page = st.radio(
        "Navigation",
        [
            "🏠 Overview & Architecture",
            "📝 Health Profile Input",
            "📊 Wellness Dashboard",
            "⏰ Personalized Daily Routine",
            "📚 IKS Knowledge & Plants",
            "📑 My Wellness Report (PDF)",
            "🔬 Research & Documentation"
        ]
    )

    st.markdown("---")
    st.markdown(
        "<div style='font-size:0.8rem; color:#6b7280;'>"
        "<b>Framework Scope:</b><br/>"
        "• Wellness & Educational Prototype<br/>"
        "• Non-Diagnostic / Non-Prescriptive<br/>"
        "• Curated Classical IKS Principles<br/>"
        "• Explainable Algorithmic Rules"
        "</div>",
        unsafe_allow_html=True
    )
    st.caption("Version 1.0 • Built with Python & Streamlit")


# PAGE 1: Overview
if page == "🏠 Overview & Architecture":
    st.markdown('<h1 class="main-title">HealthSathi: Digital IKS Wellness Assistant</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Bridging Indian Knowledge Systems (Ayurveda) and Data Science for Explainable Lifestyle Analytics</p>', unsafe_allow_html=True)

    st.markdown(
        """
        <div class="disclaimer-banner">
            <strong>⚠️ CRITICAL SAFETY & SCOPE NOTICE:</strong><br/>
            HealthSathi is strictly an educational and wellness analytics prototype. It is <strong>NOT</strong> a medical diagnostic system, clinical tool, or prescription engine. 
            It does not replace medical doctors, diagnose illnesses, or suggest altering any prescribed pharmaceuticals. 
            All self-reported conditions are treated solely as passive lifestyle context.
        </div>
        """,
        unsafe_allow_html=True
    )

    col1, col2 = st.columns([3, 2])
    with col1:
        st.markdown("### 1. Project Concept & Objectives")
        st.write(
            """
            Modern lifestyles present a growing epidemic of non-communicable lifestyle disorders linked to chronic sleep deprivation, 
            excessive screen exposure, sedentary desk habits, erratic eating times, and psychological distress. While modern digital health 
            trackers quantify metrics such as steps and heart rate, they rarely contextualize habits within holistic lifestyle frameworks.
            
            **HealthSathi** integrates classical **Indian Knowledge Systems (IKS)**—specifically authentic Ayurvedic principles of 
            *Dinacharya* (daily circadian routine), *Ahara Vidhi* (dietary discipline), *Nidra* (sleep hygiene), and *Sadvritta* (mental equilibrium)—with 
            modern data science and mathematical scoring models.
            """
        )

        st.markdown("### 2. Four-Layer System Architecture")
        st.markdown(
            """
            1. **User Lifestyle Layer:** Captures 24+ primary lifestyle variables spanning sleep, movement, hydration, screen exposure, diet, stress, and self-reported conditions.
            2. **Data Science & Scoring Layer:** Cleans, engineers circadian metrics, and calculates 6 dimension scores (0–100) and an overall composite **Lifestyle Wellness Score**.
            3. **IKS Knowledge Layer:** Houses deterministic, curated rules from foundational treatises (*Charaka Samhita*, *Astanga Hridaya*, *Bhavaprakasha*) and institutional sources (Ministry of Ayush, WHO).
            4. **Output & Explainability Layer:** Delivers interactive visual dashboards, dynamic daily routines, transparent recommendation rationales, and downloadable PDF reports.
            """
        )

    with col2:
        st.markdown("### 3. System Workflow")
        st.info(
            """
            **User Data Entry**  
            *(Sleep, Activity, Diet, Stress)*  
            ⬇️  
            **Data Science Preprocessing**  
            *(Circadian hour conversion, BMI, scoring equations)*  
            ⬇️  
            **Transparent IKS Rule Engine**  
            *(Maps metrics to classical Ayurvedic concepts)*  
            ⬇️  
            **Explainable Output**  
            *(Lifestyle Radar, Personalized Routine, PDF Report)*
            """
        )

        st.markdown("### 4. Official Institutional Grounding")
        st.markdown(
            """
            - **[Ministry of Ayush — Ayush Research Portal](https://arp.ayush.gov.in/researchabout)**
            - **[WHO — Global Traditional Medicine Strategy 2025–2034](https://www.who.int/teams/who-global-traditional-medicine-centre/traditional-medicine-strategy-2025-2034)**
            - **[WHO — Traditional Medicine Q&A](https://www.who.int/news-room/questions-and-answers/item/traditional-medicine)**
            - **Classical Treatises:** Charaka Samhita & Astanga Hridaya
            """
        )

    st.markdown("---")
    st.success("👉 Head to the **Health Profile Input** tab in the sidebar to review or edit your lifestyle information and view your scores!")


# PAGE 2: Profile Input
elif page == "📝 Health Profile Input":
    st.markdown('<h1 class="main-title">Personal Lifestyle & Health Profile</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Enter your daily routine, sleep, activity, nutrition, and stress factors (24–25 Primary Indicators)</p>', unsafe_allow_html=True)

    st.subheader("⚡ Quick Load Demonstration Presets")
    selected_preset = st.selectbox("Choose a sample lifestyle profile or keep your custom values:", list(PRESETS.keys()))
    if selected_preset and PRESETS[selected_preset] is not None:
        if st.button("Apply Selected Preset"):
            st.session_state.user_profile = PRESETS[selected_preset].copy()
            st.success(f"Loaded profile: {selected_preset}")
            st.rerun()

    prof = st.session_state.user_profile

    st.markdown("---")
    with st.form("lifestyle_input_form"):
        st.markdown("#### A. Basic Demographics & Body Metrics")
        cA1, cA2, cA3, cA4, cA5 = st.columns(5)
        with cA1:
            age = st.number_input("Age", min_value=12, max_value=100, value=int(prof.get("age", 25)))
        with cA2:
            gender = st.selectbox("Gender", ["Female", "Male", "Other"], index=["Female", "Male", "Other"].index(prof.get("gender", "Female")))
        with cA3:
            height_cm = st.number_input("Height (cm)", min_value=100.0, max_value=230.0, value=float(prof.get("height_cm", 168.0)), step=0.5)
        with cA4:
            weight_kg = st.number_input("Weight (kg)", min_value=30.0, max_value=180.0, value=float(prof.get("weight_kg", 65.0)), step=0.5)
        with cA5:
            occ_list = ["Student", "Working Professional (IT/Corporate)", "Healthcare Worker", "Educator / Academic", "Self-Employed / Business", "Homemaker", "Freelancer / Creative"]
            curr_occ = prof.get("occupation", "Working Professional (IT/Corporate)")
            occ_idx = occ_list.index(curr_occ) if curr_occ in occ_list else 1
            occupation = st.selectbox("Occupation", occ_list, index=occ_idx)

        st.markdown("#### B. Sleep Patterns & Restfulness")
        cB1, cB2, cB3, cB4 = st.columns(4)
        with cB1:
            sleep_duration = st.slider("Sleep Duration (Hours)", 3.0, 12.0, float(prof.get("sleep_duration_hrs", 7.0)), 0.5)
        with cB2:
            sleep_time_str = st.text_input("Typical Bedtime (e.g. 11:00 PM)", value=str(prof.get("sleep_time_raw", "11:00 PM")))
        with cB3:
            wake_up_time_str = st.text_input("Wake-Up Time (e.g. 06:30 AM)", value=str(prof.get("wake_up_time_raw", "06:30 AM")))
        with cB4:
            sq_opts = ["Good", "Moderate", "Poor"]
            curr_sq = prof.get("sleep_quality", "Good")
            sq_idx = sq_opts.index(curr_sq) if curr_sq in sq_opts else 0
            sleep_quality = st.selectbox("Sleep Quality", sq_opts, index=sq_idx)

        st.markdown("#### C. Daily Routine & Physical Habits")
        cC1, cC2, cC3, cC4, cC5, cC6 = st.columns(6)
        with cC1:
            work_study_hrs = st.number_input("Work/Study Hours", 0.0, 16.0, float(prof.get("work_study_hrs", 8.0)), 0.5)
        with cC2:
            screen_time_hrs = st.number_input("Screen Time (Hours)", 0.0, 16.0, float(prof.get("screen_time_hrs", 6.0)), 0.5)
        with cC3:
            physical_activity_min = st.number_input("Physical Activity (min)", 0.0, 180.0, float(prof.get("physical_activity_min", 30.0)), 5.0)
        with cC4:
            water_intake_liters = st.number_input("Water Intake (Liters)", 0.5, 6.0, float(prof.get("water_intake_liters", 2.2)), 0.1)
        with cC5:
            meal_reg = st.selectbox("Meal Regularity", ["Regular", "Irregular"], index=0 if prof.get("meal_regularity") == "Regular" else 1)
        with cC6:
            outdoor_time_min = st.number_input("Outdoor Sunlight (min)", 0.0, 180.0, float(prof.get("outdoor_time_min", 30.0)), 5.0)

        st.markdown("#### D. Mental Wellness & Stress")
        cD1, cD2, cD3 = st.columns(3)
        with cD1:
            stress_level = st.slider("Reported Stress Level (1 = Serene, 10 = Severe Strain)", 1, 10, int(prof.get("stress_level", 5)))
        with cD2:
            mood_opts = ["Good", "Neutral", "Low"]
            curr_m = prof.get("mood", "Neutral")
            m_idx = mood_opts.index(curr_m) if curr_m in mood_opts else 1
            mood = st.selectbox("General Daily Mood", mood_opts, index=m_idx)
        with cD3:
            relaxation_act = st.radio("Daily Relaxation Practice? (Yoga/Meditation/Walking)", ["Yes", "No"], index=0 if prof.get("relaxation_activity", True) else 1)

        st.markdown("#### E. Dietary & Nutritional Habits")
        cE1, cE2, cE3, cE4, cE5 = st.columns(5)
        with cE1:
            breakfast_reg = st.radio("Regular Breakfast?", ["Yes", "No"], index=0 if prof.get("breakfast_regular", True) else 1)
        with cE2:
            levels = ["Low", "Medium", "High"]
            curr_fv = prof.get("fruit_veg_intake", "Medium")
            fv_idx = levels.index(curr_fv) if curr_fv in levels else 1
            fruit_veg = st.selectbox("Fruit & Veg Intake", levels, index=fv_idx)
        with cE3:
            curr_pf = prof.get("processed_food_freq", "Low")
            pf_idx = levels.index(curr_pf) if curr_pf in levels else 0
            processed_food = st.selectbox("Processed Food Frequency", levels, index=pf_idx)
        with cE4:
            curr_cf = prof.get("caffeine_freq", "Low")
            cf_idx = levels.index(curr_cf) if curr_cf in levels else 0
            caffeine_freq = st.selectbox("Caffeine Frequency", levels, index=cf_idx)
        with cE5:
            meal_timing = st.selectbox("Meal Timing Consistency", ["Regular", "Irregular"], index=0 if prof.get("meal_timing_consistency") == "Regular" else 1)

        st.markdown("#### F. Self-Reported Health Conditions Context (Non-Diagnostic)")
        all_conditions = [
            "None", "Diabetes", "Hypertension", "Migraine", "Asthma", "Arthritis",
            "Thyroid disorder", "Heart disease", "Digestive problems", "Obesity",
            "Anxiety/stress-related concerns", "Other"
        ]
        curr_conds = prof.get("health_conditions", ["None"])
        if isinstance(curr_conds, str):
            curr_conds = [curr_conds]
        valid_curr_conds = [c for c in curr_conds if c in all_conditions]
        if not valid_curr_conds:
            valid_curr_conds = ["None"]

        health_conds = st.multiselect("Self-Reported Health Conditions", all_conditions, default=valid_curr_conds)
        submit = st.form_submit_button("💾 Save Profile & Update Analytics", use_container_width=True)

    if submit:
        updated = {
            "age": age, "gender": gender, "height_cm": height_cm, "weight_kg": weight_kg, "occupation": occupation,
            "sleep_duration_hrs": sleep_duration, "sleep_time_raw": sleep_time_str, "wake_up_time_raw": wake_up_time_str,
            "sleep_quality": sleep_quality, "work_study_hrs": work_study_hrs, "screen_time_hrs": screen_time_hrs,
            "physical_activity_min": physical_activity_min, "water_intake_liters": water_intake_liters,
            "meal_regularity": meal_reg, "outdoor_time_min": outdoor_time_min, "stress_level": stress_level,
            "mood": mood, "relaxation_activity": (relaxation_act == "Yes"), "breakfast_regular": (breakfast_reg == "Yes"),
            "fruit_veg_intake": fruit_veg, "processed_food_freq": processed_food, "caffeine_freq": caffeine_freq,
            "meal_timing_consistency": meal_timing, "health_conditions": health_conds if health_conds else ["None"]
        }
        st.session_state.user_profile = updated
        st.success("✅ Lifestyle profile updated successfully! View your updated results in the **Wellness Dashboard**.")


# PAGE 3: Dashboard
elif page == "📊 Wellness Dashboard":
    st.markdown('<h1 class="main-title">Personalized Wellness Analytics Dashboard</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Derived Lifestyle Indicators, Circadian Benchmarks, and Longitudinal Insights</p>', unsafe_allow_html=True)

    user_clean = clean_user_input(st.session_state.user_profile)
    scores = calculate_all_scores(user_clean)

    col_score, col_radar = st.columns([1, 1])
    with col_score:
        st.plotly_chart(create_wellness_gauge(scores["overall_wellness_score"], scores["wellness_band"], scores["wellness_color"]), use_container_width=True)
        st.markdown(
            f"""
            <div style="background:{scores['wellness_color']}15; border:1px solid {scores['wellness_color']}; padding:0.8rem; border-radius:8px; text-align:center;">
                <b style="color:{scores['wellness_color']}; font-size:1.05rem;">{scores['wellness_band']}</b><br/>
                <span style="color:#333; font-size:0.9rem;">{scores['wellness_summary']}</span>
            </div>
            """,
            unsafe_allow_html=True
        )

    with col_radar:
        st.plotly_chart(create_lifestyle_radar_chart(scores), use_container_width=True)

    st.markdown("### 🌿 Lifestyle Dimension Breakdown")
    m1, m2, m3, m4, m5, m6 = st.columns(6)
    m1.metric("Sleep Score", f"{scores['sleep_score']}/100", f"{user_clean['sleep_duration_hrs']} hrs")
    m2.metric("Activity Score", f"{scores['activity_score']}/100", f"{user_clean['physical_activity_min']} min")
    m3.metric("Stress Mgmt", f"{scores['stress_score']}/100", f"Lvl {user_clean['stress_level']}/10")
    m4.metric("Hydration", f"{scores['hydration_score']}/100", f"{user_clean['water_intake_liters']} L")
    m5.metric("Routine Adherence", f"{scores['routine_score']}/100", user_clean['meal_regularity'])
    m6.metric("Nutrition Score", f"{scores['nutrition_score']}/100", user_clean['fruit_veg_intake'])

    st.markdown("---")
    col_vis1, col_vis2 = st.columns(2)
    with col_vis1:
        st.plotly_chart(create_sleep_reference_chart(user_clean["sleep_duration_hrs"]), use_container_width=True)
        st.caption("ℹ️ *Guideline:* Optimal circadian rest is 7.0–8.5 hours. Low sleep duration is an educational indicator, not a disease diagnosis.")

    with col_vis2:
        st.plotly_chart(create_stress_trend_chart(user_clean["stress_level"]), use_container_width=True)
        st.caption("ℹ️ *Stress Dynamics:* Demonstrates autonomic balance across the week, highlighting Tranquil (Sattva) vs High Tension (Rajas) zones.")

    col_vis3, col_vis4 = st.columns(2)
    with col_vis3:
        st.plotly_chart(create_activity_chart(user_clean["physical_activity_min"], user_clean["outdoor_time_min"]), use_container_width=True)
        st.caption("ℹ️ *Movement:* Astanga Hridaya advises exercise up to half-capacity (Ardhshakti), paired with direct natural sunlight.")

    with col_vis4:
        st.plotly_chart(create_weekly_comparison_chart(scores), use_container_width=True)
        st.caption("ℹ️ *Weekly Trajectory:* Compares your current metrics against the previous week's baseline.")

    st.markdown("---")
    st.markdown("### 🤖 Data Science Archetype & Feature Drivers (ML Engine)")
    archetype_name, feat_importances = ml_analytics.predict_archetype(user_clean)

    c_ml1, c_ml2 = st.columns([1, 1])
    with c_ml1:
        st.info(f"**Detected Lifestyle Cluster:**  
### {archetype_name}")
        st.write("Our unsupervised K-Means clustering algorithm classifies lifestyle habits based on the 650-sample synthetic evaluation cohort, contextualizing behavioral risk patterns.")
    with c_ml2:
        st.write("**Top Lifestyle Drivers Influencing Your Score:**")
        for feat, imp in list(feat_importances.items())[:4]:
            st.progress(float(imp), text=f"{feat} (Weight: {imp * 100:.1f}%)")


# PAGE 4: Dinacharya Routine
elif page == "⏰ Personalized Daily Routine":
    st.markdown('<h1 class="main-title">Personalized Dinacharya (Daily Routine)</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Algorithmic Chronobiology Synchronized with Ayurvedic Dosha Diurnal Cycles</p>', unsafe_allow_html=True)

    user_clean = clean_user_input(st.session_state.user_profile)
    routine = rec_engine.generate_personalized_daily_routine(user_clean)

    st.markdown(
        f"""
        <div style="background:#e6f4ea; border-left:4px solid #137333; padding:0.85rem; border-radius:6px; margin-bottom:1rem;">
            <strong>Classical IKS Principle:</strong> In Ayurveda, daily living is harmonized with natural solar cycles (*Dinacharya*). 
            The 24-hour cycle is governed by recurring four-hour windows of <strong>Kapha</strong> (stability/heaviness), 
            <strong>Pitta</strong> (transformation/metabolic heat), and <strong>Vata</strong> (mobility/clarity). 
            Below is your dynamically tailored routine based on your wake-up time (<strong>{user_clean['wake_up_time_raw']}</strong>) and bedtime (<strong>{user_clean['sleep_time_raw']}</strong>).
        </div>
        """,
        unsafe_allow_html=True
    )

    for item in routine:
        st.markdown(
            f"""
            <div class="routine-row">
                <div style="display:flex; justify-content:space-between; align-items:center;">
                    <span style="font-size:1.15rem; font-weight:700; color:#1e5128;">⏰ {item['time']}</span>
                    <span class="iks-badge">{item['phase']}</span>
                </div>
                <div style="font-weight:600; color:#1f2937; margin-top:4px;">{item['activity']}</div>
                <div style="font-size:0.88rem; color:#4b5563; margin-top:2px;">{item['details']}</div>
                <div style="font-size:0.78rem; color:#059669; margin-top:4px;">🌿 <em>Ayurvedic Focus: {item.get('dosha_focus', '')}</em></div>
            </div>
            """,
            unsafe_allow_html=True
        )


# PAGE 5: IKS Knowledge & Plants
elif page == "📚 IKS Knowledge & Plants":
    st.markdown('<h1 class="main-title">Traditional IKS Knowledge & Plant Explorer</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Source-Referenced Ayurvedic Lifestyle Principles and Botanical Repository</p>', unsafe_allow_html=True)

    tab_plants, tab_principles, tab_sources = st.tabs(["🌿 Medicinal Plants Repository", "📜 Curated IKS Lifestyle Principles", "🏛️ Authentic Sources & Citations"])

    with tab_plants:
        st.markdown("### Search & Explore Traditional Ayurvedic Botanicals")
        st.caption("Language note: Entries represent traditional Ayurvedic wellness knowledge and preclinical/clinical summaries. Not intended for disease treatment or pharmacological self-medication.")

        search_query = st.text_input("🔍 Search by common name, Sanskrit name, or suitable area (e.g., 'Ashwagandha', 'Stress', 'Turmeric', 'Digestion'):", "")
        plants_df = rec_engine.df_plants
        if not plants_df.empty:
            if search_query:
                q = search_query.lower()
                mask = (
                    plants_df["common_name"].str.lower().str.contains(q) |
                    plants_df["sanskrit_name"].str.lower().str.contains(q) |
                    plants_df["suitable_for"].str.lower().str.contains(q) |
                    plants_df["traditional_information"].str.lower().str.contains(q)
                )
                display_df = plants_df[mask]
            else:
                display_df = plants_df

            st.write(f"Showing **{len(display_df)}** traditional botanical entries:")
            for _, row in display_df.iterrows():
                with st.expander(f"🌿 {row['common_name']} ({row['scientific_name']}) — Sanskrit: {row['sanskrit_name']}"):
                    c1, c2 = st.columns([1, 1])
                    with c1:
                        st.markdown(f"**Traditional System:** {row['traditional_system']}")
                        st.markdown(f"**Classical Attributes (Rasa-Virya-Vipaka):** `{row['rasa_virya_vipaka']}`")
                        st.markdown(f"**Traditional Ayurvedic Information:** {row['traditional_information']}")
                        st.markdown(f"**Primary Areas of Lifestyle Support:** `{row['suitable_for']}`")
                    with c2:
                        st.markdown(f"**Modern Research Summary:** {row['modern_research_summary']}")
                        st.markdown(f"**Published References:** *{row['research_references']}*")
                        st.error(f"⚠️ **Safety & Caution Notes:** {row['safety_notes']}")

    with tab_principles:
        st.markdown("### Curated IKS Lifestyle & Wellness Principles")
        st.write("Deterministic, expert-curated knowledge base mapping lifestyle metrics to classical rules:")
        iks_df = rec_engine.df_iks
        if not iks_df.empty:
            st.dataframe(iks_df[["rule_id", "category", "iks_concept", "principle_name", "primary_source"]], use_container_width=True)

    with tab_sources:
        st.markdown("### Authentic Institutional & Classical Literature Citations")
        st.write("HealthSathi anchors all traditional knowledge and data metrics in verifiable institutional portals and peer-reviewed literature:")
        sources_df = rec_engine.df_sources
        if not sources_df.empty:
            for _, s in sources_df.iterrows():
                st.markdown(
                    f"""
                    - **[{s['source_name']}]({s['url']})** (`{s['source_id']}`)  
                      *Topic:* {s['topic']} | *Type:* {s['source_type']}  
                      *Note:* {s['notes']}
                    """
                )


# PAGE 6: Report Generation
elif page == "📑 My Wellness Report (PDF)":
    st.markdown('<h1 class="main-title">Personalized Wellness Report Generator</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Comprehensive 13-Section Wellness Report with Transparent Recommendations and PDF Export</p>', unsafe_allow_html=True)

    user_clean = clean_user_input(st.session_state.user_profile)
    scores = calculate_all_scores(user_clean)
    recommendations = rec_engine.evaluate_recommendations(user_clean)
    routine = rec_engine.generate_personalized_daily_routine(user_clean)
    relevant_plants = rec_engine.get_relevant_plants(user_clean)

    col_btn, col_info = st.columns([1, 2])
    with col_btn:
        generate_clicked = st.button("📄 Generate / Refresh My Wellness Report", type="primary", use_container_width=True)

    pdf_filename = f"reports/HealthSathi_Report_{user_clean['gender']}_{user_clean['age']}.pdf"
    generate_pdf_report(
        user_data=user_clean,
        scores=scores,
        recommendations=recommendations,
        routine=routine,
        plants=relevant_plants,
        sources_df=rec_engine.df_sources,
        output_pdf_path=pdf_filename
    )

    if os.path.exists(pdf_filename):
        with open(pdf_filename, "rb") as f:
            pdf_bytes = f.read()
        st.download_button(
            label="⬇️ Download Official PDF Wellness Report",
            data=pdf_bytes,
            file_name=os.path.basename(pdf_filename),
            mime="application/pdf",
            use_container_width=True
        )

    st.markdown("---")
    st.markdown("### 📑 Report Preview (Interactive View)")
    st.markdown("#### 🔍 Curated Recommendations & Explainability")
    st.caption("Every recommendation explicitly displays the triggering user habit, classical Ayurvedic rule, and source citation.")
    
    if recommendations:
        for idx, rec in enumerate(recommendations, 1):
            exp = rec.get("explainability", {})
            src = rec.get("source", {})
            with st.container():
                st.markdown(
                    f"""
                    <div style="background:#ffffff; border:1px solid #cbd5e1; border-radius:8px; padding:1rem; margin-bottom:1rem; box-shadow:0 1px 3px rgba(0,0,0,0.05);">
                        <div style="display:flex; justify-content:space-between; align-items:center;">
                            <span style="font-weight:700; color:#1e5128; font-size:1.05rem;">{idx}. {rec.get('principle_name')}</span>
                            <span class="iks-badge">{rec.get('category')} • {rec.get('iks_concept')}</span>
                        </div>
                        <p style="margin:0.5rem 0; color:#334155;"><strong>Guideline:</strong> {rec.get('recommendation_text')}</p>
                        <div style="background:#f8fafc; border-left:3px solid #f97316; padding:0.6rem; border-radius:4px; margin:0.5rem 0;">
                            <span style="color:#c2410c; font-weight:600;">Why am I getting this recommendation?</span><br/>
                            <span style="font-size:0.88rem; color:#475569;">
                                <strong>Your Input:</strong> {exp.get('user_trigger')}<br/>
                                <strong>IKS Rationale:</strong> {exp.get('reasoning')}
                            </span>
                        </div>
                        <div style="font-size:0.8rem; color:#64748b;">
                            📖 <strong>Source:</strong> <a href="{src.get('url')}" target="_blank">{src.get('name')}</a> | Ref: <em>{exp.get('primary_source')}</em>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
    else:
        st.success("Your lifestyle markers demonstrate balanced adherence to baseline principles. Continue maintaining regular circadian habits.")

    with st.expander("📝 View Full 13-Section Markdown Report Text"):
        full_md = generate_markdown_report(user_clean, scores, recommendations, routine, relevant_plants)
        st.markdown(full_md)


# PAGE 7: Research & Documentation
elif page == "🔬 Research & Documentation":
    st.markdown('<h1 class="main-title">Academic Research Paper & Article</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-title">Complete 14-Section Research Paper & 12-Section Science Article</p>', unsafe_allow_html=True)

    t_paper, t_art = st.tabs(["📄 Research Paper (14 Sections)", "📰 Public Science Article (12 Sections)"])
    paper_md_path = "research/research_paper.md"
    article_md_path = "research/article.md"
    paper_docx_path = "research/research_paper.docx"
    article_docx_path = "research/article.docx"

    with t_paper:
        st.markdown("### Research Paper: *HealthSathi*")
        st.caption("Title: *HealthSathi: A Data-Driven Framework for Personalized Wellness Using Indian Knowledge Systems and Ayurvedic Lifestyle Principles*")
        if os.path.exists(paper_docx_path):
            with open(paper_docx_path, "rb") as f:
                st.download_button("⬇️ Download Full Research Paper (.DOCX)", f.read(), "HealthSathi_Research_Paper.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        if os.path.exists(paper_md_path):
            with open(paper_md_path, "r", encoding="utf-8") as f:
                st.markdown(f.read())

    with t_art:
        st.markdown("### Public Science Article")
        st.caption("Title: *HealthSathi: Bringing Indian Traditional Wellness Knowledge into a Data-Driven Digital Lifestyle Assistant*")
        if os.path.exists(article_docx_path):
            with open(article_docx_path, "rb") as f:
                st.download_button("⬇️ Download Full Article (.DOCX)", f.read(), "HealthSathi_Article.docx", "application/vnd.openxmlformats-officedocument.wordprocessingml.document")
        if os.path.exists(article_md_path):
            with open(article_md_path, "r", encoding="utf-8") as f:
                st.markdown(f.read())
