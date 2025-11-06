# ScoreSight Feature Engineering v3.0 - Implementation Guide

**Version:** 3.0 - Advanced ML Optimization  
**Date:** November 2025  
**Author:** Prathamesh Fuke  
**Status:** Phase 1 Complete (Tiers 1-3)

---

## 📋 Table of Contents

1. [Quick Start](#quick-start)
2. [Architecture Overview](#architecture-overview)
3. [Implementation Status](#implementation-status)
4. [Tier-by-Tier Breakdown](#tier-by-tier-breakdown)
5. [Running the Notebook](#running-the-notebook)
6. [Feature Descriptions](#feature-descriptions)
7. [Next Steps & Roadmap](#next-steps--roadmap)
8. [Troubleshooting](#troubleshooting)

---

## 🚀 Quick Start

### Prerequisites
```bash
pip install pandas numpy scipy scikit-learn matplotlib seaborn
```

### Run the Notebook
```bash
jupyter notebook notebooks/07_Feature_Engineering_v3_Advanced.ipynb
```

### Expected Output
- **New Features Generated:** ~40 features across Tiers 1-3
- **Dataset Output:** `data/engineered/data_engineered_match_v3.csv`
- **Feature Descriptions:** `data/engineered/feature_descriptions_v3.json`
- **Visualizations:** `visualizations/tier1_3_feature_distributions.png`

---

## 🏗️ Architecture Overview

### Three-Tier Feature Engineering System

```
┌─────────────────────────────────────────────────────────────────┐
│        SCORESIGHT FEATURE ENGINEERING V3.0 ARCHITECTURE         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  TIER 1: STATISTICAL & DISTRIBUTIONAL (19 features)           │
│  ├─ Percentile Rankings                                        │
│  ├─ Distribution Characteristics (Skewness, Kurtosis)         │
│  ├─ Quantile-Based Statistics                                 │
│  └─ Anomaly Detection & Z-Scores                              │
│                                                                 │
│  TIER 2: MARKET & CONTEXT (13 features)                       │
│  ├─ Team Quality & Tier Classification                        │
│  ├─ Fixture Scheduling Effects                                │
│  └─ Psychological Motivation Factors                          │
│                                                                 │
│  TIER 3: NON-LINEAR & INTERACTIONS (20 features)              │
│  ├─ Polynomial Transformations                                │
│  ├─ Efficiency Ratio Metrics                                  │
│  ├─ Composite Threat Indices                                  │
│  └─ Feature Interactions                                       │
│                                                                 │
│  ─────────────────────────────────────────────────────────────│
│  TOTAL PHASE 1: ~52 NEW FEATURES (6-12% MAE improvement)      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📊 Implementation Status

### ✅ COMPLETED: Phase 1 - Tiers 1-3

#### Tier 1: Statistical & Distributional Features (19 features)
**Expected Impact:** +2-4% MAE

| Feature Category | Count | Implementation |
|---|---|---|
| Percentile Features | 4 | ✅ Implemented |
| Distribution Features | 4 | ✅ Implemented |
| Quantile Features | 8 | ✅ Implemented |
| Anomaly Features | 3 | ✅ Implemented |

**Key Features:**
- `home_goals_percentile` - Relative scoring performance (0-100 scale)
- `home_scoring_cv` - Coefficient of variation (consistency metric)
- `home_goals_skewness` - Distribution shape (lopsided vs consistent wins)
- `home_goals_iqr` - Interquartile range (consistency measure)
- `home_anomaly_count_5` - Recent unusual performances
- `home_ma_deviation` - Deviation from 5-game average

---

#### Tier 2: Market & Context Features (13 features)
**Expected Impact:** +2-4% MAE

| Feature Category | Count | Implementation |
|---|---|---|
| Team Quality Proxies | 5 | ✅ Implemented |
| Scheduling Effects | 4 | ✅ Implemented |
| Psychological Factors | 4 | ✅ Implemented |

**Key Features:**
- `home_team_tier` - Team classification (1=Elite, 2=Mid, 3=Struggling)
- `home_quality_score` - Normalized team quality [0-1]
- `team_tier_diff` - Tier differential (matchup advantage)
- `home_days_rest` - Recovery time since last match
- `rest_advantage` - Rest differential vs opponent
- `home_winning_momentum` - Confidence from recent wins (0-1)
- `is_midweek` - Fixture timing (impacts fatigue)

---

#### Tier 3: Non-Linear & Interaction Features (20 features)
**Expected Impact:** +3-5% MAE

| Feature Category | Count | Implementation |
|---|---|---|
| Polynomial Transforms | 6 | ✅ Implemented |
| Efficiency Ratios | 6 | ✅ Implemented |
| Composite Indices | 4 | ✅ Implemented |
| Interactions | 4 | ✅ Implemented |

**Key Features:**
- `home_goals_sqrt` - Square root transform (dampen large values)
- `home_goals_log` - Log transform (handle skewness)
- `home_offensive_efficiency` - Offense/defense balance
- `home_defensive_efficiency` - Defensive robustness (>0.5=strong)
- `home_strength_index` - Composite strength (0-1)
- `matchup_threat_score` - Home advantage prediction
- `home_form_x_quality` - Form × team quality interaction
- `home_efficiency_x_rest` - Efficiency × recovery interaction

---

### ⏳ IN PROGRESS: Phase 2 - Tiers 4-5 (Next Sprint)

#### Tier 4: Domain-Expert & Tactical Features (Planned)
- Formation analysis and matchup matrices
- Possession quality (progressive passes, dead ball vs open play)
- Shot quality metrics (xG outperformance, conversion rates)
- Chance creation pathways (counter vs positional play)
- Set-piece effectiveness

#### Tier 5: Time-Series & Sequential Features (Planned)
- Autoregressive features (lag-1, lag-2, lag-3)
- Multi-horizon rolling stats (2-match, 5-match, 10-match, season)
- Decay-weighted features (exponential recency weighting)
- Season phase encoding
- Form momentum indicators

---

### ⏸️ NOT STARTED: Phases 3-4

#### Tier 6-7: Clustering & Dimensionality Reduction
- Unsupervised clustering (K-means on match characteristics)
- Hierarchical team segmentation
- PCA compression (reducing 100+ features → 10 components)
- Feature interaction matrices

#### Tier 8: Automated Feature Selection
- Statistical correlation filtering
- Multicollinearity detection (VIF)
- Mutual information ranking
- Tree-based importance scoring
- LASSO regularization path
- RFE (Recursive Feature Elimination)
- Ensemble voting

#### Tier 9-10: Validation & Robustness
- Walk-forward temporal validation
- Season-aware train/test splits
- Outlier sensitivity analysis
- Missing data handling
- Stacking features (meta-features)
- Prediction confidence scoring

---

## 🔍 Tier-by-Tier Breakdown

### TIER 1: Statistical & Distributional Features

#### What Problem Does It Solve?
Raw values don't capture relative performance. A team scoring 2 goals could be:
- Outstanding performance (if they normally score 0.5 goals)
- Poor performance (if they normally score 3 goals)

#### Features Implemented

**1. Percentile Features**
```
home_goals_percentile = percentileofscore(team_goals, all_team_goals)
```
- **Meaning:** "Team scores more than X% of EPL teams"
- **Range:** 0-100
- **Use Case:** Identifies elite offenses vs average teams

**2. Distribution Features**
```
goals_scored_skewness = skew(last_10_goals)
goals_conceded_kurtosis = kurtosis(last_10_goals_conceded)
scoring_cv = std_goals / mean_goals
```
- **Skewness:** Positive = Few games with many goals; Negative = Consistent
- **Kurtosis:** High = Rare defeats but severe; Low = Predictable
- **CV:** Measures consistency relative to average

**3. Quantile Features**
```
goals_q25 = quantile(last_10_goals, 0.25)
goals_q50 = quantile(last_10_goals, 0.50)  # Median
goals_q75 = quantile(last_10_goals, 0.75)
goals_iqr = q75 - q25  # Interquartile range
```
- **Meaning:** Captures typical (Q50) vs best/worst (Q75/Q25)
- **Advantage:** Robust to outliers (median ≠ mean)

**4. Anomaly Features**
```
home_goals_zscore = (goals - mean) / std
anomaly_count = sum(|zscore| > 2)
```
- **Meaning:** "How many unusual performances recently?"
- **Use Case:** Detects form changes early

#### Expected Impact
- **+2-4% MAE improvement**
- Captures relative performance context
- Robust to outliers

---

### TIER 2: Market & External Context Features

#### What Problem Does It Solve?
Team performance varies by quality, scheduling, and psychological state.
- A big team losing 1-0 ≠ Small team losing 1-0
- Monday match after Sunday game ≠ Thursday match
- Losing streak reduces confidence

#### Features Implemented

**1. Team Quality & Tier Features**
```
# Classify teams into 3 tiers based on historical performance
home_team_tier = {1: Elite, 2: Mid-table, 3: Struggling}
team_tier_diff = home_tier - away_tier  # -2 to +2 range
home_quality_score = normalized_team_strength  # 0-1 range
```
- **Use Case:** Different models for Elite vs Struggling teams
- **Advantage:** Captures structural hierarchy

**2. Scheduling Features**
```
home_days_rest = days_since_last_home_fixture
away_days_rest = days_since_last_away_fixture
rest_advantage = home_days - away_days
is_midweek = fixture_is_monday_to_thursday
```
- **Meaning:** Rest impacts performance (tired teams underperform)
- **Typical Values:** 6-8 days normal; <3 days = fatigue risk
- **Example:** Saturday vs Monday = 2-day disadvantage

**3. Psychological Factors**
```
# Win rate in last 5 games
home_winning_momentum = consecutive_wins_last_5 / 5 * 100
winning_momentum_score = 1 - exp(-win_pct / 50)
```
- **Meaning:** Winning run boosts confidence exponentially
- **Range:** 0-1 (0=no wins, 1=all wins recently)
- **Effect:** Momentum is real but decays if team loses

#### Expected Impact
- **+2-4% MAE improvement (if quality data available)**
- Captures non-performance factors
- Context-aware predictions

---

### TIER 3: Non-Linear & Interaction Features

#### What Problem Does It Solve?
Linear relationships insufficient for sports. Effects are often:
- **Non-linear:** 2 wins ≠ 2× impact of 1 win
- **Interactive:** Strong attack + weak defense ≠ sum of effects

#### Features Implemented

**1. Polynomial Transformations**
```
home_goals_sqrt = sqrt(htgs)        # Dampen large values
home_goals_log = log1p(htgs)         # Handle skewness
home_points_sq = htp^2               # Capture non-linearity
```
- **sqrt:** Reduces extreme values' impact
- **log:** Transforms right-skewed distributions
- **sq:** Captures accelerating effects

**2. Efficiency Ratio Features**
```
offensive_efficiency = goals / (goals + conceded + 1)
defensive_efficiency = 1 / (1 + conceded / (scored + 1))
gd_efficiency = (goals - conceded) / (goals + conceded + 1)
points_efficiency = team_points / (team_points + opp_points + 1)
```
- **Range:** 0-1 (0=worst, 1=best)
- **Advantage:** Context-dependent (balance matters)
- **Example:** 2-2 vs 4-4 draw are equivalent (both 0.5 efficiency)

**3. Composite Strength Index**
```
strength_index = (0.35 × form +
                  0.25 × offensive_eff +
                  0.20 × defensive_eff +
                  0.20 × consistency)
```
- **Range:** 0-1 (composite score)
- **Components:** Weighted by predictive importance
- **Use:** Single feature capturing multiple dimensions

**4. Interaction Features**
```
form_x_quality = form_points × team_quality
momentum_x_tier = winning_momentum × (1 / team_tier)
efficiency_x_rest = offensive_eff × log(days_rest)
```
- **Meaning:** Effects multiply when both conditions met
- **Example:** Strong form + elite team = exponential advantage
- **Use:** Captures synergistic effects

#### Expected Impact
- **+3-5% MAE improvement**
- Captures non-linear relationships
- Identifies key interactions

---

## 📖 Feature Descriptions

### Complete Feature List (52 features)

#### Tier 1: Statistical Features (19)
| Feature | Type | Range | Description |
|---|---|---|---|
| home_goals_percentile | Continuous | 0-100 | Relative goal scoring performance |
| away_goals_percentile | Continuous | 0-100 | Away team relative scoring |
| home_conceded_percentile | Continuous | 0-100 | Defensive strength (inverse) |
| away_conceded_percentile | Continuous | 0-100 | Away defensive strength |
| home_goals_skewness | Continuous | -3 to 3 | Scoring distribution shape |
| away_goals_skewness | Continuous | -3 to 3 | Away scoring distribution |
| home_conceded_kurtosis | Continuous | -2 to 5 | Defensive tail risk |
| home_scoring_cv | Continuous | 0+ | Scoring consistency |
| home_goals_q25 | Continuous | 0+ | 25th percentile goals |
| home_goals_q50 | Continuous | 0+ | Median goals (robust) |
| home_goals_q75 | Continuous | 0+ | 75th percentile goals |
| away_goals_q25-q75 | Continuous | 0+ | Away quartiles |
| home_goals_iqr | Continuous | 0+ | Consistency (IQR) |
| away_goals_iqr | Continuous | 0+ | Away consistency |
| home_goals_zscore | Continuous | -4 to 4 | Standardized deviation |
| home_anomaly_count_5 | Integer | 0-5 | Recent unusual games |
| home_ma_deviation | Continuous | 0+ | Deviation from trend |

#### Tier 2: Market & Context (13)
| Feature | Type | Range | Description |
|---|---|---|---|
| home_team_tier | Categorical | 1, 2, 3 | Quality tier (Elite/Mid/Strug) |
| away_team_tier | Categorical | 1, 2, 3 | Away team tier |
| team_tier_diff | Integer | -2 to 2 | Tier matchup advantage |
| home_quality_score | Continuous | 0-1 | Normalized team quality |
| away_quality_score | Continuous | 0-1 | Away team quality |
| home_days_rest | Integer | 1-14 | Days since last match |
| away_days_rest | Integer | 1-14 | Away rest time |
| rest_advantage | Integer | -13 to 13 | Home rest - away rest |
| is_midweek | Binary | 0, 1 | Mon-Thu fixture flag |
| home_consecutive_wins | Continuous | 0-100 | Win % last 5 games |
| away_consecutive_wins | Continuous | 0-100 | Away win % |
| home_winning_momentum | Continuous | 0-1 | Exponential momentum |
| away_winning_momentum | Continuous | 0-1 | Away momentum |

#### Tier 3: Non-Linear & Interactions (20)
| Feature | Type | Range | Description |
|---|---|---|---|
| home_goals_sqrt | Continuous | 0+ | Square root transform |
| away_goals_sqrt | Continuous | 0+ | Away sqrt |
| home_goals_log | Continuous | 0+ | Log transform |
| away_goals_log | Continuous | 0+ | Away log |
| home_points_sq | Continuous | 0+ | Squared points |
| away_points_sq | Continuous | 0+ | Away squared |
| home_offensive_efficiency | Continuous | 0-1 | Offense/defense balance |
| away_offensive_efficiency | Continuous | 0-1 | Away efficiency |
| home_defensive_efficiency | Continuous | 0-1 | Defense strength |
| away_defensive_efficiency | Continuous | 0-1 | Away defense |
| home_gd_efficiency | Continuous | -1 to 1 | Goal diff efficiency |
| away_gd_efficiency | Continuous | -1 to 1 | Away GD eff |
| home_points_efficiency | Continuous | 0-1 | Points ratio |
| away_points_efficiency | Continuous | 0-1 | Away points ratio |
| home_strength_index | Continuous | 0-1 | Composite strength score |
| away_strength_index | Continuous | 0-1 | Away strength |
| matchup_threat_score | Continuous | -1 to 1 | Home advantage |
| home_h2h_advantage | Continuous | 0+ | Historical h2h |
| home_form_x_quality | Continuous | 0+ | Form × quality interaction |
| home_momentum_x_tier | Continuous | 0+ | Momentum × tier interaction |

---

## ▶️ Running the Notebook

### Step 1: Prepare Environment
```bash
# Navigate to ScoreSight directory
cd d:\ScoreSight

# Create virtual environment (optional)
python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
pip install jupyter
```

### Step 2: Start Jupyter
```bash
jupyter notebook
```

### Step 3: Open Notebook
1. Navigate to `notebooks/07_Feature_Engineering_v3_Advanced.ipynb`
2. Click to open

### Step 4: Run Cells
- **Cell 1:** Load libraries (takes ~10 seconds)
- **Cell 2:** Load data (takes ~5 seconds)
- **Cells 3-5:** Generate Tiers 1-3 (takes ~2-3 minutes total)
- **Cells 6-9:** Analysis & visualization (takes ~30 seconds)
- **Cells 10-11:** Save results (takes ~5 seconds)

### Total Runtime: ~3-4 minutes

---

## 🔧 Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'scipy'"
**Solution:**
```bash
pip install scipy scikit-learn
```

### Issue: "Memory Error" or very slow execution
**Solution:** Process in batches
```python
# In notebook, limit to recent seasons
df = df[df['date'] > '2015-01-01']  # Last 10 years
```

### Issue: Missing values in output features
**Cause:** Early season games have no rolling statistics
**Solution:** Features are 'NaN' until 3+ games played (expected)
```python
# Check missing data
df_tier3.isnull().sum()
```

### Issue: Features not correlated with target
**Cause:** May need different window sizes or aggregations
**Solution:** Experiment with window parameters in tier classes
```python
# In Tier1FeatureEngineering, modify:
window = 10  # Try 5, 7, 15 instead
```

---

## 🎯 Performance Benchmarks

### Expected Results After Tier 1-3

| Metric | Before | After | Improvement |
|---|---|---|---|
| Match Prediction MAE | 0.85 | 0.80-0.82 | +2-4% |
| Feature Count | ~40 | ~92 | +130% |
| Model Training Time | 5s | 8s | +60% |

### Feature Importance Distribution (Expected)
- **Top 5 features:** 35-45% of total importance
- **Top 10 features:** 55-65% of total importance
- **Top 20 features:** 75-85% of total importance

---

## 📈 Next Steps

### Immediate (This Week)
- [ ] Run Tier 1-3 notebook
- [ ] Validate features on validation set
- [ ] Check for data leakage
- [ ] Document any anomalies

### Short-term (Next 1-2 Weeks)
- [ ] Implement Tier 4: Tactical features
- [ ] Implement Tier 5: Time-series features
- [ ] Run Tier 4-5 notebook
- [ ] Expected improvement: +4-8% additional

### Medium-term (Weeks 3-4)
- [ ] Implement Tier 6-7: Clustering & PCA
- [ ] Implement Tier 8: Automated selection
- [ ] Feature selection pipeline
- [ ] Expected improvement: +5-12% additional

### Long-term (Week 4+)
- [ ] Implement Tier 9-10: Validation & robustness
- [ ] Full model retraining
- [ ] Production deployment
- [ ] **Total expected improvement: +25-40% MAE**

---

## 📚 References & Resources

### Recommended Reading
1. Feature Engineering for Machine Learning (O'Reilly)
2. Practical Statistics for Data Scientists
3. Sports Analytics research papers (Statsbomb, Expected Goals)

### Useful Libraries
- `pandas` - Data manipulation
- `numpy` - Numerical operations
- `scipy.stats` - Statistical functions
- `scikit-learn` - ML tools and preprocessing
- `pandas-profiling` - Data quality reports

---

## ✅ Checklist for Feature Usage

Before using features in models:

- [ ] Data leakage check (no future information used)
- [ ] Temporal validity (proper date sorting)
- [ ] Missing data handling (< 10% for most features)
- [ ] Outlier sensitivity (tested robustness)
- [ ] Documentation (clear descriptions saved)
- [ ] Validation (tested on holdout set)
- [ ] Correlation (checked multicollinearity)
- [ ] Business logic (makes intuitive sense)

---

## 📞 Support & Questions

For questions or issues:
1. Check this guide's troubleshooting section
2. Review feature descriptions in `feature_descriptions_v3.json`
3. Examine notebook comments and examples
4. Check git history for implementation details

---

**Last Updated:** November 2025  
**Current Phase:** 1 of 4 Complete  
**Next Update:** After Tier 4-5 Implementation
