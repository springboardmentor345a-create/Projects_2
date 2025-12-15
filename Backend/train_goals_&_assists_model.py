"""
Train XGBoost pipelines for Goals and Assists (if present) and save:
- pipeline files: xgb_goal_pipeline.pkl / xgb_assist_pipeline.pkl
- metadata files: metadata_goals.json / metadata_assists.json (feature list, types, categories)
This script uses the same preprocessing approach as your original script (OneHotEncoder for categorical).
"""

import json
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import joblib
from scipy.stats import randint, uniform

from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split, RandomizedSearchCV

RANDOM_STATE = 42
TEST_SIZE = 0.20
N_ITER = 30
CV = 3

INPUT_FILE = "Goals & Assist .xlsx"   

try:
    from xgboost import XGBRegressor
    xgb_available = True
except Exception:
    xgb_available = False
    print("xgboost not installed. Install via `pip install xgboost` then re-run.")

def clean_column_names(df):
    df = df.copy()
    df.columns = (df.columns
                  .str.replace(r"[^A-Za-z0-9_]", "", regex=True)
                  .str.replace(" ", "_"))
    return df

def load_data(path):
    df = pd.read_excel(path)
    df = clean_column_names(df)
    return df

def handle_missing(df):
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    cat_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
    if numeric_cols:
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].median())
    for c in cat_cols:
        if df[c].isnull().any():
            df[c] = df[c].fillna(df[c].mode().iloc[0])
    return df

def build_preprocessor(categorical_cols):
    # OneHotEncoder with drop="first" and sparse_output=False for compatibility
    ohe = OneHotEncoder(drop="first", sparse_output=False, handle_unknown="ignore")
    preproc = ColumnTransformer(transformers=[("ohe", ohe, categorical_cols)],
                                remainder="passthrough",
                                verbose_feature_names_out=False)
    return preproc

def train_xgb_pipeline(X_train, y_train):
    base = XGBRegressor(objective="reg:squarederror",
                        random_state=RANDOM_STATE,
                        verbosity=0,
                        n_jobs=-1)
    param_dist = {
        "model__n_estimators": randint(200, 900),
        "model__learning_rate": uniform(0.01, 0.3),
        "model__max_depth": randint(3, 12),
        "model__subsample": uniform(0.5, 0.5),
        "model__colsample_bytree": uniform(0.5, 0.5)
    }
    pipe = Pipeline([("preprocessor", "passthrough"), ("model", base)])
    search = RandomizedSearchCV(pipe, param_distributions=param_dist, n_iter=N_ITER, cv=CV,
                                scoring="r2", n_jobs=-1, random_state=RANDOM_STATE, verbose=1)
    search.fit(X_train, y_train)
    return search

if __name__ == "__main__":
    df = load_data(INPUT_FILE)
    df = handle_missing(df)

    targets = [t for t in ["Goals", "Assists"] if t in df.columns]
    if not targets:
        raise KeyError("No 'Goals' or 'Assists' columns found in dataset.")

    categorical_cols = []
    if "Position" in df.columns:
        categorical_cols = ["Position"]
    else:
        for c in df.select_dtypes(include=['object', 'category']).columns:
            if df[c].nunique() <= 20:
                categorical_cols.append(c)

    for target in targets:
        print(f"\n--- Preparing model for target: {target} ---")
        other = [t for t in ["Goals", "Assists"] if t != target and t in df.columns]
        features_to_remove = other
        X = df.drop(columns=[target] + features_to_remove)
        y = df[target]

        feature_types = {}
        categories_map = {}
        for c in X.columns:
            if c in categorical_cols:
                feature_types[c] = "categorical"
                categories_map[c] = sorted(X[c].astype(str).unique().tolist())
            else:
                feature_types[c] = "numeric"
        preprocessor = build_preprocessor([c for c in categorical_cols if c in X.columns])
        final_pipe = Pipeline([("preprocessor", preprocessor), ("model", XGBRegressor(objective="reg:squarederror",
                                                                                      random_state=RANDOM_STATE,
                                                                                      verbosity=0,
                                                                                      n_jobs=-1))])

        # hyperparam search for the pipeline (RandomizedSearchCV)
        param_dist = {
            "model__n_estimators": randint(200, 900),
            "model__learning_rate": uniform(0.01, 0.3),
            "model__max_depth": randint(3, 12),
            "model__subsample": uniform(0.5, 0.5),
            "model__colsample_bytree": uniform(0.5, 0.5)
        }
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TEST_SIZE, random_state=RANDOM_STATE)

        from sklearn.model_selection import RandomizedSearchCV
        search = RandomizedSearchCV(final_pipe, param_distributions=param_dist, n_iter=30, cv=3,
                                    scoring="r2", n_jobs=-1, random_state=RANDOM_STATE, verbose=1)
        print("Starting RandomizedSearchCV for target:", target)
        search.fit(X_train, y_train)

        best_pipe = search.best_estimator_
        # Save pipeline and metadata
        model_filename = f"xgb_{target.lower()}_pipeline.pkl"
        meta_filename = f"metadata_{target.lower()}.json"
        joblib.dump(best_pipe, model_filename)
        meta = {
            "features": X.columns.tolist(),
            "feature_types": feature_types,
            "categorical_cols": [c for c in categorical_cols if c in X.columns],
            "categories_map": categories_map
        }
        with open(meta_filename, "w") as f:
            json.dump(meta, f, indent=2)
        print(f"Saved {model_filename} and {meta_filename}")

    print("\nTraining complete. You can now run the Streamlit app (app_streamlit.py).")
