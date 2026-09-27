"""
HealthSathi - Real Machine Learning Benchmark & Empirical Results Generator
Generates actual, un-fabricated ML benchmarks, confusion matrices, and metrics
conforming to the IKS x Data Science Mini Project Research Article Guidelines.
"""

import os
import json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.cluster import KMeans
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    confusion_matrix, classification_report, silhouette_score,
    calinski_harabasz_score, davies_bouldin_score
)

def run_benchmarks():
    os.makedirs("results", exist_ok=True)
    df = pd.read_csv("data/lifestyle_data.csv")
    print(f"Loaded dataset: {df.shape[0]} rows, {df.shape[1]} columns.")

    # 1. Feature selection (Raw lifestyle inputs only, strictly avoiding derived scores to prevent leakage)
    numerical_features = [
        "age", "height_cm", "weight_kg", "bmi", "sleep_duration_hrs",
        "sleep_time_dec", "wake_up_time_dec", "work_study_hrs", "screen_time_hrs",
        "physical_activity_min", "water_intake_liters", "outdoor_time_min", "stress_level"
    ]
    categorical_features = [
        "gender", "occupation", "sleep_quality", "meal_regularity", "mood",
        "relaxation_activity", "breakfast_regular", "fruit_veg_intake",
        "processed_food_freq", "caffeine_freq", "meal_timing_consistency"
    ]

    target_col = "wellness_category"
    X = df[numerical_features + categorical_features].copy()
    y = df[target_col].copy()

    # Encode boolean columns if necessary
    for col in ["relaxation_activity", "breakfast_regular"]:
        X[col] = X[col].astype(str)

    # Class ordering
    classes = [
        "Needs Attention (Hina Vihara)",
        "Moderate (Madhyama)",
        "Good (Prasanna)",
        "Excellent (Svastha)"
    ]

    # Preprocessor
    preprocessor = ColumnTransformer(
        transformers=[
            ("num", StandardScaler(), numerical_features),
            ("cat", OneHotEncoder(drop="first", handle_unknown="ignore"), categorical_features)
        ]
    )

    # 80-20 Train-Test split stratified
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, random_state=42, stratify=y
    )

    models = {
        "Multinomial Logistic Regression": LogisticRegression(max_iter=1000, random_state=42),
        "Support Vector Classifier (RBF)": SVC(probability=True, random_state=42),
        "Random Forest Classifier": RandomForestClassifier(n_estimators=100, max_depth=8, random_state=42)
    }

    metrics_list = []
    trained_pipelines = {}

    for name, clf in models.items():
        pipe = Pipeline(steps=[
            ("preprocessor", preprocessor),
            ("classifier", clf)
        ])
        pipe.fit(X_train, y_train)
        trained_pipelines[name] = pipe

        y_pred = pipe.predict(X_test)

        acc = accuracy_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred, average="macro", zero_division=0)
        rec = recall_score(y_test, y_pred, average="macro", zero_division=0)
        f1 = f1_score(y_test, y_pred, average="macro", zero_division=0)
        f1_wt = f1_score(y_test, y_pred, average="weighted", zero_division=0)

        metrics_list.append({
            "Model": name,
            "Accuracy": round(float(acc), 4),
            "Precision (Macro)": round(float(prec), 4),
            "Recall (Macro)": round(float(rec), 4),
            "F1-Score (Macro)": round(float(f1), 4),
            "F1-Score (Weighted)": round(float(f1_wt), 4)
        })

    metrics_df = pd.DataFrame(metrics_list)
    metrics_df.to_csv("results/model_evaluation_metrics.csv", index=False)
    print("Model Evaluation Metrics:")
    print(metrics_df.to_string(index=False))

    # Confusion Matrix for Best Model (Random Forest)
    best_pipe = trained_pipelines["Random Forest Classifier"]
    y_test_pred = best_pipe.predict(X_test)
    cm = confusion_matrix(y_test, y_test_pred, labels=classes)

    plt.figure(figsize=(8, 6))
    sns.heatmap(cm, annot=True, fmt="d", cmap="Blues", xticklabels=classes, yticklabels=classes)
    plt.title("Fig. 2. Confusion Matrix: Random Forest Classifier on Holdout Test Set (N=130)", fontsize=11, fontweight="bold", pad=12)
    plt.xlabel("Predicted Class", fontsize=10)
    plt.ylabel("True Actual Class", fontsize=10)
    plt.xticks(rotation=20, ha="right", fontsize=8.5)
    plt.yticks(rotation=0, fontsize=8.5)
    plt.tight_layout()
    plt.savefig("results/confusion_matrix.png", dpi=300)
    plt.close()

    # Classification report breakdown
    clf_rep = classification_report(y_test, y_test_pred, labels=classes, output_dict=True, zero_division=0)
    with open("results/classification_report.json", "w") as f:
        json.dump(clf_rep, f, indent=2)

    # Feature Importance Extraction from Random Forest
    rf_clf = best_pipe.named_steps["classifier"]
    onehot_encoder = best_pipe.named_steps["preprocessor"].named_transformers_["cat"]
    cat_names = list(onehot_encoder.get_feature_names_out(categorical_features))
    feature_names = numerical_features + cat_names
    importances = rf_clf.feature_importances_

    feat_df = pd.DataFrame({"Feature": feature_names, "Importance": importances})
    feat_df = feat_df.sort_values(by="Importance", ascending=False).reset_index(drop=True)
    feat_df.to_csv("results/feature_importances.csv", index=False)

    plt.figure(figsize=(9, 5))
    top_feats = feat_df.head(10)
    sns.barplot(data=top_feats, x="Importance", y="Feature", palette="viridis")
    plt.title("Fig. 3. Top 10 Feature Importances Driving Wellness Classification", fontsize=11, fontweight="bold")
    plt.xlabel("Mean Impurity Reduction (Gini Importance)", fontsize=10)
    plt.ylabel("Feature", fontsize=10)
    plt.tight_layout()
    plt.savefig("results/feature_importance.png", dpi=300)
    plt.close()

    # Model comparison bar plot
    plt.figure(figsize=(8, 4.5))
    metrics_melt = metrics_df.melt(id_vars="Model", value_vars=["Accuracy", "Precision (Macro)", "Recall (Macro)", "F1-Score (Macro)"], var_name="Metric", value_name="Score")
    sns.barplot(data=metrics_melt, x="Metric", y="Score", hue="Model", palette="Set2")
    plt.title("Fig. 4. Empirical Performance Comparison Across Baseline Models", fontsize=11, fontweight="bold")
    plt.ylim(0.70, 1.0)
    plt.legend(bbox_to_anchor=(1.02, 1), loc="upper left", borderaxespad=0.)
    plt.tight_layout()
    plt.savefig("results/model_comparison_bar.png", dpi=300)
    plt.close()

    # Unsupervised K-Means clustering evaluation
    X_num_scaled = StandardScaler().fit_transform(df[numerical_features])
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    cluster_labels = kmeans.fit_predict(X_num_scaled)

    sil_score = silhouette_score(X_num_scaled, cluster_labels)
    ch_score = calinski_harabasz_score(X_num_scaled, cluster_labels)
    db_score = davies_bouldin_score(X_num_scaled, cluster_labels)

    clustering_metrics = {
        "Optimal_Clusters_K": 4,
        "Silhouette_Score": round(float(sil_score), 4),
        "Calinski_Harabasz_Index": round(float(ch_score), 2),
        "Davies_Bouldin_Index": round(float(db_score), 4)
    }
    with open("results/clustering_metrics.json", "w") as f:
        json.dump(clustering_metrics, f, indent=2)

    print("\nK-Means Clustering Metrics (K=4):")
    print(json.dumps(clustering_metrics, indent=2))

    # Calculate exact misclassification statistics for Section 9 (Limitations & Failure Analysis)
    total_test = len(y_test)
    correct_test = accuracy_score(y_test, y_test_pred) * total_test
    misclassified = total_test - correct_test
    print(f"\nMisclassification Analysis: {int(misclassified)} out of {total_test} samples misclassified (Error Rate: {misclassified/total_test:.2%})")

    # Inspect class-by-class errors
    error_summary = []
    for i, c_true in enumerate(classes):
        total_class = np.sum(cm[i, :])
        correct_class = cm[i, i]
        err_class = total_class - correct_class
        error_summary.append({
            "Class": c_true,
            "Total_Samples": int(total_class),
            "Correct": int(correct_class),
            "Misclassified": int(err_class),
            "Class_Error_Rate": round(float(err_class / total_class), 4) if total_class > 0 else 0.0
        })
    with open("results/error_analysis.json", "w") as f:
        json.dump(error_summary, f, indent=2)
    print("Class Error Summary:")
    print(json.dumps(error_summary, indent=2))

    print("\n[SUCCESS] All real ML benchmarks and figures successfully created in results/!")

if __name__ == "__main__":
    run_benchmarks()
