"""
HealthSathi - Machine Learning & Archetype Analytics Module
Provides unsupervised clustering (K-Means) and feature importance analysis (Random Forest)
trained on the lifestyle cohort to identify behavioral archetypes and key lifestyle drivers.
"""

import os
import pandas as pd
import numpy as np
from typing import Dict, Any, Tuple
from sklearn.cluster import KMeans
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler


class LifestyleMLAnalytics:
    def __init__(self, data_path: str = "data/lifestyle_data.csv"):
        self.data_path = data_path
        self.scaler = StandardScaler()
        self.kmeans = None
        self.rf = None
        self.feature_cols = [
            "sleep_duration_hrs", "physical_activity_min", "water_intake_liters",
            "screen_time_hrs", "outdoor_time_min", "stress_level", "bmi"
        ]
        self.archetype_labels = {
            0: "Balanced Circadian Lifestyle (Svastha)",
            1: "High-Stress Sedentary Lifestyle (Rajasika Strain)",
            2: "Irregular Routine & Circadian Drift (Vata Disturbance)",
            3: "Active but Sleep-Constrained (Pitta/Vata Tension)"
        }
        self.is_trained = False
        self._train_if_data_exists()

    def _train_if_data_exists(self):
        if not os.path.exists(self.data_path):
            return
        try:
            df = pd.read_csv(self.data_path)
            if len(df) < 50:
                return

            X = df[self.feature_cols].copy().fillna(df[self.feature_cols].median())
            X_scaled = self.scaler.fit_transform(X)

            self.kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
            self.kmeans.fit(X_scaled)

            y = df["wellness_category"].astype(str)
            self.rf = RandomForestClassifier(n_estimators=100, random_state=42, max_depth=6)
            self.rf.fit(X, y)

            self.is_trained = True
        except Exception as e:
            print(f"ML Model training notice: {e}")
            self.is_trained = False

    def predict_archetype(self, user_data: Dict[str, Any]) -> Tuple[str, Dict[str, float]]:
        if not self.is_trained or self.kmeans is None:
            stress = user_data.get("stress_level", 5)
            act = user_data.get("physical_activity_min", 30)
            sleep = user_data.get("sleep_duration_hrs", 7.0)

            if stress >= 7 and act < 30:
                archetype = self.archetype_labels[1]
            elif sleep < 6.5:
                archetype = self.archetype_labels[2]
            elif act >= 40 and sleep >= 7.0 and stress <= 4:
                archetype = self.archetype_labels[0]
            else:
                archetype = self.archetype_labels[3]

            default_imp = {
                "Sleep Duration": 0.25,
                "Stress Level": 0.22,
                "Physical Activity": 0.18,
                "Screen Time": 0.14,
                "Water Intake": 0.11,
                "Outdoor Sunlight": 0.10
            }
            return archetype, default_imp

        x_df = pd.DataFrame([[
            float(user_data.get("sleep_duration_hrs", 7.0)),
            float(user_data.get("physical_activity_min", 30.0)),
            float(user_data.get("water_intake_liters", 2.2)),
            float(user_data.get("screen_time_hrs", 6.0)),
            float(user_data.get("outdoor_time_min", 30.0)),
            float(user_data.get("stress_level", 5)),
            float(user_data.get("bmi", 22.5))
        ]], columns=self.feature_cols)

        x_scaled = self.scaler.transform(x_df)
        cluster_id = int(self.kmeans.predict(x_scaled)[0])
        archetype_name = self.archetype_labels.get(cluster_id, "Diverse Lifestyle Profile")

        importances = dict(zip(
            ["Sleep Duration", "Physical Activity", "Water Intake", "Screen Time", "Outdoor Sunlight", "Stress Level", "BMI"],
            [round(float(v), 3) for v in self.rf.feature_importances_]
        ))
        sorted_imp = dict(sorted(importances.items(), key=lambda item: item[1], reverse=True))

        return archetype_name, sorted_imp
