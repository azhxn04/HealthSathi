"""
HealthSathi - Transparent IKS Recommendation Engine & Dinacharya Generator
Implements deterministic, rule-based reasoning mapped to classical Ayurvedic principles,
source citations, and explainability cards ("Why am I getting this recommendation?").
"""

import os
import pandas as pd
from typing import Dict, Any, List, Optional
from src.preprocessing import parse_time_to_hours, format_hours_to_time


class RecommendationEngine:
    def __init__(self, data_dir: Optional[str] = None):
        if data_dir is None:
            data_dir = os.path.join(os.path.dirname(__file__), "..", "data")
        self.data_dir = data_dir
        self.iks_knowledge_path = os.path.join(data_dir, "iks_knowledge.csv")
        self.sources_path = os.path.join(data_dir, "sources.csv")
        self.plants_path = os.path.join(data_dir, "medicinal_plants.csv")

        self.df_iks = pd.read_csv(self.iks_knowledge_path) if os.path.exists(self.iks_knowledge_path) else pd.DataFrame()
        self.df_sources = pd.read_csv(self.sources_path) if os.path.exists(self.sources_path) else pd.DataFrame()
        self.df_plants = pd.read_csv(self.plants_path) if os.path.exists(self.plants_path) else pd.DataFrame()

    def get_source_info(self, source_id: str) -> Dict[str, str]:
        if self.df_sources.empty:
            return {"name": "Classical IKS Treatise", "url": "https://arp.ayush.gov.in/researchabout"}
        row = self.df_sources[self.df_sources["source_id"] == source_id]
        if not row.empty:
            return {
                "name": str(row.iloc[0]["source_name"]),
                "type": str(row.iloc[0]["source_type"]),
                "url": str(row.iloc[0]["url"]),
                "notes": str(row.iloc[0]["notes"])
            }
        return {"name": "Ayush Research Portal", "type": "Government Portal", "url": "https://arp.ayush.gov.in/researchabout", "notes": "Official reference"}

    def evaluate_recommendations(self, user_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        recommendations = []

        if user_data.get("sleep_duration_hrs", 7.0) < 6.5:
            rec = self._build_rec(
                rule_id="R-SLP-01",
                trigger_text=f"Your reported sleep duration is {user_data.get('sleep_duration_hrs')} hours (< 6.5 hr guideline).",
                user_data=user_data
            )
            if rec: recommendations.append(rec)

        sleep_dec = user_data.get("sleep_time_dec", 23.0)
        if sleep_dec >= 23.5 or (0.0 <= sleep_dec <= 4.0):
            rec = self._build_rec(
                rule_id="R-SLP-02",
                trigger_text=f"Your reported bedtime is {user_data.get('sleep_time_raw', 'late')} (after 11:30 PM).",
                user_data=user_data
            )
            if rec: recommendations.append(rec)

        if user_data.get("physical_activity_min", 30) < 30:
            rec = self._build_rec(
                rule_id="R-ACT-01",
                trigger_text=f"Your reported physical activity is {user_data.get('physical_activity_min')} min/day (< 30 min minimum).",
                user_data=user_data
            )
            if rec: recommendations.append(rec)

        if user_data.get("stress_level", 5) >= 7:
            rec = self._build_rec(
                rule_id="R-STR-01",
                trigger_text=f"Your reported stress score is {user_data.get('stress_level')}/10 (elevated psychological tension).",
                user_data=user_data
            )
            if rec: recommendations.append(rec)

        if not user_data.get("relaxation_activity", True):
            rec = self._build_rec(
                rule_id="R-STR-02",
                trigger_text="You indicated not engaging in any regular relaxation or mindfulness activity.",
                user_data=user_data
            )
            if rec: recommendations.append(rec)

        if user_data.get("water_intake_liters", 2.0) < 2.0:
            rec = self._build_rec(
                rule_id="R-HYD-01",
                trigger_text=f"Your reported daily water intake is {user_data.get('water_intake_liters')} L (< 2.0 L recommended baseline).",
                user_data=user_data
            )
            if rec: recommendations.append(rec)

        if not user_data.get("breakfast_regular", True):
            rec = self._build_rec(
                rule_id="R-NUT-01",
                trigger_text="You reported skipping regular morning breakfast.",
                user_data=user_data
            )
            if rec: recommendations.append(rec)

        if str(user_data.get("processed_food_freq", "")).capitalize() == "High":
            rec = self._build_rec(
                rule_id="R-NUT-02",
                trigger_text="You reported a High frequency of processed / ultra-packaged food consumption.",
                user_data=user_data
            )
            if rec: recommendations.append(rec)

        if str(user_data.get("caffeine_freq", "")).capitalize() == "High":
            rec = self._build_rec(
                rule_id="R-NUT-03",
                trigger_text="You reported a High frequency of daily caffeine consumption.",
                user_data=user_data
            )
            if rec: recommendations.append(rec)

        if user_data.get("screen_time_hrs", 6.0) > 7.0:
            rec = self._build_rec(
                rule_id="R-ROU-01",
                trigger_text=f"Your daily digital screen exposure is {user_data.get('screen_time_hrs')} hours (> 7.0 hr threshold).",
                user_data=user_data
            )
            if rec: recommendations.append(rec)

        if user_data.get("outdoor_time_min", 30) < 20:
            rec = self._build_rec(
                rule_id="R-ROU-02",
                trigger_text=f"Your outdoor natural sunlight exposure is {user_data.get('outdoor_time_min')} min/day (< 20 min guideline).",
                user_data=user_data
            )
            if rec: recommendations.append(rec)

        if str(user_data.get("meal_regularity", "")).capitalize() == "Irregular":
            rec = self._build_rec(
                rule_id="R-ROU-03",
                trigger_text="You reported irregular or erratic daily meal timings.",
                user_data=user_data
            )
            if rec: recommendations.append(rec)

        conds = user_data.get("health_conditions", ["None"])
        if any(c not in ["None", ""] for c in conds):
            cond_str = ", ".join([c for c in conds if c not in ["None", ""]])
            rec = self._build_rec(
                rule_id="R-CND-01",
                trigger_text=f"Self-reported health condition context noted: {cond_str}.",
                user_data=user_data
            )
            if rec: recommendations.append(rec)

        return recommendations

    def _build_rec(self, rule_id: str, trigger_text: str, user_data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        if self.df_iks.empty:
            return None
        row = self.df_iks[self.df_iks["rule_id"] == rule_id]
        if row.empty:
            return None
        r = row.iloc[0]
        source_meta = self.get_source_info(str(r["source_id"]))

        return {
            "rule_id": str(r["rule_id"]),
            "category": str(r["category"]),
            "principle_name": str(r["principle_name"]),
            "iks_concept": str(r["iks_concept"]),
            "traditional_guideline": str(r["traditional_guideline"]),
            "recommendation_text": str(r["recommendation_text"]),
            "explainability": {
                "user_trigger": trigger_text,
                "reasoning": str(r["explainability_reason"]),
                "iks_concept": str(r["iks_concept"]),
                "primary_source": str(r["primary_source"])
            },
            "source": source_meta
        }

    def generate_personalized_daily_routine(self, user_data: Dict[str, Any]) -> List[Dict[str, str]]:
        wake_hr = user_data.get("wake_up_time_dec", 6.5) % 24.0
        sleep_hr = user_data.get("sleep_time_dec", 23.0) % 24.0
        work_hrs = float(user_data.get("work_study_hrs", 8.0))
        act_min = float(user_data.get("physical_activity_min", 30.0))

        t_wake = wake_hr
        t_movement = (t_wake + 0.5) % 24.0
        t_breakfast = (t_wake + 1.25) % 24.0
        t_work_start = (t_wake + 2.25) % 24.0
        t_midday_break = (t_work_start + 2.5) % 24.0
        t_lunch = 13.0
        t_afternoon_focus = 14.5
        t_outdoor_exercise = (17.5 if act_min >= 20 else 18.0)
        t_dinner = 19.5
        t_relaxation = 20.5
        t_digital_dusk = max(21.0, (sleep_hr - 1.5) % 24.0 if sleep_hr >= 12 else (sleep_hr + 24 - 1.5) % 24.0)
        t_sleep_prep = max(21.5, (sleep_hr - 0.75) % 24.0 if sleep_hr >= 12 else (sleep_hr + 24 - 0.75) % 24.0)
        t_sleep = sleep_hr

        schedule = [
            {
                "time": format_hours_to_time(t_wake),
                "phase": "Brahma Muhurta / Ushahkala",
                "activity": "Awaken Mindfully & Ushnodaka Hydration",
                "details": "Rise quietly. Cleanse eyes, mouth, and tongue (Jihwa Nirlekhana). Sip 1-2 glasses of warm lukewarm water to awaken peristalsis (Agni Deepana).",
                "dosha_focus": "Vata to Kapha Transition"
            },
            {
                "time": format_hours_to_time(t_movement),
                "phase": "Pratah Vyayama",
                "activity": "Light Physical Movement / Yoga / Surya Namaskar",
                "details": f"Perform {int(max(20, min(60, act_min)))} minutes of mindful exercise up to half your capacity (Ardhshakti). Include gentle joint loosening and 5 minutes of Sukhasana breathwork.",
                "dosha_focus": "Kapha Pacification (Circulation & Agni)"
            },
            {
                "time": format_hours_to_time(t_breakfast),
                "phase": "Pratarasa (Breakfast)",
                "activity": "Warm Grounding Nourishment",
                "details": "Freshly cooked, warm meal (e.g. spiced whole grains, warm porridge, stewed fruits). Avoid cold smoothies or heavy fried items.",
                "dosha_focus": "Pitta Sparking & Energy Grounding"
            },
            {
                "time": format_hours_to_time(t_work_start),
                "phase": "Karma Yoga (Morning Focus)",
                "activity": "Deep Focused Work / Academic Study",
                "details": "Tackle the most demanding analytical or strategic tasks while mental clarity (Sattva) is peak and distractions are minimal.",
                "dosha_focus": "Kapha Stability & Clarity"
            },
            {
                "time": format_hours_to_time(t_midday_break),
                "phase": "Prana Pause",
                "activity": "Sensory Rest & Hydration",
                "details": "Step away from screens for 5-10 minutes. Practice 20-20-20 eye relaxation and sip room-temperature water or herbal tea.",
                "dosha_focus": "Alochak Pitta (Eye Strain Relief)"
            },
            {
                "time": format_hours_to_time(t_lunch),
                "phase": "Madhyanha Bhojana (Primary Lunch)",
                "activity": "Main Substantial Meal of the Day",
                "details": "The solar fire is at its zenith; digestive Agni is strongest. Enjoy your most substantial, balanced meal with all six tastes (Shad-Rasa) in a calm setting without screens.",
                "dosha_focus": "Peak Pitta Agni (Optimal Assimilation)"
            },
            {
                "time": format_hours_to_time(t_afternoon_focus),
                "phase": "Apara Karma",
                "activity": "Collaborative Work & Creative Execution",
                "details": "Afternoon tasks, communications, administrative duties, or creative exploration. Keep posture upright.",
                "dosha_focus": "Vata Creative Window"
            },
            {
                "time": format_hours_to_time(t_outdoor_exercise),
                "phase": "Sandhyakala Movement",
                "activity": "Outdoor Walk & Natural Sunlight",
                "details": "Step outdoors for 25-35 minutes. Natural light exposure during late afternoon supports circadian alignment, mood regulation, and gentle movement.",
                "dosha_focus": "Vata Balancing & Transition"
            },
            {
                "time": format_hours_to_time(t_dinner),
                "phase": "Ratri Bhojana (Light Dinner)",
                "activity": "Warm, Light, Easily Digestible Supper",
                "details": "A lighter dinner consumed at least 2.5 to 3 hours before sleep. Warm vegetable soups, spiced lentils (Mung dal), or steamed greens.",
                "dosha_focus": "Agni Preservation & Digestion"
            },
            {
                "time": format_hours_to_time(t_relaxation),
                "phase": "Sadvritta & Manasika Shanti",
                "activity": "Conscious Relaxation & Family / Reflection Time",
                "details": "Engage in calming leisure, gentle conversation, contemplative reading, or Nadi Shodhana (Alternate Nostril Breathwork).",
                "dosha_focus": "Prana Vata Calming"
            },
            {
                "time": format_hours_to_time(t_digital_dusk),
                "phase": "Netra Shanti (Digital Dusk)",
                "activity": "Screen Shutoff & Blue-Light Elimination",
                "details": "Power down high-luminance smartphones, laptops, and TVs. Switch home lighting to warm, ambient, dim tones to signal nocturnal melatonin synthesis.",
                "dosha_focus": "Sensory Withdrawal (Pratyahara)"
            },
            {
                "time": format_hours_to_time(t_sleep_prep),
                "phase": "Ratricharya Ritual",
                "activity": "Padabhyanga (Foot Massage) & Bedtime Quietude",
                "details": "Gently massage the soles of your feet with a few drops of warm sesame oil or cow's ghee (Padabhyanga) to induce deep sleep and ground nervous system tension.",
                "dosha_focus": "Vata Pacification & Somnolence"
            },
            {
                "time": format_hours_to_time(t_sleep),
                "phase": "Sushupti (Restorative Sleep)",
                "activity": "Deep Sleep Window",
                "details": "Rest in a well-ventilated, dark room. Entering sleep before the 11:00 PM late-night Pitta cycle allows natural cellular detoxification and tissue rejuvenation (Dhatu Poshana).",
                "dosha_focus": "Kapha Restoration & Ojas Replenishment"
            }
        ]
        return schedule

    def get_relevant_plants(self, user_data: Dict[str, Any]) -> List[Dict[str, Any]]:
        if self.df_plants.empty:
            return []

        matched_plants = []
        stress = user_data.get("stress_level", 5)
        sleep_dur = user_data.get("sleep_duration_hrs", 7.0)
        activity = user_data.get("physical_activity_min", 30.0)
        screen = user_data.get("screen_time_hrs", 6.0)
        processed = str(user_data.get("processed_food_freq", "")).capitalize()

        tags_needed = []
        if stress >= 6 or sleep_dur < 6.5:
            tags_needed.extend(["Ashwagandha", "Tulsi (Holy Basil)"])
        if screen > 7.0 or user_data.get("occupation") in ["Student", "Working Professional (IT/Corporate)"]:
            tags_needed.append("Brahmi")
        if processed == "High" or user_data.get("meal_regularity") == "Irregular":
            tags_needed.extend(["Ginger", "Amla (Indian Gooseberry)"])
        if activity > 40:
            tags_needed.append("Turmeric")

        if len(tags_needed) < 3:
            tags_needed.extend(["Amla (Indian Gooseberry)", "Turmeric", "Tulsi (Holy Basil)"])

        unique_tags = []
        for t in tags_needed:
            if t not in unique_tags:
                unique_tags.append(t)

        for tag in unique_tags[:4]:
            match = self.df_plants[self.df_plants["common_name"] == tag]
            if not match.empty:
                matched_plants.append(match.iloc[0].to_dict())

        return matched_plants
