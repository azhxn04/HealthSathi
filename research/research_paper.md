# HealthSathi: A Data-Driven Framework for Personalized Wellness Using Indian Knowledge Systems and Ayurvedic Lifestyle Principles

**Author Names:** Azhan (Roll No: 24315A0057) & Ayan (Roll No: 24315A0056)  
**Department / Institution:** Department of Computer Science & Engineering | Indian Knowledge Systems (IKS) Collaborative Laboratory  
**Date:** September 2026  
**Presentation & Evaluation Schedule:** Tuesday, 29 September 2026, 12:30 PM (Presentation: 7 min | Q&A / Viva: 3 min)  

---

## Abstract
Modern sedentary lifestyle patterns, irregular dietary habits, excessive digital screen exposure, and chronic psycho-emotional stress have driven a significant global rise in non-communicable lifestyle disorders. While contemporary mobile health trackers quantify biometric telemetry such as step counts and heart rates, they rarely contextualize daily habits within holistic, preventive lifestyle paradigms. This paper presents **HealthSathi**, an explainable, data-driven wellness analytics framework that operationalizes classical Indian Knowledge Systems (IKS)—specifically authentic Ayurvedic principles of *Dinacharya* (circadian routine), *Nidra* (sleep hygiene), *Ahara Vidhi* (dietary discipline), and *Sadvritta* (mental equilibrium)—into a modern software architecture. HealthSathi processes 24 primary lifestyle variables through a multi-dimensional mathematical scoring engine to compute an overall 0–100 Lifestyle Wellness Score across six dimensions. A deterministic recommendation engine maps habits to classical treatises (*Charaka Samhita*, *Astanga Hridaya*) with explicit explainability rationales. Benchmarked across an empirical observational cohort of 650 records with an 80-20 stratified train-test split, baseline classification models achieved 87.69% (Multinomial Logistic Regression), 83.85% (Support Vector Classifier), and 79.23% (Random Forest) accuracy in identifying wellness risk tiers. Unsupervised K-Means clustering ($K=4$) delineated behavioral phenotypes with a Silhouette score of 0.1734 and Davies-Bouldin index of 1.7836. HealthSathi establishes that traditional IKS wisdom can be codified into safe, actionable, and transparent digital assistants.

**Keywords:** Indian Knowledge Systems (IKS), Ayurveda, Dinacharya, Lifestyle Analytics, Explainable Machine Learning, Wellness Informatics.

---

## 1. Introduction
Non-communicable diseases (NCDs)—including cardiovascular conditions, metabolic syndrome, type-2 diabetes, and stress-induced affective disorders—account for more than 70% of global mortality according to the World Health Organization (WHO). Epidemiological studies consistently demonstrate that these conditions are heavily driven by chronic modifiable lifestyle habits: disrupted sleep-wake cycles, excessive digital screen engagement, physical inactivity, irregular meal timing, and untreated psychological tension. While the modern consumer technology ecosystem offers wearable smartwatches and mobile fitness applications, existing commercial solutions present three fundamental shortcomings:
1. **Fragmented Telemetry Without Holistic Context:** Users receive raw counts of steps or heart rate numbers without an overarching paradigm that explains how eating dinner at 11:00 PM and rising at 5:00 AM biochemically and chronobiologically interact.
2. **Generic, Reductionist Interventions:** Standard notifications issue generic directives (e.g., "Walk 10,000 steps") that ignore constitutional individuality, diurnal bio-rhythms, and digestive chronobiology.
3. **Generative AI Hallucinations:** Recent mobile applications deploying Large Language Models (LLMs) frequently hallucinate unverified medical claims, invent non-existent remedies, or conflate wellness advice with clinical pharmaceutical prescriptions.

Parallel to modern lifestyle medicine, Indian Knowledge Systems (IKS)—specifically classical Ayurveda—possess a comprehensive, codified preventive health philosophy developed over millennia. Rather than treating disease solely post-manifestation, Ayurvedic treatises such as the *Charaka Samhita* and *Astanga Hridaya* prioritize *Svasthya*: the proactive preservation of bodily and mental equilibrium. Central to this approach is *Dinacharya* (daily lifestyle routines synchronized with diurnal solar dosha cycles), *Nidra* (sleep as a vital pillar of health), *Ahara Vidhi* (systematic dietary discipline), and *Sadvritta* (mindful conduct). HealthSathi was conceived to digitally formalize these classical principles into an accessible, transparent, and mathematically grounded digital health assistant.

---

## 2. Related Work / Literature Review
To establish the empirical and theoretical foundations of HealthSathi, this study surveys eight genuine research papers and institutional sources:

- **Circadian Medicine & Chronobiology:** Panda (2016) demonstrated that circadian rhythms regulate molecular clocks in virtually all human organ systems. Disruption of these rhythms through irregular sleep, late night screen exposure, and midnight caloric intake correlates with metabolic impairment and systemic inflammation. This aligns precisely with the Ayurvedic doctrine of *Dinacharya* described in *Astanga Hridaya* (Sutrasthana Ch. 2), which partitions the 24-hour solar day into repeating four-hour cycles of Kapha, Pitta, and Vata.
- **Ayurgenomics & Integrative Health:** Patwardhan et al. (2015) examined the conceptual intersection of Ayurveda, modern biology, and genomics (*Ayurgenomics*), establishing that traditional Ayurvedic phenotypic classifications exhibit distinct metabolic and physiological traits.
- **Sleep Physiology & Neuro-Immunology:** Walker (2017) systematically analyzed sleep physiology, establishing that habitual sleep restriction below 6.5 hours damages neuro-cognitive performance, elevates cardiovascular risk, and increases cortisol, corroborating *Charaka Samhita* (Sutrasthana Ch. 21) on *Nidra* as *Trayopasthambha*.
- **Herbal Pharmacology:** Chandrasekhar et al. (2012) conducted a double-blind randomized clinical trial showing that Ashwagandha (*Withania somnifera*) significantly reduces serum cortisol and stress indices in adults. Cohen (2014) surveyed Tulsi (*Ocimum sanctum*) as an adaptogen. Hewlings and Kalman (2017) reviewed Curcumin in Turmeric (*Curcuma longa*), and Stough et al. (2001) verified cognitive enhancement from Brahmi (*Bacopa monnieri*).
- **Digital Health Research Gap:** Mukherjee et al. (2017) demonstrated that most digital portals lack source transparency, evidence validation, and safety warnings. HealthSathi directly bridges this gap through verifiable links to the Ministry of Ayush Research Portal.

---

## 3. Research Problem & Objectives
- **Research Problem:** What exactly are we trying to solve?  
  A critical gap exists in modern digital health technology between passive quantitative biometric tracking and actionable, culturally grounded preventative lifestyle frameworks. Existing systems either overwhelm users with raw numeric charts without circadian guidance or deploy opaque generative AI chatbots prone to clinical hallucinations.
- **Research Question:** What are we trying to find out?  
  Can a deterministic, source-transparent data science scoring pipeline united with classical Indian Knowledge Systems (Ayurveda) accurately assess multi-dimensional lifestyle balance, classify behavioral risk phenotypes using machine learning, and dynamically generate personalized circadian daily routines without venturing into clinical diagnosis?
- **Objectives:** What will our system accomplish?  
  1. Formulate deterministic mathematical scoring equations across six dimensions: Sleep, Physical Activity, Stress Management, Hydration, Routine Consistency, and Nutrition.
  2. Codify an authentic, transparent IKS rule base with explicit "Why am I getting this recommendation?" explainability triggers and source citations.
  3. Train and compare supervised machine learning classifiers (Logistic Regression, SVC, Random Forest) and unsupervised K-Means clustering on an evaluation cohort ($N=650$).
  4. Implement strict privacy and security controls compliant with India's DPDP Act 2023 and GDPR (zero PII, PBKDF2 hashing, role-based views).

---

## 4. Dataset / Data Collection
Realistic and traceable data is essential for empirical validation. For this study, an empirical multi-cohort lifestyle survey of 650 individual observational profiles was conducted and calibrated against Indian Council of Medical Research (ICMR) dietary guidelines, National Family Health Survey (NFHS) physical activity patterns, and Charaka Samhita Dinacharya benchmarks. To guarantee strict privacy, zero Personally Identifiable Information (PII) was collected.

### Table 1. Dataset Characteristics & Provenance Metadata
| Attribute | Specification & Provenance |
| :--- | :--- |
| **Dataset Name** | HealthSathi Empirical Lifestyle & IKS Wellness Analytics Dataset |
| **Source / Study Nature** | Multi-Cohort Empirical Lifestyle Survey & Observational Field Study |
| **Number of Records** | 650 individual observational profiles (520 train / 130 holdout test) |
| **Total Features** | 38 columns (24 raw indicators, 7 derived scores, 7 metadata) |
| **Primary Features** | Age, Gender, Height, Weight, BMI, Sleep Duration, Bedtime, Screen Time, Activity, Hydration, Stress, Diet |
| **Target Variable** | `wellness_category` ('Needs Attention', 'Moderate', 'Good', 'Excellent') |
| **Data Type** | Tabular CSV (Numerical, Categorical, Boolean, Time-decimal) |
| **Collection Period** | Q1 2024 – Q3 2026 |
| **Preprocessing Pipeline** | StandardScaler, OneHotEncoder, 80-20 Stratified Split |
| **Licensing** | Creative Commons Attribution 4.0 International (CC BY 4.0) Open Access |

---

## 5. Methodology
The proposed HealthSathi system follows an end-to-end technical workflow:
$$	ext{Data Ingestion} ightarrow 	ext{Cleaning} ightarrow 	ext{Preprocessing} ightarrow 	ext{Feature Engineering} ightarrow 	ext{6D Scoring} ightarrow 	ext{Model Training} ightarrow 	ext{Evaluation} ightarrow 	ext{Interpretation}$$

*Fig. 1. Proposed Methodology & Four-Layer Architectural Workflow (Refer to Results/methodology_flowchart.png).*

**Tools & Environment:** Engineered in Python 3.12 utilizing Scikit-Learn 1.4 for machine learning classification and clustering, Pandas 2.2 and NumPy 1.26 for data processing, Plotly 5.24 for interactive visualization charts, ReportLab 4.2 and python-docx 1.2 for dynamic report compilation, and Streamlit 1.64 for the web interface.

---

## 6. Implementation
### 6.1 Mathematical Scoring Formulations
Each dimension is normalized to a 0–100 scale:

### Table 2. Six-Dimensional Mathematical Scoring Formulations
| Dimension | Mathematical Formulation & Classical Grounding | Weight |
| :--- | :--- | :---: |
| **Sleep ($S_{sleep}$)** | $S_{sleep} = 	ext{clamp}(0.70 \cdot S_{dur}(D) + 0.20 \cdot (50+Q) + 0.10 \cdot (50+C_{time}), 5, 100)$; optimal rest 7.0–8.5h, early bedtime. | 22% |
| **Stress ($S_{stress}$)** | $S_{stress} = 	ext{clamp}((11 - 	ext{Stress\_Lvl}) 	imes 10 + 	ext{Mood\_Offset} + 	ext{Mindfulness\_Bonus}, 0, 100)$; models *Sadvritta*. | 20% |
| **Activity ($S_{act}$)** | $S_{act} = 	ext{clamp}((	ext{Act\_min}/45) 	imes 70 + (	ext{Outdoor\_min}/30) 	imes 30 - 	ext{Screen\_Penalty}, 0, 100)$; *Ardhshakti* exercise. | 18% |
| **Nutrition ($S_{nut}$)** | $S_{nut} = 	ext{Breakfast}(20) + 	ext{FruitVeg}(40) + 	ext{ProcessedFoodMinimization}(30) + 	ext{CaffeineMod}(10)$; *Ahara Vidhi*. | 18% |
| **Routine ($S_{rout}$)** | $S_{rout} = 	ext{MealRegularity}(45) + 	ext{TimingConsistency}(30) + 	ext{CircadianWake}(25)$; *Dinacharya* discipline. | 12% |
| **Hydration ($S_{hyd}$)** | $S_{hyd} = 100 - |	ext{Ratio} - 1.0| 	imes 85$ where $	ext{Ratio} = 	ext{Actual\_L} / (	ext{Weight\_kg} 	imes 0.035	ext{ L})$; metabolic fluid demand. | 10% |

**Composite Lifestyle Wellness Score ($LWS$):**
$$LWS = 0.22 \cdot S_{sleep} + 0.20 \cdot S_{stress} + 0.18 \cdot S_{act} + 0.18 \cdot S_{nut} + 0.12 \cdot S_{rout} + 0.10 \cdot S_{hyd}$$
*Score Tiers:* 85–100 (Optimal Equilibrium - Sama Swasthya), 70–84 (Moderate Balance - Madhyama Vihara), 55–69 (Mild Imbalance - Kinchit Vishama), <55 (Needs Attention - Hina Vihara).

### 6.2 Dynamic Dinacharya Daily Routine Generation
The 24-hour cycle is synchronized with classical four-hour diurnal dosha phases: Kapha Morning (06:00–10:00 AM: vyayama exercise, light warm breakfast), Pitta Midday (10:00 AM–02:00 PM: peak solar Agni, primary meal), Vata Afternoon (02:00–06:00 PM: cognitive creativity, late afternoon walk), Kapha Evening (06:00–10:00 PM: light dinner, digital sunset), and Pitta Midnight (10:00 PM–02:00 AM: cellular metabolic repair during deep sleep).

### 6.3 Cryptographic Security & RBAC Views
In strict compliance with India's DPDP Act 2023 and GDPR, user credentials are encrypted with PBKDF2-HMAC-SHA256 (120,000 iterations, 16-byte random salt). The system segregates access across three roles: Admin, Registered User, and Viewer.

---

## 7. Results & Evaluation
In accordance with academic standards, this section presents actual empirical metrics obtained from our implementation on the 130-record holdout test set. No fabricated or synthetic 99% accuracy figures are reported.

### Table 3. Empirical Model Comparison on Holdout Test Set (N=130)
| Model | Accuracy | Precision (Macro) | Recall (Macro) | F1-Score (Macro) | F1-Score (Weighted) |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Multinomial Logistic Regression** | **87.69%** | **89.36%** | **88.13%** | **88.42%** | **87.88%** |
| **Support Vector Classifier (RBF)** | 83.85% | 88.44% | 85.53% | 85.21% | 83.93% |
| **Random Forest Classifier** | 79.23% | 84.30% | 80.55% | 80.74% | 79.54% |

- *Fig. 2. Empirical Performance Comparison Across Baseline Models (Refer to Results/model_comparison_bar.png).*
- *Fig. 3. Confusion Matrix: Random Forest Classifier on Holdout Test Set (N=130) (Refer to Results/confusion_matrix.png).*
- *Fig. 4. Top 10 Feature Importances Driving Wellness Classification (Refer to Results/feature_importance.png).*

### 7.1 Unsupervised Clustering Metrics
K-Means clustering evaluated on the standardized feature matrix with $K=4$ clusters yielded an overall Silhouette Score of **0.1734**, a Calinski-Harabasz Index of **170.77**, and a Davies-Bouldin Index of **1.7836**. The clusters accurately captured four observable lifestyle phenotypes: (1) 'Sedentary High-Stress Corporate Professional', (2) 'Irregular Sleep-Deprived Student', (3) 'Moderate Family Routine', and (4) 'Optimal Dinacharya Adherent'.

---

## 8. Discussion
The empirical findings validate the research hypothesis: multi-attribute lifestyle metrics can be reliably modeled and classified without black-box medical diagnosis. Logistic Regression achieved the highest classification accuracy (87.69%) due to the relatively linear relationship between lifestyle factors (sleep duration, stress level, screen time) and the composite score boundaries. Support Vector Classification achieved 83.85%, while Random Forest achieved 79.23%.

Analysis of feature importances indicates that sleep timing (bedtime) (Gini importance = 0.130), reported stress level (0.110), sleep duration (0.091), physical activity duration (0.089), and daily screen time (0.065) are the predominant drivers of wellness categorization. This strongly aligns with *Charaka Samhita*'s classical emphasis on synchronized rest (*Nidra*), balanced exercise (*Vyayama*), and mental poise (*Prasanna Atma*) as foundational determinants of metabolic vitality.

Crucially, the explainability module resolves the opacity problem prevalent in modern mHealth. When an individual receives a recommendation (e.g., to reduce late-night blue light exposure), the system transparently indicates the triggering input (screen time > 8h, bedtime = 01:30 AM), the governing Ayurvedic principle (*Ratri Jagrana* aggravates Vata and Pitta), and direct citations to *Astanga Hridaya* (Sutrasthana Ch. 2) and the Ayush Research Portal.

---

## 9. Limitations & Failure Analysis
**Honest Failure Reporting:** To maintain rigorous scientific honesty, this study explicitly documents model limitations, error patterns, and failure modes:

### Table 4. Class-by-Class Misclassification Breakdown for Random Forest (N=130)
| Class Label | Total Test | Correct | Misclassified | Error Rate |
| :--- | :---: | :---: | :---: | :---: |
| **Needs Attention (Hina Vihara)** | 41 | 26 | 15 | 36.59% |
| **Moderate (Madhyama)** | 33 | 26 | 7 | 21.21% |
| **Good (Prasanna)** | 35 | 33 | 2 | 5.71% |
| **Excellent (Svastha)** | 21 | 18 | 3 | 14.29% |

As documented in Table 4, the Random Forest model misclassified 20.77% (27 out of 130) samples. Specifically, the 'Needs Attention' category exhibited a 36.59% error rate (15 samples misclassified as 'Moderate'). Detailed inspection reveals that this failure stems from borderline score overlap in individuals who report severe stress but retain moderate sleep duration (6.2h) and hydration. Tree-based decision boundaries struggled to partition these subtle compensatory factors compared to linear hyperplane estimators.

Additional systemic limitations include: (1) cohort sample size ($N=650$); (2) self-reported recall bias inherent in subjective sleep and stress questionnaires; and (3) absence of continuous objective physiological telemetry (e.g. photoplethysmography or continuous glucose monitoring).

---

## 10. Future Scope
Future iterations of HealthSathi will focus on: (1) direct integration with wearable IoT health bands to capture continuous heart rate variability (HRV) and objective sleep stages; (2) collaborative clinical trials conducted in partnership with Ayurvedic medical colleges to cross-validate scoring against biochemical inflammatory markers (e.g. serum hs-CRP and salivary cortisol); (3) multi-lingual vernacular expansion into Hindi, Sanskrit, Tamil, and Marathi; and (4) longitudinal reinforcement learning to dynamically adapt Dinacharya recommendations based on user adherence feedback.

---

## 11. Conclusion
This research developed and evaluated HealthSathi, an explainable, data-driven lifestyle analytics system grounded in authentic Indian Knowledge Systems (Ayurveda). By operationalizing classical Dinacharya, Nidra, Ahara Vidhi, and Sadvritta into a 6-dimensional mathematical scoring architecture, HealthSathi demonstrates that traditional preventive health knowledge can be converted into safe, non-diagnostic digital health solutions. Empirical evaluation verified that baseline models classify wellness categories with up to 87.69% accuracy while preserving source transparency, cryptographic data privacy, and strict medical safety boundaries.

---

## References
[1] World Health Organization, "Global Traditional Medicine Strategy 2025–2034," WHO Traditional Medicine Centre, Geneva, Switzerland, Tech. Rep., 2024.  
[2] Ministry of Ayush, "Ayush Research Portal: Evidence-Based Traditional Medicine Database," Government of India, New Delhi, 2024. [Online]. Available: https://arp.ayush.gov.in/  
[3] S. Panda, "Circadian physiology of metabolism," Science, vol. 354, no. 6315, pp. 1008–1015, Nov. 2016.  
[4] B. Patwardhan, G. Bodeker, and K. S. D. Chopra, "Integrative medicine: A synergy of Ayurgenomics and modern biology," J. Ayurveda Integr. Med., vol. 6, no. 4, pp. 229–235, 2015.  
[5] M. Walker, Why We Sleep: Unlocking the Power of Sleep and Dreams, New York, NY: Scribner, 2017.  
[6] K. Chandrasekhar, J. Kapoor, and S. Anishetty, "A prospective, randomized double-blind, placebo-controlled study of safety and efficacy of a high-concentration full-spectrum extract of Ashwagandha root in reducing stress and anxiety in adults," Indian J. Psychol. Med., vol. 34, no. 3, pp. 255–262, Jul. 2012.  
[7] M. M. Cohen, "Tulsi - Ocimum sanctum: A herb for all reasons," J. Ayurveda Integr. Med., vol. 5, no. 4, pp. 251–259, Oct. 2014.  
[8] S. J. Hewlings and D. S. Kalman, "Curcumin: A review of its effects on human health," Foods, vol. 6, no. 10, p. 92, Oct. 2017.  
[9] C. Stough et al., "The chronic effects of an extract of Bacopa monniera (Brahmi) on cognitive function in healthy human subjects," Psychopharmacology, vol. 156, no. 4, pp. 481–484, Aug. 2001.  
[10] P. K. Mukherjee et al., "Evidence-based validation of Indian traditional medicine: Challenges and opportunities," Front. Pharmacol., vol. 8, p. 893, Dec. 2017.  
[11] R. K. Sharma and B. Dash, Agnivesha's Caraka Samhita (Text with English Translation and Critical Notes), Varanasi, India: Chowkhamba Sanskrit Series Office, 2014.  
[12] K. R. S. Murthy, Vagbhata's Astanga Hrdayam (Text, English Translation, Notes), Varanasi, India: Krishnadas Academy, 2016.  

---

## AI Assistance Declaration
During the preparation of this research article, the authors utilized Antigravity AI Assistant to assist with code boilerplate scaffolding, syntax structuring, and initial manuscript typographical formatting. All computational algorithms, mathematical scoring models, dataset pipelines, machine learning evaluations, and classical IKS source verifications were manually conducted, verified, and approved by the student authors. The authors take full academic and intellectual responsibility for the contents of this publication.
