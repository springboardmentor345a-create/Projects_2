# ScoreSight ML Project - Problem Statements & Training Status

## Executive Summary

**Date:** 2025-11-06  
**Project:** ScoreSight Machine Learning System  
**Branch:** Prathamesh_Fuke

### Quick Status Overview

| # | Problem Statement | Dataset | Target | Type | Status |
|---|-------------------|---------|--------|------|---------|
| 1 | **League Winner Prediction** | league_winner_corrected.csv | League champion/position | Classification | ❌ NOT STARTED |
| 2 | **Match Winner Prediction** | data_final_match_prediction.csv | mw (Match winner) | Classification | ❌ NOT STARTED |
| 3 | **Top Scorer Prediction** | data_final_top_scorer.csv | goals scored | Regression | ❌ NOT STARTED |
| 4 | **Total Points Prediction** | data_final_points_tally.csv | target_total_points | Regression | ❌ NOT STARTED |
| 5 | **Match Result Prediction** | match_prediction_corrected.csv | Result (H/D/A) | Classification | ❌ NOT STARTED |

**Overall Progress:** 0/5 problem statements complete (0%)

---

## Problem Statement Details

### 1. Match Home Goals Prediction ✅ COMPLETE

**Objective:** Predict the number of goals scored by the home team in a match

**Dataset:**
- File: `data/engineered/data_engineered_match_v3.csv`
- Rows: 6,840 matches
- Features: 96 columns (78 features after preprocessing)
- Target: `fthg` (Full-Time Home Goals) - Regression task

**Training Notebook:** `notebooks/09_Root_Model_Training_v2.ipynb`

**Models Trained:**
1. Ridge Regression - MAE: 0.7912
2. Lasso Regression - MAE: 0.7886
3. Random Forest - MAE: 0.8024
4. Gradient Boosting - MAE: 0.7925
5. XGBoost - MAE: 0.7824
6. **LightGBM - MAE: 0.7785** ⭐ BEST

**Model Artifacts:**
- `models/ridge_v2.joblib`
- `models/lasso_v2.joblib`
- `models/randomforest_v2.joblib`
- `models/gradientboosting_v2.joblib`
- `models/xgboost_v2.joblib`
- `models/lightgbm_v2.joblib`

**Training Summary:** `data/engineered/model_training_summary_v2.json`

**Evaluation:**
- CV Strategy: Walk-Forward Temporal (5-fold, 60% initial)
- Hyperparameter Optimization: RandomizedSearchCV (20 iterations)
- Best Performance: MAE 0.7785 goals/match
- Status: **PRODUCTION READY**

---

### 2. Match Winner Prediction ❌ NOT STARTED

**Objective:** Predict which team wins the match (Home/Draw/Away)

**Dataset:**
- File: `data/engineered/data_engineered_match_prediction.csv`
- Rows: 6,822 matches
- Features: 56 columns (53 features after preprocessing)
- Target: `mw` (Match Winner) - Classification task (3 classes: H/D/A)

**Problem Type:** Multi-class Classification

**Suggested Models:**
1. Logistic Regression (baseline)
2. Random Forest Classifier
3. Gradient Boosting Classifier
4. XGBoost Classifier
5. LightGBM Classifier
6. Neural Network (optional)

**Evaluation Metrics:**
- Accuracy
- Precision/Recall/F1 (per class)
- Confusion Matrix
- ROC-AUC (one-vs-rest)

**Expected Notebook:** `notebooks/10_Match_Winner_Classification.ipynb`

**Expected Models:**
- `models/match_winner_logistic_v1.joblib`
- `models/match_winner_rf_v1.joblib`
- `models/match_winner_lgb_v1.joblib`
- etc.

---

### 3. League Points Tally & Winner Prediction ❌ NOT STARTED

**Objective:** Predict end-of-season outcomes for teams

**Dataset:**
- File: `data/engineered/data_engineered_league_points.csv`
- Rows: 180 team-seasons
- Features: 22 columns (19 features after preprocessing)
- Targets (Multiple):
  - `target_total_points` - Regression (total points in season)
  - `target_league_position` - Regression/Classification (final position 1-20)
  - `target_champion` - Binary Classification (1 if champion, 0 otherwise)

**Problem Types:**
1. **Points Tally Prediction:** Regression
2. **League Position Prediction:** Ordinal Regression or Multiclass Classification
3. **Champion Prediction:** Binary Classification

**Suggested Approach:**
- Train 3 separate models (one per target)
- Or use multi-output regression/classification

**Suggested Models:**
1. Ridge/Lasso (baseline for regression)
2. Random Forest (both regression and classification)
3. Gradient Boosting
4. XGBoost
5. LightGBM

**Evaluation Metrics:**
- **Points Tally:** MAE, RMSE, R²
- **League Position:** MAE, Accuracy (if classification)
- **Champion:** Accuracy, Precision, Recall, F1, ROC-AUC

**Expected Notebook:** `notebooks/11_League_Winner_Points_Prediction.ipynb`

**Expected Models:**
- `models/league_points_lgb_v1.joblib`
- `models/league_position_lgb_v1.joblib`
- `models/league_champion_lgb_v1.joblib`

---

### 4. Top Scorer Prediction ❌ NOT STARTED

**Objective:** Predict total goals scored by a player in a season

**Dataset:**
- File: `data/engineered/data_engineered_top_scorer.csv`
- Rows: 2,070 player-seasons
- Features: 44 columns (41 features after preprocessing)
- Target: `goals` - Regression task (total goals scored)

**Problem Type:** Regression

**Suggested Models:**
1. Ridge/Lasso (baseline)
2. Random Forest Regressor
3. Gradient Boosting Regressor
4. XGBoost Regressor
5. LightGBM Regressor

**Evaluation Metrics:**
- MAE (Mean Absolute Error)
- RMSE (Root Mean Squared Error)
- R² (Coefficient of Determination)

**Expected Notebook:** `notebooks/12_Top_Scorer_Prediction.ipynb`

**Expected Models:**
- `models/top_scorer_ridge_v1.joblib`
- `models/top_scorer_lgb_v1.joblib`
- `models/top_scorer_xgb_v1.joblib`

---

## Implementation Plan

### Phase 1: Match Winner Classification (Next Priority)

**Steps:**
1. Create `notebooks/10_Match_Winner_Classification.ipynb`
2. Load `data/engineered/data_engineered_match_prediction.csv`
3. Preprocess features (handle missing values, encoding)
4. Train 5-6 classification models
5. Evaluate with accuracy, F1, confusion matrix
6. Save best models to `models/` directory
7. Generate classification report and visualizations

**Estimated Time:** 30-45 minutes

---

### Phase 2: League Winner & Points Prediction

**Steps:**
1. Create `notebooks/11_League_Winner_Points_Prediction.ipynb`
2. Load `data/engineered/data_engineered_league_points.csv`
3. Train 3 separate pipelines:
   - Pipeline A: Total Points Regression
   - Pipeline B: League Position Prediction
   - Pipeline C: Champion Binary Classification
4. Evaluate each with appropriate metrics
5. Save all models to `models/` directory
6. Generate comprehensive report

**Estimated Time:** 45-60 minutes

---

### Phase 3: Top Scorer Prediction

**Steps:**
1. Create `notebooks/12_Top_Scorer_Prediction.ipynb`
2. Load `data/engineered/data_engineered_top_scorer.csv`
3. Train 5-6 regression models
4. Evaluate with MAE, RMSE, R²
5. Save best models to `models/` directory
6. Generate predictions and visualizations

**Estimated Time:** 30-45 minutes

---

## Data Summary

### Available Datasets

| Dataset | Rows | Columns | Problem Type | Target |
|---------|------|---------|-------------|---------|
| data_final_match_prediction.csv | 6,822 | 23 | Classification | mw (Match Winner) |
| data_final_points_tally.csv | 180 | 10 | Regression/Classification | Multiple targets |
| data_final_top_scorer.csv | 2,070 | 21 | Regression | goals |
| data_engineered_match_v3.csv | 6,840 | 96 | Regression | fthg (Home Goals) |
| data_engineered_match_prediction.csv | 6,822 | 56 | Classification | mw (Match Winner) |
| data_engineered_league_points.csv | 180 | 22 | Multiple | target_* columns |
| data_engineered_top_scorer.csv | 2,070 | 44 | Regression | goals |

---

## Current Model Inventory

### Trained Models (Problem #1 Only)

```
models/
├── ridge_v2.joblib                    # Ridge Regression (MAE 0.7912)
├── lasso_v2.joblib                    # Lasso Regression (MAE 0.7886)
├── randomforest_v2.joblib            # Random Forest (MAE 0.8024)
├── gradientboosting_v2.joblib        # Gradient Boosting (MAE 0.7925)
├── xgboost_v2.joblib                 # XGBoost (MAE 0.7824)
└── lightgbm_v2.joblib                # LightGBM (MAE 0.7785) ⭐ BEST
```

### Expected Models (After Full Implementation)

```
models/
├── # Problem 1: Match Home Goals (DONE)
├── lightgbm_v2.joblib
├── ...
│
├── # Problem 2: Match Winner Classification
├── match_winner_logistic_v1.joblib
├── match_winner_rf_v1.joblib
├── match_winner_lgb_v1.joblib
├── match_winner_xgb_v1.joblib
│
├── # Problem 3: League Predictions
├── league_points_lgb_v1.joblib       # Points regression
├── league_position_lgb_v1.joblib     # Position prediction
├── league_champion_lgb_v1.joblib     # Champion classification
│
└── # Problem 4: Top Scorer
    ├── top_scorer_ridge_v1.joblib
    ├── top_scorer_lgb_v1.joblib
    └── top_scorer_xgb_v1.joblib
```

---

## Recommended Next Steps

1. **IMMEDIATE:** Create Match Winner Classification notebook (Problem #2)
2. **NEXT:** Create League Winner & Points Prediction notebook (Problem #3)
3. **FINAL:** Create Top Scorer Prediction notebook (Problem #4)
4. **WRAP-UP:** Remove emojis across repo
5. **DEPLOY:** Commit and push all changes to branch

---

## Key Insights

### What We Have:
- ✅ Complete feature engineering for all 4 problem statements
- ✅ Engineered datasets ready for training
- ✅ One problem statement fully trained (Match Home Goals)
- ✅ Production-ready training pipeline template (can be reused)

### What We Need:
- ❌ Classification models for Match Winner (Problem #2)
- ❌ Regression/Classification models for League predictions (Problem #3)
- ❌ Regression models for Top Scorer (Problem #4)

### Time Estimate:
- Total remaining work: ~2-3 hours
- Can parallelize by creating all 3 notebooks simultaneously
- Leverage existing pipeline from notebook 09 as template

---

## Validation Checklist

Before marking each problem statement as complete, ensure:

- [ ] Training notebook created and executed
- [ ] All models trained with hyperparameter optimization
- [ ] Model artifacts saved to `models/` directory
- [ ] Training summary JSON generated
- [ ] Model comparison table/visualization created
- [ ] Best model identified
- [ ] Evaluation metrics documented
- [ ] No data leakage (temporal CV for time-series)
- [ ] Models production-ready (sklearn Pipeline with preprocessing)

---

**Status:** 1/4 Complete (25%)  
**Next Action:** Create notebook for Problem #2 (Match Winner Classification)  
**Last Updated:** 2025-11-06
