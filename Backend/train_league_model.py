# train_league_model.py
"""
Train the league winner model and save artifacts for the Streamlit app.
This script reproduces the pipeline you used (scaling, RandomForest,
CV probability predictions, threshold tuning) and then saves:
- rf_model.joblib
- scaler.joblib
- threshold.json
- feature_importance.csv
- model_metadata.json
"""

import json
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_predict
from sklearn.metrics import classification_report, precision_recall_curve, roc_curve, auc
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
import joblib
import warnings
warnings.filterwarnings("ignore")

DATA_PATH = "league_winner_data.csv"   
MODEL_OUT = "rf_model.joblib"
SCALER_OUT = "scaler.joblib"
THRESH_OUT = "threshold.json"
FI_OUT = "feature_importance.csv"
META_OUT = "model_metadata.json"
RANDOM_STATE = 42

df = pd.read_csv(DATA_PATH)
print("Loaded dataset:", df.shape)

# Drop wins/draws/losses as you requested
df_modified = df.drop(columns=['wins', 'draws', 'losses'], errors='ignore')

# Define features and target consistent with your notebook
exclude_from_features = [
    'season', 'team', 'target_champion', 'target_top_4',
    'target_top_6', 'target_relegated', 'target_league_position',
    'target_total_points'
]
feature_cols = [c for c in df_modified.columns if c not in exclude_from_features]
X = df_modified[feature_cols].copy()
y = df_modified['target_champion'].copy().astype(int)

print("Features used:", feature_cols)
print("Target distribution:", y.value_counts().to_dict())

# Scale features 
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

#  Model: RandomForest 
rf = RandomForestClassifier(
    n_estimators=150,
    max_depth=6,
    min_samples_split=10,
    min_samples_leaf=5,
    class_weight='balanced',
    random_state=RANDOM_STATE
)

# Cross-validated predicted probabilities (5-fold) 
print("Generating cross-validated probability estimates (5-fold)...")
y_proba_cv = cross_val_predict(rf, X_scaled, y, cv=5, method='predict_proba')[:, 1]

#  Tune threshold to maximize F1 score
thresholds = np.arange(0.1, 0.9, 0.05)
best_f1 = -1.0
best_threshold = 0.5
from sklearn.metrics import f1_score

for t in thresholds:
    preds = (y_proba_cv > t).astype(int)
    f1 = f1_score(y, preds)
    if f1 > best_f1:
        best_f1 = f1
        best_threshold = float(t)

print(f"Optimal threshold (by F1) found: {best_threshold} (F1={best_f1:.4f})")

#Fit final RF on full (scaled) data so we can get feature importances 
rf.fit(X_scaled, y)
print("RandomForest fit on full dataset.")

fpr, tpr, _ = roc_curve(y, y_proba_cv)
roc_auc = auc(fpr, tpr)
report = classification_report(y, (y_proba_cv > best_threshold).astype(int), output_dict=True)

metrics = {
    "roc_auc_cv": float(roc_auc),
    "accuracy_cv": float(report["accuracy"]),
    "precision_champion": float(report["1"]["precision"]),
    "recall_champion": float(report["1"]["recall"]),
    "f1_champion": float(report["1"]["f1-score"]),
    "optimal_threshold": best_threshold
}

print("Cross-validated ROC AUC:", roc_auc)
print("Cross-validated accuracy:", report["accuracy"])

# Feature importance 
fi = pd.DataFrame({
    "feature": feature_cols,
    "importance": rf.feature_importances_
}).sort_values("importance", ascending=False)

joblib.dump(rf, MODEL_OUT)
joblib.dump(scaler, SCALER_OUT)
fi.to_csv(FI_OUT, index=False)

metadata = {
    "feature_columns": feature_cols,
    "model_file": MODEL_OUT,
    "scaler_file": SCALER_OUT,
    "feature_importance_file": FI_OUT,
    "metrics": metrics
}
with open(META_OUT, "w") as f:
    json.dump(metadata, f, indent=2)

with open(THRESH_OUT, "w") as f:
    json.dump({"optimal_threshold": best_threshold}, f)

print("Artifacts saved:")
print(" -", MODEL_OUT)
print(" -", SCALER_OUT)
print(" -", THRESH_OUT)
print(" -", FI_OUT)
print(" -", META_OUT)
