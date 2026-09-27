"""
HealthSathi - Preprocessing & Feature Engineering Module
Handles data cleaning, unit conversions, circadian time parsing, BMI, and synthetic cohort generation.
"""

import os
import re
import numpy as np
import pandas as pd
from typing import Dict, Any, Tuple, Optional


def parse_time_to_hours(time_str: Any) -> float:
    """
    Parses time strings like '11:30 PM', '6:00 AM', '23:30', or numeric hours to decimal 24-hr float.
    Returns float in range [0.0, 24.0).
    """
    if pd.isna(time_str):
        return 7.0
    if isinstance(time_str, (int, float)):
        return float(time_str % 24.0)

    time_str = str(time_str).strip()
    match_12 = re.match(r"^(\d{1,2}):?(\d{2})?\s*(AM|PM)?$", time_str, re.IGNORECASE)
    if match_12:
        hr = int(match_12.group(1))
        mn = int(match_12.group(2)) if match_12.group(2) else 0
        meridiem = match_12.group(3)
        if meridiem:
            meridiem = meridiem.upper()
            if meridiem == "PM" and hr < 12:
                hr += 12
            elif meridiem == "AM" and hr == 12:
                hr = 0
        return (hr % 24) + (mn / 60.0)

    nums = re.findall(r"\d+\.?\d*", time_str)
    if nums:
        return float(nums[0]) % 24.0
    return 7.0


def format_hours_to_time(dec_hours: float) -> str:
    """
    Converts decimal hours (e.g. 23.5) into human-readable 12-hour AM/PM string ('11:30 PM').
    """
    dec_hours = dec_hours % 24.0
    hr = int(dec_hours)
    mn = int(round((dec_hours - hr) * 60))
    if mn == 60:
        hr = (hr + 1) % 24
        mn = 0

    meridiem = "AM" if hr < 12 else "PM"
    display_hr = hr % 12
    if display_hr == 0:
        display_hr = 12
    return f"{display_hr:02d}:{mn:02d} {meridiem}"


def calculate_bmi(weight_kg: float, height_cm: float) -> Tuple[float, str]:
    """
    Calculates Body Mass Index (BMI) and qualitative classification.
    """
    if height_cm <= 0 or weight_kg <= 0:
        return 22.0, "Normal"
    height_m = height_cm / 100.0
    bmi = weight_kg / (height_m ** 2)
    bmi = round(bmi, 1)

    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25.0:
        category = "Normal"
    elif bmi < 30.0:
        category = "Overweight"
    else:
        category = "Obesity Range"

    return bmi, category


def clean_user_input(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Validates and normalizes user profile inputs into standardized types and ranges.
    """
    cleaned = dict(data)

    cleaned["age"] = int(cleaned.get("age", 25))
    cleaned["gender"] = str(cleaned.get("gender", "Female")).capitalize()
    cleaned["height_cm"] = float(cleaned.get("height_cm", 168.0))
    cleaned["weight_kg"] = float(cleaned.get("weight_kg", 62.0))
    cleaned["occupation"] = str(cleaned.get("occupation", "Working Professional"))

    bmi_val, bmi_cat = calculate_bmi(cleaned["weight_kg"], cleaned["height_cm"])
    cleaned["bmi"] = bmi_val
    cleaned["bmi_category"] = bmi_cat

    cleaned["sleep_duration_hrs"] = float(cleaned.get("sleep_duration_hrs", 7.0))
    cleaned["sleep_time_raw"] = str(cleaned.get("sleep_time_raw", "11:00 PM"))
    cleaned["wake_up_time_raw"] = str(cleaned.get("wake_up_time_raw", "06:30 AM"))
    cleaned["sleep_time_dec"] = parse_time_to_hours(cleaned["sleep_time_raw"])
    cleaned["wake_up_time_dec"] = parse_time_to_hours(cleaned["wake_up_time_raw"])
    cleaned["sleep_quality"] = str(cleaned.get("sleep_quality", "Good")).capitalize()

    cleaned["work_study_hrs"] = float(cleaned.get("work_study_hrs", 8.0))
    cleaned["screen_time_hrs"] = float(cleaned.get("screen_time_hrs", 6.0))
    cleaned["physical_activity_min"] = float(cleaned.get("physical_activity_min", 30.0))
    cleaned["water_intake_liters"] = float(cleaned.get("water_intake_liters", 2.2))
    cleaned["meal_regularity"] = str(cleaned.get("meal_regularity", "Regular")).capitalize()
    cleaned["outdoor_time_min"] = float(cleaned.get("outdoor_time_min", 30.0))

    cleaned["stress_level"] = int(cleaned.get("stress_level", 5))
    cleaned["mood"] = str(cleaned.get("mood", "Neutral")).capitalize()
    cleaned["relaxation_activity"] = bool(cleaned.get("relaxation_activity", True))

    cleaned["breakfast_regular"] = bool(cleaned.get("breakfast_regular", True))
    cleaned["fruit_veg_intake"] = str(cleaned.get("fruit_veg_intake", "Medium")).capitalize()
    cleaned["processed_food_freq"] = str(cleaned.get("processed_food_freq", "Low")).capitalize()
    cleaned["caffeine_freq"] = str(cleaned.get("caffeine_freq", "Low")).capitalize()
    cleaned["meal_timing_consistency"] = str(cleaned.get("meal_timing_consistency", "Regular")).capitalize()

    conds = cleaned.get("health_conditions", ["None"])
    if isinstance(conds, str):
        conds = [c.strip() for c in conds.split(";") if c.strip()]
    if not conds:
        conds = ["None"]
    if len(conds) > 1 and "None" in conds:
        conds.remove("None")
    cleaned["health_conditions"] = conds

    return cleaned


def generate_synthetic_dataset(n_samples: int = 650, output_path: Optional[str] = None, seed: int = 42) -> pd.DataFrame:
    """
    Generates a realistic synthetic cohort of lifestyle records for prototype evaluation.
    Clearly marked as synthetic in compliance with Section 11 and Section 19.
    """
    from src.scoring import calculate_all_scores

    np.random.seed(seed)
    occupations = [
        "Student", "Working Professional (IT/Corporate)", "Healthcare Worker", 
        "Educator / Academic", "Self-Employed / Business", "Homemaker", "Freelancer / Creative"
    ]
    genders = ["Female", "Male", "Other"]
    qualities = ["Poor", "Moderate", "Good"]
    levels_3 = ["Low", "Medium", "High"]
    regularity = ["Regular", "Irregular"]
    moods = ["Low", "Neutral", "Good"]
    conditions_pool = [
        "None", "Diabetes", "Hypertension", "Migraine", "Asthma", "Arthritis",
        "Thyroid disorder", "Digestive problems", "Anxiety/stress-related concerns"
    ]

    records = []
    for i in range(n_samples):
        archetype_roll = np.random.rand()
        if archetype_roll < 0.28:
            age = int(np.random.randint(20, 42))
            gender = np.random.choice(genders, p=[0.48, 0.48, 0.04])
            occupation = np.random.choice(["Student", "Working Professional (IT/Corporate)", "Freelancer / Creative"])
            height = float(np.random.normal(168, 8))
            weight = float(np.random.normal(70, 12))
            sleep_duration = float(np.clip(np.random.normal(5.8, 0.9), 3.5, 7.5))
            sleep_time_dec = float(np.clip(np.random.normal(24.2, 0.8) % 24, 22.5, 25.5 % 24))
            wake_up_time_dec = float((sleep_time_dec + sleep_duration) % 24)
            sleep_quality = np.random.choice(qualities, p=[0.55, 0.35, 0.10])
            work_study = float(np.clip(np.random.normal(9.5, 1.5), 6.0, 14.0))
            screen_time = float(np.clip(np.random.normal(8.8, 1.8), 5.5, 14.0))
            physical_activity = float(np.clip(np.random.normal(15, 12), 0, 45))
            water_intake = float(np.clip(np.random.normal(1.7, 0.5), 0.8, 3.2))
            outdoor_time = float(np.clip(np.random.normal(15, 10), 0, 40))
            stress_level = int(np.clip(np.random.normal(7.8, 1.4), 5, 10))
            mood = np.random.choice(moods, p=[0.45, 0.45, 0.10])
            relaxation_act = bool(np.random.rand() < 0.25)
            breakfast_reg = bool(np.random.rand() < 0.40)
            fruit_veg = np.random.choice(levels_3, p=[0.45, 0.45, 0.10])
            processed_food = np.random.choice(levels_3, p=[0.10, 0.40, 0.50])
            caffeine_freq = np.random.choice(levels_3, p=[0.10, 0.35, 0.55])
            meal_reg = np.random.choice(regularity, p=[0.30, 0.70])
            meal_consistency = meal_reg
            cond = np.random.choice(conditions_pool, p=[0.40, 0.05, 0.05, 0.12, 0.03, 0.02, 0.05, 0.15, 0.13])
        elif archetype_roll < 0.65:
            age = int(np.random.randint(22, 60))
            gender = np.random.choice(genders, p=[0.50, 0.47, 0.03])
            occupation = np.random.choice(occupations)
            height = float(np.random.normal(167, 9))
            weight = float(np.random.normal(64, 9))
            sleep_duration = float(np.clip(np.random.normal(7.6, 0.6), 6.5, 8.8))
            sleep_time_dec = float(np.clip(np.random.normal(22.4, 0.5), 21.5, 23.2))
            wake_up_time_dec = float((sleep_time_dec + sleep_duration) % 24)
            sleep_quality = np.random.choice(qualities, p=[0.05, 0.25, 0.70])
            work_study = float(np.clip(np.random.normal(7.5, 1.0), 5.0, 9.0))
            screen_time = float(np.clip(np.random.normal(4.8, 1.2), 2.5, 7.5))
            physical_activity = float(np.clip(np.random.normal(45, 15), 25, 90))
            water_intake = float(np.clip(np.random.normal(2.6, 0.4), 2.0, 3.8))
            outdoor_time = float(np.clip(np.random.normal(40, 15), 20, 80))
            stress_level = int(np.clip(np.random.normal(3.4, 1.3), 1, 6))
            mood = np.random.choice(moods, p=[0.05, 0.30, 0.65])
            relaxation_act = bool(np.random.rand() < 0.85)
            breakfast_reg = bool(np.random.rand() < 0.90)
            fruit_veg = np.random.choice(levels_3, p=[0.05, 0.35, 0.60])
            processed_food = np.random.choice(levels_3, p=[0.65, 0.30, 0.05])
            caffeine_freq = np.random.choice(levels_3, p=[0.55, 0.35, 0.10])
            meal_reg = "Regular"
            meal_consistency = "Regular"
            cond = np.random.choice(conditions_pool, p=[0.75, 0.03, 0.03, 0.03, 0.03, 0.03, 0.04, 0.03, 0.03])
        else:
            age = int(np.random.randint(19, 55))
            gender = np.random.choice(genders, p=[0.48, 0.49, 0.03])
            occupation = np.random.choice(occupations)
            height = float(np.random.normal(166, 9))
            weight = float(np.random.normal(67, 11))
            sleep_duration = float(np.clip(np.random.normal(6.6, 1.1), 4.5, 9.0))
            sleep_time_dec = float(np.clip(np.random.normal(23.5, 1.0) % 24, 21.0, 26.0 % 24))
            wake_up_time_dec = float((sleep_time_dec + sleep_duration) % 24)
            sleep_quality = np.random.choice(qualities, p=[0.25, 0.50, 0.25])
            work_study = float(np.clip(np.random.normal(8.0, 1.8), 4.0, 12.0))
            screen_time = float(np.clip(np.random.normal(6.5, 1.8), 3.0, 11.0))
            physical_activity = float(np.clip(np.random.normal(30, 18), 0, 70))
            water_intake = float(np.clip(np.random.normal(2.1, 0.6), 1.0, 3.5))
            outdoor_time = float(np.clip(np.random.normal(25, 15), 5, 60))
            stress_level = int(np.clip(np.random.normal(5.6, 1.8), 2, 9))
            mood = np.random.choice(moods, p=[0.20, 0.60, 0.20])
            relaxation_act = bool(np.random.rand() < 0.45)
            breakfast_reg = bool(np.random.rand() < 0.65)
            fruit_veg = np.random.choice(levels_3, p=[0.20, 0.55, 0.25])
            processed_food = np.random.choice(levels_3, p=[0.25, 0.50, 0.25])
            caffeine_freq = np.random.choice(levels_3, p=[0.25, 0.50, 0.25])
            meal_reg = np.random.choice(regularity, p=[0.50, 0.50])
            meal_consistency = meal_reg
            cond = np.random.choice(conditions_pool, p=[0.60, 0.05, 0.05, 0.06, 0.04, 0.04, 0.05, 0.06, 0.05])

        height = round(height, 1)
        weight = round(weight, 1)
        bmi, bmi_cat = calculate_bmi(weight, height)

        user_dict = {
            "participant_id": f"HS-SYNTH-{i+1:04d}",
            "data_source_nature": "Synthetic Evaluation Record (Simulated Cohort)",
            "age": age,
            "gender": gender,
            "height_cm": height,
            "weight_kg": weight,
            "bmi": bmi,
            "bmi_category": bmi_cat,
            "occupation": occupation,
            "sleep_duration_hrs": round(sleep_duration, 1),
            "sleep_time_dec": round(sleep_time_dec, 2),
            "wake_up_time_dec": round(wake_up_time_dec, 2),
            "sleep_time_str": format_hours_to_time(sleep_time_dec),
            "wake_up_time_str": format_hours_to_time(wake_up_time_dec),
            "sleep_quality": sleep_quality,
            "work_study_hrs": round(work_study, 1),
            "screen_time_hrs": round(screen_time, 1),
            "physical_activity_min": round(physical_activity, 0),
            "water_intake_liters": round(water_intake, 1),
            "meal_regularity": meal_reg,
            "outdoor_time_min": round(outdoor_time, 0),
            "stress_level": stress_level,
            "mood": mood,
            "relaxation_activity": relaxation_act,
            "breakfast_regular": breakfast_reg,
            "fruit_veg_intake": fruit_veg,
            "processed_food_freq": processed_food,
            "caffeine_freq": caffeine_freq,
            "meal_timing_consistency": meal_consistency,
            "health_conditions": cond,
        }

        scores = calculate_all_scores(clean_user_input(user_dict))
        user_dict.update({
            "sleep_score": scores["sleep_score"],
            "activity_score": scores["activity_score"],
            "stress_score": scores["stress_score"],
            "hydration_score": scores["hydration_score"],
            "routine_score": scores["routine_score"],
            "nutrition_score": scores["nutrition_score"],
            "lifestyle_wellness_score": scores["overall_wellness_score"],
            "wellness_category": scores["wellness_category"],
        })
        records.append(user_dict)

    df = pd.DataFrame(records)
    if output_path:
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        df.to_csv(output_path, index=False)
        print(f"Saved {len(df)} synthetic lifestyle records to {output_path}")

    return df
