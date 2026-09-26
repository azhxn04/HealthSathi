# HealthSathi: End-to-End Dataset Documentation & Provenance

## 1. Overview of the Dataset Repository
The `dataset/` directory contains all datasets used by the HealthSathi platform. In accordance with Section 11 and Section 19 of the project blueprint, the lifestyle dataset is explicitly identified as a synthetic evaluation cohort generated for prototype benchmarking.

### Files Included:
1. `lifestyle_data.csv`: Synthetic cohort of 650 participant records with 38 primary and derived lifestyle features.
2. `iks_knowledge.csv`: Curated decision table containing 13 deterministic classical Ayurvedic lifestyle rules, explainability rationale, and primary source citations.
3. `medicinal_plants.csv`: Repository of 10 foundational Ayurvedic botanicals with scientific binomials, classical attributes (*Rasa, Virya, Vipaka*), modern research citations, and safety contraindications.
4. `sources.csv`: Institutional literature citations with clickable links (Ministry of Ayush, WHO, PubMed, classical treatises).
5. `DATA_DICTIONARY.csv`: Complete column-by-column schema and mathematical formulations.

---

## 2. Cohort Demographics & Empirical Distributions (N = 650)

| Metric | Mean ± Std | Median | Min | Max | IQR |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Age (Years)** | 33.8 ± 10.4 | 32.0 | 19 | 60 | 25 – 41 |
| **Height (cm)** | 167.3 ± 8.8 | 167.2 | 140.1 | 188.4 | 161.2 – 173.8 |
| **Weight (kg)** | 67.4 ± 11.2 | 66.8 | 44.2 | 96.5 | 59.8 – 74.6 |
| **BMI ($kg/m^2$)** | 24.1 ± 3.4 | 23.8 | 16.8 | 34.8 | 21.6 – 26.3 |
| **Sleep Duration (Hours)** | 6.67 ± 1.13 | 6.80 | 3.70 | 9.00 | 5.80 – 7.50 |
| **Work/Study Hours** | 8.35 ± 1.62 | 8.10 | 4.20 | 13.80 | 7.20 – 9.40 |
| **Screen Time (Hours)** | 6.78 ± 2.05 | 6.60 | 2.50 | 12.80 | 5.20 – 8.20 |
| **Physical Activity (Min)** | 31.8 ± 18.6 | 32.0 | 0.0 | 85.0 | 16.0 – 46.0 |
| **Water Intake (Liters)** | 2.21 ± 0.58 | 2.20 | 0.80 | 3.80 | 1.80 – 2.60 |
| **Outdoor Sunlight (Min)** | 27.8 ± 15.2 | 26.0 | 0.0 | 75.0 | 15.0 – 38.0 |
| **Reported Stress (1–10)** | 5.62 ± 2.18 | 5.0 | 1 | 10 | 4 – 7 |
| **Lifestyle Wellness Score** | **68.15 ± 16.49** | **68.20** | **34.20** | **95.30** | **54.40 – 84.20** |

---

## 3. Correlation Matrix with Overall Lifestyle Wellness Score
- **Stress Level ($L$):** $r = -0.788$ ($p < 0.001$)
- **Physical Activity ($A$):** $r = 0.724$ ($p < 0.001$)
- **Screen Time Exposure ($H_{scr}$):** $r = -0.691$ ($p < 0.001$)
- **Sleep Duration ($D$):** $r = 0.676$ ($p < 0.001$)
- **Water Intake:** $r = 0.442$ ($p < 0.001$)

---

## 4. Machine Learning Behavioral Archetypes
Unsupervised K-Means clustering ($K=4$) delineates four distinct lifestyle cohorts:
1. **Cluster 0: Balanced Circadian Cohort** ($LWS pprox 88.4$) — Characterized by early awakening, optimal sleep ($7.6	ext{h}$), and consistent meals.
2. **Cluster 1: High-Stress Sedentary Tech Cohort** ($LWS pprox 44.1$) — Characterized by high screen time ($9.2	ext{h}$), low movement ($12	ext{m}$), and high stress ($7.9/10$).
3. **Cluster 2: Irregular Shift & Late Sleep Cohort** ($LWS pprox 52.7$) — Characterized by bedtimes after 1:00 AM and irregular meal windows.
4. **Cluster 3: Moderately Active but Recovery-Constrained** ($LWS pprox 69.8$) — Characterized by adequate movement but sleep debt and high caffeine use.

---

## 5. Ethical Guidelines & Data Privacy
- **Zero PII Collection:** The system does not store names, phone numbers, email addresses, or physical locations.
- **Voluntary Demonstration Usage:** Any future human sampling must adhere to institutional ethics clearance and voluntary consent.
- **Explicit Synthetic Labeling:** Synthetic files carry internal metadata headers identifying simulated provenance.
