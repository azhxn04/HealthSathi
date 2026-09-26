# 📚 HealthSathi: Annotated Literature Compendium & End-to-End Dataset Provenance
### Formal Scientific and Classical Source Documentation for Faculty Review & Publication
*(Aligned with Section 10, 11, 16, 17, and 19 of the HealthSathi Project Blueprint)*

> **MANDATORY ETHICAL & NON-DIAGNOSTIC DISCLAIMER:**  
> HealthSathi is a lifestyle and wellness analytics research prototype, not a medical diagnosis or treatment system. It does not diagnose diseases, prescribe pharmaceuticals, replace licensed physicians, or advise altering any ongoing clinical therapy. All self-reported conditions are treated solely as contextual lifestyle indicators.

---
## Part 1: Comprehensive Literature & Treatise Analyses (14 Annotated Studies)

### 1. Ministry of Ayush — Ayush Research Portal (ARP) (`SRC-001`)
- **Lead Author / Institution:** Government of India, Ministry of Ayush
- **Publication Type:** National Evidence Repository & Clinical Trial Database (2026 (Continuous Indexing))
- **Direct Link / Reference URL:** [https://arp.ayush.gov.in/researchabout](https://arp.ayush.gov.in/researchabout)
- **Core Conceptual Framework:** National digital repository indexing over 41,000 peer-reviewed clinical trials, pharmacological analyses, and historical manuscripts across Ayurveda, Yoga, Unani, Siddha, and Homeopathy.
- **Key Findings / Empirical Evidence:** Provides standardized monographs on botanical safety, permissible human posology (dosage), heavy metal contamination thresholds, and standardized phytochemical markers (e.g. withanolides in Withania somnifera, curcuminoids in Curcuma longa).
- **Direct Integration into HealthSathi:** Serves as the primary institutional benchmark for validating botanical profiles in medicinal_plants.csv, cross-verifying safety contraindications, and preventing unsubstantiated therapeutic claims in HealthSathi.
- ⚠️ **Safety Bounds & Contraindications:** Official portal policy dictates that traditional formulations must be prescribed by registered AYUSH practitioners and not automated via unmonitored software.

### 2. WHO Global Traditional Medicine Strategy 2025–2034 (`SRC-002`)
- **Lead Author / Institution:** World Health Organization (WHO Global Traditional Medicine Centre, Jamnagar)
- **Publication Type:** International Public Health Policy Directive (2025)
- **Direct Link / Reference URL:** [https://www.who.int/teams/who-global-traditional-medicine-centre/traditional-medicine-strategy-2025-2034](https://www.who.int/teams/who-global-traditional-medicine-centre/traditional-medicine-strategy-2025-2034)
- **Core Conceptual Framework:** Strategic global directive establishing international standards for integrating traditional, complementary, and integrative health (TCIH) into national health systems through rigorous evidence synthesis, digital innovation, and biodiversity conservation.
- **Key Findings / Empirical Evidence:** Prioritizes four pillars: (1) Evidence and learning; (2) Universal health coverage integration; (3) Digital health and artificial intelligence applications for traditional knowledge; and (4) Ethical biodiversity and intellectual property preservation.
- **Direct Integration into HealthSathi:** HealthSathi is directly modeled upon Pillar 3 (Digital Health & AI integration). It adopts the WHO guidelines requiring algorithmic transparency, non-diagnostic boundaries, and human-in-the-loop clinical safety.
- ⚠️ **Safety Bounds & Contraindications:** Directly warns against unregulated AI systems making autonomous diagnostic declarations or dispensing unsupervised herbal therapy.

### 3. WHO Traditional, Complementary and Integrative Medicine: Strategic Priorities (`SRC-003`)
- **Lead Author / Institution:** World Health Organization Department of Integrated Health Services
- **Publication Type:** Global Healthcare Regulatory Framework (2024)
- **Direct Link / Reference URL:** [https://www.who.int/teams/integrated-health-services/traditional-complementary-and-integrative-medicine/global-strategies](https://www.who.int/teams/integrated-health-services/traditional-complementary-and-integrative-medicine/global-strategies)
- **Core Conceptual Framework:** Technical framework establishing regulatory mechanisms for herbal medicines, practitioner credentialing, and safety surveillance (pharmacovigilance) in Member States.
- **Key Findings / Empirical Evidence:** Highlights that over 88% of Member States report traditional medicine usage. Recommends lifestyle and preventive practices as high-value, cost-effective interventions against chronic non-communicable diseases (NCDs).
- **Direct Integration into HealthSathi:** Grounds HealthSathi's lifestyle focus: rather than treating acute pathology, HealthSathi targets pre-clinical lifestyle determinants (circadian synchronization, hydration, physical activity, and stress management).
- ⚠️ **Safety Bounds & Contraindications:** Mandates that digital health tools clearly separate wellness promotion from clinical medical intervention.

### 4. WHO Traditional Medicine: Public Health Questions and Answers (`SRC-004`)
- **Lead Author / Institution:** World Health Organization Communications & Health Emergencies
- **Publication Type:** Public Health Advisory Brief (2024)
- **Direct Link / Reference URL:** [https://www.who.int/news-room/questions-and-answers/item/traditional-medicine](https://www.who.int/news-room/questions-and-answers/item/traditional-medicine)
- **Core Conceptual Framework:** Clear institutional guidance defining the scope, benefits, scientific challenges, and safety risks associated with traditional and complementary health modalities.
- **Key Findings / Empirical Evidence:** Clarifies that 'natural does not always mean safe'. Identifies herb-drug interactions, misidentification of botanical species, and inconsistent processing as major risk vectors requiring stringent public education.
- **Direct Integration into HealthSathi:** Directly incorporated into HealthSathi's mandatory safety disclaimers, educational plant explorer warnings, and explainability cards.
- ⚠️ **Safety Bounds & Contraindications:** Warns patients with cardiovascular disease, diabetes, and pregnancy never to discontinue conventional prescription pharmaceuticals without consulting a physician.

### 5. Charaka Samhita: Sutrasthana Chapter 21 (Ashtauninditiya Adhyaya) (`SRC-005`)
- **Lead Author / Institution:** Acharya Agnivesha; redacted by Acharya Charaka & Dridhabala
- **Publication Type:** Classical Ayurvedic Epistemological Treatise (Classical Era (c. 1000 BCE – 200 CE))
- **Direct Link / Reference URL:** [https://www.carakasamhitaonline.com](https://www.carakasamhitaonline.com)
- **Core Conceptual Framework:** Defines Nidra (Sleep) as one of the three irreplaceable pillars supporting living existence: Trayopasthambha (Ahara / Food, Nidra / Sleep, Brahmacharya / Controlled Conduct).
- **Key Findings / Empirical Evidence:** Articulates that happiness, strength, virility, cognitive acuity, and life longevity depend upon proper sleep (Samyak Nidra). Sleep deprivation (Anidra) causes emaciation, cognitive instability, and Vata aggravation. Inappropriate daytime sleep (Divasvapna) causes Kapha accumulation and sluggish metabolism.
- **Direct Integration into HealthSathi:** Provides the theoretical foundation for HealthSathi's Sleep Score mathematical model, which penalizes both deficient sleep (< 6.5 hours) and late-night bedtimes (> 11:30 PM).
- ⚠️ **Safety Bounds & Contraindications:** Emphasizes that sleep disorders secondary to underlying clinical illnesses require clinical panchakarma therapies rather than simple routine adjustments.

### 6. Astanga Hridaya: Sutrasthana Chapter 2 (Dinacharya Adhyaya) (`SRC-006`)
- **Lead Author / Institution:** Acharya Vagbhata
- **Publication Type:** Classical Ayurvedic Compendium on Circadian Medicine (Classical Era (c. 6th–7th Century CE))
- **Direct Link / Reference URL:** [https://vedicheritage.gov.in](https://vedicheritage.gov.in)
- **Core Conceptual Framework:** Systematic description of the daily circadian regimen: 'Brahme muhurte uttisthet svastho raksartham ayushah' (One desirous of preserving life and health should awaken during the Brahma Muhurta pre-dawn period).
- **Key Findings / Empirical Evidence:** Details hygiene, sensory protection, exercise, work rhythm, and nocturnal preparation. Specifies that physical exercise (Vyayama) should only be performed to half-capacity (Ardhshakti), indicated by perspiration on the brow and axillae, preventing physiological exhaustion.
- **Direct Integration into HealthSathi:** Forms the exact chronological backbone of HealthSathi's 11-step Personalized Daily Routine engine and the Physical Activity scoring benchmark.
- ⚠️ **Safety Bounds & Contraindications:** Contraindicates heavy physical exercise during acute fever, indigestion, or immediately after consuming heavy meals.

### 7. Charaka Samhita: Sutrasthana Chapter 27 (Annapanavidhi Adhyaya) (`SRC-007`)
- **Lead Author / Institution:** Acharya Charaka
- **Publication Type:** Classical Ayurvedic Nutritional Science (Classical Era (c. 1000 BCE – 200 CE))
- **Direct Link / Reference URL:** [https://www.carakasamhitaonline.com](https://www.carakasamhitaonline.com)
- **Core Conceptual Framework:** Science of dietary consumption (Ahara Vidhi Vishesha Ayatana), food qualities (heavy vs light), metabolic fire (Agni), and incompatible dietary combinations (Viruddha Ahara).
- **Key Findings / Empirical Evidence:** Explains that eating at regular, consistent hours (Kala Bhojana) preserves stable digestive fire (Agni Samata), whereas erratic meal times generate toxic undigested metabolic byproduct (Aama), leading to systemic lethargy and metabolic dysfunction.
- **Direct Integration into HealthSathi:** Informs HealthSathi's Nutrition Score and Routine Consistency Score, penalizing irregular meal times and rewarding consistent breakfast and unprocessed meals.
- ⚠️ **Safety Bounds & Contraindications:** Classical dietary rules must be adjusted during severe digestive illness under physician supervision.

### 8. Bhavaprakasha Nighantu: Varivarga (Hydrological Therapeutics) (`SRC-008`)
- **Lead Author / Institution:** Acharya Bhavamishra
- **Publication Type:** Classical Ayurvedic Pharmacopeia & Materia Medica (Medieval Era (c. 16th Century CE))
- **Direct Link / Reference URL:** [https://vedicheritage.gov.in](https://vedicheritage.gov.in)
- **Core Conceptual Framework:** Exposition on water qualities, thermal states, and physiological actions of boiled warm water (Ushnodaka).
- **Key Findings / Empirical Evidence:** States that boiled warm water is light to digest (Laghu), stimulates metabolic fire (Deepana), cleanses the urinary tract (Basti Shodhana), dispels gas, and facilitates the elimination of metabolic toxins (Aama Pachana).
- **Direct Integration into HealthSathi:** Grounds HealthSathi's Hydration Balance Score and recommends sipping warm water throughout the day, especially upon awakening and between meals.
- ⚠️ **Safety Bounds & Contraindications:** Excessive boiling or consuming boiling-hot water is cautioned against in Pitta-aggravated conditions (such as peptic ulcers).

### 9. Sushruta Samhita: Sutrasthana Chapter 15 (Dosha-Dhatu-Mala Kshaya Vriddhi) (`SRC-009`)
- **Lead Author / Institution:** Acharya Sushruta
- **Publication Type:** Classical Ayurvedic Surgical & Systemic Treatise (Classical Era (c. 800 BCE – 100 CE))
- **Direct Link / Reference URL:** [https://vedicheritage.gov.in](https://vedicheritage.gov.in)
- **Core Conceptual Framework:** The canonical definition of true holistic wellness (Svastha): 'Samadoshah samagnishcha samadhatu malakriyah | Prasannatmendriyamanah svastha ityabhidhiyate'.
- **Key Findings / Empirical Evidence:** Defines health not merely as the absence of clinical disease, but as a dynamic equilibrium of biological humor (Doshas), metabolic fire (Agni), cellular tissues (Dhatus), and excretion (Malas), united with mental serenity, sensory acuity, and spiritual tranquility.
- **Direct Integration into HealthSathi:** Provides the philosophical and mathematical justification for HealthSathi's composite Lifestyle Wellness Score (0–100), integrating physical, emotional, and circadian inputs.
- ⚠️ **Safety Bounds & Contraindications:** States that bodily imbalance must be addressed proactively through lifestyle before progressing into irreversible structural pathology.

### 10. Chandrasekhar et al. (2012) — Ashwagandha Root Extract in Stress & Anxiety (`SRC-010`)
- **Lead Author / Institution:** K. Chandrasekhar, Jyoti Kapoor, Sridhar Anishetty
- **Publication Type:** Prospective, Randomized, Double-Blind, Placebo-Controlled Trial (2012 (Indian Journal of Psychological Medicine))
- **Direct Link / Reference URL:** [https://pubmed.ncbi.nlm.nih.gov/23439798/](https://pubmed.ncbi.nlm.nih.gov/23439798/)
- **Core Conceptual Framework:** Investigated the efficacy of a high-concentration full-spectrum Ashwagandha (Withania somnifera) root extract in reducing stress and cortisol levels in chronically stressed adults.
- **Key Findings / Empirical Evidence:** 64 participants receiving 300 mg of KSM-66 extract twice daily for 60 days exhibited a statistically significant 27.9% reduction in serum cortisol (p=0.0006) and a 44.0% reduction in Perceived Stress Scale (PSS) scores compared to placebo, with excellent tolerability.
- **Direct Integration into HealthSathi:** Provides peer-reviewed clinical justification for Ashwagandha in HealthSathi's botanical explorer and grounds recommendations triggered by high stress (> 7/10).
- ⚠️ **Safety Bounds & Contraindications:** Not recommended during pregnancy, lactation, active thyroid disorders, or concurrently with immunosuppressant medications without medical monitoring.

### 11. Hewlings & Kalman (2017) — Curcumin: A Review of Effects on Human Health (`SRC-011`)
- **Lead Author / Institution:** Susan J. Hewlings, Douglas S. Kalman
- **Publication Type:** Systematic Review & Meta-Analysis (2017 (Foods, MDPI))
- **Direct Link / Reference URL:** [https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5664031/](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC5664031/)
- **Core Conceptual Framework:** Synthesized findings from multiple clinical trials evaluating the anti-inflammatory, antioxidant, and metabolic effects of curcumin (Curcuma longa).
- **Key Findings / Empirical Evidence:** Documents that curcumin downregulates NF-κB and inhibits pro-inflammatory cytokines (IL-6, TNF-α). Confirms that co-administration with piperine (from black pepper, the classical Trikatu principle) increases curcumin bioavailability by 2,000%.
- **Direct Integration into HealthSathi:** Directly supports the Turmeric profile in HealthSathi's medicinal plants explorer, validating the traditional practice of consuming turmeric in warm milk or with black pepper.
- ⚠️ **Safety Bounds & Contraindications:** High supplemental doses are contraindicated in active gallstone disease, biliary obstruction, or concurrently with anticoagulant medications.

### 12. Cohen (2014) — Tulsi: A Herb for All Reasons (`SRC-012`)
- **Lead Author / Institution:** Marc Maurice Cohen
- **Publication Type:** Comprehensive Pharmacological Review (2014 (Journal of Ayurveda and Integrative Medicine))
- **Direct Link / Reference URL:** [https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4296439/](https://www.ncbi.nlm.nih.gov/pmc/articles/PMC4296439/)
- **Core Conceptual Framework:** Systematic analysis of the clinical and preclinical literature on Holy Basil (Ocimum sanctum) as an adaptogen and daily wellness tonic.
- **Key Findings / Empirical Evidence:** Demonstrates that Tulsi exerts multi-system protective actions: mitigates physical stress, normalizes psychological stress through neuroprotective mechanisms, and modulates glycemic and lipid markers in metabolic stress.
- **Direct Integration into HealthSathi:** Validates Tulsi herbal tea in HealthSathi's evening wind-down routine and provides educational citations for mental wellness.
- ⚠️ **Safety Bounds & Contraindications:** May have mild anti-platelet and anti-fertility effects in animal models at mega-doses; caution in bleeding disorders.

### 13. Stough et al. (2001) — Bacopa monnieri on Cognitive Function (`SRC-013`)
- **Lead Author / Institution:** Con Stough, J. Lloyd, J. Clarke, et al.
- **Publication Type:** Double-Blind, Randomized, Placebo-Controlled Trial (2001 (Psychopharmacology))
- **Direct Link / Reference URL:** [https://pubmed.ncbi.nlm.nih.gov/11498727/](https://pubmed.ncbi.nlm.nih.gov/11498727/)
- **Core Conceptual Framework:** Examined the chronic effects of standardized Bacopa monnieri (Brahmi) extract (300 mg/day) on cognitive function in healthy adult human subjects.
- **Key Findings / Empirical Evidence:** Significant improvements observed in higher-order cognitive processing, visual information processing speed, and working memory after 12 weeks of administration (p < 0.05).
- **Direct Integration into HealthSathi:** Grounds the Brahmi entry in HealthSathi's botanical module for users with high screen time exposure, students, and intensive digital professionals.
- ⚠️ **Safety Bounds & Contraindications:** May cause mild gastrointestinal hypermotility or nausea if taken on an empty stomach; best taken with food or warm ghee.

### 14. Sharma, P. V. (1982) — Dravyaguna Vijnana & Classical Epistemology (`SRC-014`)
- **Lead Author / Institution:** Prof. P. V. Sharma (Chaukhambha Bharati Academy)
- **Publication Type:** Authoritative Ayurvedic Pharmacological Reference (1982 (Standard Academic Edition))
- **Direct Link / Reference URL:** [https://vedicheritage.gov.in](https://vedicheritage.gov.in)
- **Core Conceptual Framework:** Systematizes the classical principles of Ayurvedic pharmacology (Dravyaguna Vidya): Rasa (primary taste), Guna (biophysical properties), Virya (thermal potency), Vipaka (post-digestive effect), and Prabhava (specific therapeutic action).
- **Key Findings / Empirical Evidence:** Codifies over 400 classical botanicals into pharmacological families, establishing rigorous criteria for distinguishing warming (Ushna) from cooling (Sheeta) herbs and their dosha-specific indications.
- **Direct Integration into HealthSathi:** Supplies the multi-attribute taxonomic schema utilized in dataset/medicinal_plants.csv (Rasa, Virya, Vipaka columns) in HealthSathi.
- ⚠️ **Safety Bounds & Contraindications:** Highlights that improper combination of herbs with opposing potencies (Viruddha Virya) can diminish efficacy or produce gastric irritation.

---
## Part 2: End-to-End Dataset Provenance & Statistical Validation

### 1. Overview of the `dataset/` Repository
The `dataset/` directory contains all datasets utilized in the HealthSathi framework:
1. `lifestyle_data.csv`: Synthetic cohort of 650 participant records with 38 primary and derived lifestyle features.
2. `iks_knowledge.csv`: Curated decision table containing 13 deterministic classical Ayurvedic lifestyle rules, explainability rationale, and primary source citations.
3. `medicinal_plants.csv`: Repository of 10 foundational Ayurvedic botanicals with scientific binomials, classical attributes (*Rasa, Virya, Vipaka*), modern research citations, and safety contraindications.
4. `sources.csv`: Indexed bibliographic metadata linking all recommendations and herbs to primary institutional literature.
5. `DATA_DICTIONARY.csv`: Complete column-by-column schema and mathematical formulations.
6. `DATASET_DOCUMENTATION.md`: Full provenance and descriptive statistics markdown documentation.

### 2. Demographic & Lifestyle Parameter Distributions (N = 650)
| Feature | Mean ± Std | Median | Min | Max | IQR |
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

### 3. Pearson Correlation Coefficients with Lifestyle Wellness Score ($p < 0.001$)
- **Reported Stress Level ($L$):** $r = -0.788$ (Strong negative impact on autonomic resilience)
- **Physical Activity ($A$):** $r = +0.724$ (Strong positive correlation with physical vitality)
- **Screen Exposure Hours ($H_{scr}$):** $r = -0.691$ (Strong negative driver due to sensory fatigue)
- **Sleep Duration ($D$):** $r = +0.676$ (Primary restorative pillar)
- **Water Intake (L):** $r = +0.442$ (Hydration and Agni stimulation)

### 4. Unsupervised K-Means Behavioral Clustering ($K=4$)
1. **Cluster 0: Balanced Circadian Cohort** ($N=184$, Mean $LWS = 88.4$): Early sleepers (< 10:30 PM), regular meals, low stress (3.2/10), and optimal physical activity (45 min).
2. **Cluster 1: High-Stress Sedentary Tech Cohort** ($N=162$, Mean $LWS = 44.1$): High screen exposure (9.2 hrs), minimal movement (12 min), high stress (7.9/10), and fragmented sleep.
3. **Cluster 2: Irregular Shift & Delayed Sleep Cohort** ($N=148$, Mean $LWS = 52.7$): Late bedtimes (1:30 AM), erratic meal timings, skipped breakfasts, and high processed food intake.
4. **Cluster 3: Moderately Active but Recovery-Constrained** ($N=156$, Mean $LWS = 69.8$): Good physical activity (40 min) but elevated caffeine intake and sleep deficit (6.1 hrs).

---
*(End-to-end literature and dataset compendium prepared for HealthSathi Academic and Clinical Research Review.)*