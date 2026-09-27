"""
HealthSathi - Wellness Scoring Engine
Implements transparent mathematical scoring algorithms for 6 lifestyle dimensions
and computes the composite 0-100 Lifestyle Wellness Score.
"""

from typing import Dict, Any


def calculate_sleep_score(duration: float, quality: str, sleep_time_dec: float) -> float:
    if 7.0 <= duration <= 8.5:
        dur_score = 100.0
    elif duration < 7.0:
        dur_score = max(10.0, 100.0 - (7.0 - duration) * 22.0)
    else:
        dur_score = max(30.0, 100.0 - (duration - 8.5) * 18.0)

    q_str = str(quality).capitalize()
    q_offset = 12.0 if q_str == "Good" else (-15.0 if q_str == "Poor" else 0.0)

    eff_bedtime = sleep_time_dec if sleep_time_dec >= 12.0 else sleep_time_dec + 24.0
    if eff_bedtime <= 22.5:
        time_offset = 10.0
    elif eff_bedtime <= 23.5:
        time_offset = 5.0
    elif eff_bedtime <= 25.0:
        time_offset = -10.0
    else:
        time_offset = -20.0

    raw_score = dur_score * 0.70 + (50.0 + q_offset) * 0.20 + (50.0 + time_offset) * 0.10
    return round(float(min(100.0, max(5.0, raw_score))), 1)


def calculate_activity_score(physical_activity_min: float, outdoor_time_min: float, screen_time_hrs: float) -> float:
    act_pts = min(70.0, (physical_activity_min / 45.0) * 70.0)
    out_pts = min(30.0, (outdoor_time_min / 30.0) * 30.0)
    screen_pen = max(0.0, (screen_time_hrs - 8.0) * 4.0)
    raw_score = act_pts + out_pts - screen_pen
    return round(float(min(100.0, max(5.0, raw_score))), 1)


def calculate_stress_score(stress_level: int, mood: str, relaxation_activity: bool) -> float:
    stress_val = min(10, max(1, stress_level))
    base = (11 - stress_val) * 10.0
    m_str = str(mood).capitalize()
    m_offset = 10.0 if m_str == "Good" else (-15.0 if m_str == "Low" else 0.0)
    rel_offset = 10.0 if relaxation_activity else -8.0
    raw_score = base * 0.75 + (50.0 + m_offset) * 0.15 + (50.0 + rel_offset) * 0.10
    return round(float(min(100.0, max(5.0, raw_score))), 1)


def calculate_hydration_score(water_intake_liters: float, weight_kg: float, physical_activity_min: float) -> float:
    target = (weight_kg * 0.035) + (physical_activity_min / 60.0) * 0.5
    target = max(2.0, min(4.0, target))
    ratio = water_intake_liters / target
    if 0.90 <= ratio <= 1.30:
        score = 95.0 + (1.0 - abs(ratio - 1.0) * 2.5) * 5.0
    elif ratio < 0.90:
        score = max(10.0, ratio * 100.0)
    else:
        score = max(70.0, 100.0 - (ratio - 1.30) * 50.0)
    return round(float(min(100.0, max(5.0, score))), 1)


def calculate_routine_score(
    meal_regularity: str, 
    meal_timing_consistency: str, 
    work_study_hrs: float, 
    screen_time_hrs: float, 
    wake_time_dec: float
) -> float:
    meal_pts = 25.0 if str(meal_regularity).capitalize() == "Regular" else 5.0
    cons_pts = 25.0 if str(meal_timing_consistency).capitalize() == "Regular" else 5.0

    if work_study_hrs <= 8.5:
        work_pts = 20.0
    elif work_study_hrs <= 10.0:
        work_pts = 10.0
    else:
        work_pts = max(0.0, 20.0 - (work_study_hrs - 10.0) * 8.0)

    if screen_time_hrs <= 6.0:
        scr_pts = 15.0
    elif screen_time_hrs <= 8.5:
        scr_pts = 8.0
    else:
        scr_pts = max(0.0, 15.0 - (screen_time_hrs - 8.5) * 5.0)

    wake_hr = wake_time_dec % 24.0
    if wake_hr <= 6.5:
        wake_pts = 15.0
    elif wake_hr <= 8.0:
        wake_pts = 8.0
    else:
        wake_pts = 2.0

    raw_score = meal_pts + cons_pts + work_pts + scr_pts + wake_pts
    return round(float(min(100.0, max(10.0, raw_score))), 1)


def calculate_nutrition_score(
    breakfast_regular: bool, 
    fruit_veg_intake: str, 
    processed_food_freq: str, 
    caffeine_freq: str
) -> float:
    bf_pts = 20.0 if breakfast_regular else 0.0
    fv = str(fruit_veg_intake).capitalize()
    fv_pts = 40.0 if fv == "High" else (25.0 if fv == "Medium" else 10.0)
    pf = str(processed_food_freq).capitalize()
    pf_pts = 30.0 if pf == "Low" else (15.0 if pf == "Medium" else -5.0)
    caf = str(caffeine_freq).capitalize()
    caf_pts = 10.0 if caf == "Low" else (5.0 if caf == "Medium" else -8.0)
    raw_score = bf_pts + fv_pts + pf_pts + caf_pts
    return round(float(min(100.0, max(10.0, raw_score))), 1)


def calculate_overall_lifestyle_wellness_score(scores: Dict[str, float]) -> float:
    w_sleep = 0.22
    w_stress = 0.20
    w_act = 0.18
    w_nut = 0.18
    w_rout = 0.12
    w_hyd = 0.10

    overall = (
        scores.get("sleep_score", 60.0) * w_sleep +
        scores.get("stress_score", 60.0) * w_stress +
        scores.get("activity_score", 60.0) * w_act +
        scores.get("nutrition_score", 60.0) * w_nut +
        scores.get("routine_score", 60.0) * w_rout +
        scores.get("hydration_score", 60.0) * w_hyd
    )
    return round(float(min(100.0, max(5.0, overall))), 1)


def categorize_wellness_score(score: float) -> Dict[str, str]:
    if score >= 85.0:
        return {
            "band": "Excellent (Svastha)",
            "color": "#1b5e20",
            "summary": "Exemplary adherence to balanced circadian and nutritional rhythms."
        }
    elif score >= 70.0:
        return {
            "band": "Good (Prasanna)",
            "color": "#2e7d32",
            "summary": "Healthy foundational habits with minor potential optimizations."
        }
    elif score >= 55.0:
        return {
            "band": "Moderate (Madhyama)",
            "color": "#f57f17",
            "summary": "Inconsistent lifestyle routine; moderate susceptibility to fatigue and stress."
        }
    else:
        return {
            "band": "Needs Attention (Hina Vihara)",
            "color": "#c62828",
            "summary": "Substantial lifestyle strain across sleep, routine, or stress management."
        }


def calculate_all_scores(data: Dict[str, Any]) -> Dict[str, Any]:
    sleep = calculate_sleep_score(
        duration=data["sleep_duration_hrs"],
        quality=data["sleep_quality"],
        sleep_time_dec=data["sleep_time_dec"]
    )
    activity = calculate_activity_score(
        physical_activity_min=data["physical_activity_min"],
        outdoor_time_min=data["outdoor_time_min"],
        screen_time_hrs=data["screen_time_hrs"]
    )
    stress = calculate_stress_score(
        stress_level=data["stress_level"],
        mood=data["mood"],
        relaxation_activity=data["relaxation_activity"]
    )
    hydration = calculate_hydration_score(
        water_intake_liters=data["water_intake_liters"],
        weight_kg=data["weight_kg"],
        physical_activity_min=data["physical_activity_min"]
    )
    routine = calculate_routine_score(
        meal_regularity=data["meal_regularity"],
        meal_timing_consistency=data["meal_timing_consistency"],
        work_study_hrs=data["work_study_hrs"],
        screen_time_hrs=data["screen_time_hrs"],
        wake_time_dec=data["wake_up_time_dec"]
    )
    nutrition = calculate_nutrition_score(
        breakfast_regular=data["breakfast_regular"],
        fruit_veg_intake=data["fruit_veg_intake"],
        processed_food_freq=data["processed_food_freq"],
        caffeine_freq=data["caffeine_freq"]
    )

    scores_dict = {
        "sleep_score": sleep,
        "activity_score": activity,
        "stress_score": stress,
        "hydration_score": hydration,
        "routine_score": routine,
        "nutrition_score": nutrition,
    }

    overall = calculate_overall_lifestyle_wellness_score(scores_dict)
    cat_info = categorize_wellness_score(overall)

    scores_dict["overall_wellness_score"] = overall
    scores_dict["wellness_band"] = cat_info["band"]
    scores_dict["wellness_color"] = cat_info["color"]
    scores_dict["wellness_category"] = cat_info["band"]
    scores_dict["wellness_summary"] = cat_info["summary"]

    return scores_dict
