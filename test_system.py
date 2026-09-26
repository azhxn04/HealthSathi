"""
HealthSathi - Automated End-to-End System Test Suite
Verifies data pipeline, scoring consistency, rule engine, PDF/DOCX compilation,
ML models, PBKDF2 password hashing, RBAC permissions, and security audit logging.
"""

import os
import unittest
from src.preprocessing import clean_user_input, parse_time_to_hours, format_hours_to_time
from src.scoring import calculate_all_scores
from src.recommendations import RecommendationEngine
from src.report_generator import generate_pdf_report, generate_docx_report
from src.ml_models import LifestyleMLAnalytics
from src.security import (
    hash_password, verify_password, UserManager, check_permission,
    export_user_data_package, SecurityAuditLogger
)


class TestHealthSathiSystem(unittest.TestCase):
    def setUp(self):
        self.rec_engine = RecommendationEngine()
        self.ml_analytics = LifestyleMLAnalytics()
        self.user_manager = UserManager()
        self.sample_user = {
            "age": 28, "gender": "Male", "height_cm": 175.0, "weight_kg": 72.0,
            "occupation": "Working Professional (IT/Corporate)", "sleep_duration_hrs": 5.5,
            "sleep_time_raw": "01:00 AM", "wake_up_time_raw": "06:30 AM", "sleep_quality": "Poor",
            "work_study_hrs": 9.5, "screen_time_hrs": 9.0, "physical_activity_min": 15.0,
            "water_intake_liters": 1.6, "meal_regularity": "Irregular", "outdoor_time_min": 15.0,
            "stress_level": 8, "mood": "Low", "relaxation_activity": False,
            "breakfast_regular": False, "fruit_veg_intake": "Low", "processed_food_freq": "High",
            "caffeine_freq": "High", "meal_timing_consistency": "Irregular",
            "health_conditions": ["Anxiety/stress-related concerns"]
        }

    def test_preprocessing(self):
        cleaned = clean_user_input(self.sample_user)
        self.assertEqual(cleaned["age"], 28)
        self.assertAlmostEqual(cleaned["bmi"], 23.5, places=1)
        self.assertEqual(cleaned["bmi_category"], "Normal")
        self.assertAlmostEqual(cleaned["sleep_time_dec"], 1.0)
        self.assertAlmostEqual(cleaned["wake_up_time_dec"], 6.5)

    def test_scoring(self):
        cleaned = clean_user_input(self.sample_user)
        scores = calculate_all_scores(cleaned)
        for k in ["sleep_score", "activity_score", "stress_score", "hydration_score", "routine_score", "nutrition_score", "overall_wellness_score"]:
            self.assertIn(k, scores)
            self.assertGreaterEqual(scores[k], 0.0)
            self.assertLessEqual(scores[k], 100.0)
        self.assertIn("wellness_band", scores)
        self.assertIn("wellness_color", scores)

    def test_recommendation_engine(self):
        cleaned = clean_user_input(self.sample_user)
        recs = self.rec_engine.evaluate_recommendations(cleaned)
        self.assertGreater(len(recs), 0)
        first_rec = recs[0]
        self.assertIn("rule_id", first_rec)
        self.assertIn("explainability", first_rec)
        self.assertIn("user_trigger", first_rec["explainability"])
        self.assertIn("reasoning", first_rec["explainability"])
        self.assertIn("source", first_rec)

    def test_dinacharya_routine(self):
        cleaned = clean_user_input(self.sample_user)
        routine = self.rec_engine.generate_personalized_daily_routine(cleaned)
        self.assertGreaterEqual(len(routine), 10)
        self.assertIn("time", routine[0])
        self.assertIn("phase", routine[0])
        self.assertIn("activity", routine[0])

    def test_pdf_report_compilation(self):
        cleaned = clean_user_input(self.sample_user)
        scores = calculate_all_scores(cleaned)
        recs = self.rec_engine.evaluate_recommendations(cleaned)
        routine = self.rec_engine.generate_personalized_daily_routine(cleaned)
        plants = self.rec_engine.get_relevant_plants(cleaned)
        test_pdf = "reports/test_verification_report.pdf"
        out_path = generate_pdf_report(
            user_data=cleaned, scores=scores, recommendations=recs, routine=routine,
            plants=plants, sources_df=self.rec_engine.df_sources, output_pdf_path=test_pdf
        )
        self.assertTrue(os.path.exists(out_path))
        self.assertGreater(os.path.getsize(out_path), 5000)

    def test_docx_report_compilation(self):
        cleaned = clean_user_input(self.sample_user)
        scores = calculate_all_scores(cleaned)
        recs = self.rec_engine.evaluate_recommendations(cleaned)
        routine = self.rec_engine.generate_personalized_daily_routine(cleaned)
        plants = self.rec_engine.get_relevant_plants(cleaned)
        test_docx = "reports/test_verification_report.docx"
        out_path = generate_docx_report(
            user_data=cleaned, scores=scores, recommendations=recs, routine=routine,
            plants=plants, sources_df=self.rec_engine.df_sources, output_docx_path=test_docx
        )
        self.assertTrue(os.path.exists(out_path))
        self.assertGreater(os.path.getsize(out_path), 5000)

    def test_ml_archetype(self):
        cleaned = clean_user_input(self.sample_user)
        archetype, importances = self.ml_analytics.predict_archetype(cleaned)
        self.assertIsInstance(archetype, str)
        self.assertIsInstance(importances, dict)
        self.assertGreater(len(importances), 0)

    def test_password_hashing_and_verification(self):
        raw_pw = "AyurVeda#Secure2026!"
        hashed = hash_password(raw_pw)
        self.assertTrue(hashed.startswith("pbkdf2_sha256$120000$"))
        self.assertTrue(verify_password(raw_pw, hashed))
        self.assertFalse(verify_password("WrongPassword123", hashed))

    def test_user_authentication_and_rbac(self):
        success, session, msg = self.user_manager.authenticate("admin", "Admin@HealthSathi2026")
        self.assertTrue(success)
        self.assertIsNotNone(session)
        self.assertEqual(session["role"], "admin")
        self.assertTrue(check_permission("admin", "access_admin_console"))
        self.assertFalse(check_permission("viewer", "access_admin_console"))
        self.assertTrue(check_permission("viewer", "view_overview"))

    def test_audit_logging_and_privacy_export(self):
        audit = SecurityAuditLogger()
        audit.log_event("UNIT_TEST_EVENT", "test_user", "user", "SUCCESS", "Testing audit logger")
        logs = audit.get_recent_logs(limit=5)
        self.assertFalse(logs.empty)
        
        cleaned = clean_user_input(self.sample_user)
        scores = calculate_all_scores(cleaned)
        pkg_json = export_user_data_package(cleaned, scores)
        self.assertIn("compliance", pkg_json)
        self.assertIn("DPDP Act 2023", pkg_json)


if __name__ == "__main__":
    unittest.main()
