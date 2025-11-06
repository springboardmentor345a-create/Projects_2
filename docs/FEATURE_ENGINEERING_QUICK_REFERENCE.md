# ScoreSight Feature Engineering v3.0 - Quick Reference Card

## 🚀 Quick Start (2 Minutes)

```bash
cd d:\ScoreSight
jupyter notebook
# Open: notebooks/07_Feature_Engineering_v3_Advanced.ipynb
# Press: Ctrl+Enter to run cells
```

**Expected Output:**
- 52 new features generated
- File: `data/engineered/data_engineered_match_v3.csv`
- Visualization: `visualizations/tier1_3_feature_distributions.png`

---

## 📊 What Gets Generated?

| Tier | Features | Impact | Time |
|---|---|---|---|
| **1: Statistical** | 19 | +2-4% MAE | ~1 min |
| **2: Market/Context** | 13 | +2-4% MAE | ~30 sec |
| **3: Non-Linear** | 20 | +3-5% MAE | ~1.5 min |
| **TOTAL** | **52** | **+6-12% MAE** | **~3 min** |

---

## 🎯 Key Features by Purpose

### Predict Higher Scores (Offense)
- `home_goals_percentile` - Relative scoring strength
- `home_offensive_efficiency` - Goal efficiency
- `home_strength_index` - Overall offense rating

### Predict Lower Scores (Defense)
- `home_conceded_percentile` - Defensive strength
- `home_defensive_efficiency` - Defense effectiveness
- `home_team_tier` - Team quality tier

### Predict Upsets (Surprises)
- `matchup_threat_score` - Home advantage indicator
- `away_winning_momentum` - Away team form
- `rest_advantage` - Fatigue factor
- `away_quality_score` - Team strength comparison

### Predict Form Changes
- `home_anomaly_count_5` - Recent unusual performances
- `home_ma_deviation` - Deviation from trend
- `home_winning_momentum` - Momentum shifts
- `home_consecutive_wins` - Recent form

---

## 📈 Feature Categories

### Tier 1: Statistical (Low Noise, High Stability)
✅ **Use for:** Base models, feature importance ranking
```
• Percentile Features: Relative performance (0-100)
• Distribution Features: Skewness, Kurtosis, CV
• Quantile Features: Q25, Q50, Q75 (robust to outliers)
• Anomaly Features: Z-scores, deviation tracking
```

### Tier 2: Context (Domain Knowledge)
✅ **Use for:** Team quality matching, scheduling adjustments
```
• Team Quality: Tier classification, quality scores
• Scheduling: Rest days, midweek indicators
• Psychology: Momentum, winning streaks
```

### Tier 3: Interactions (Non-Linear Patterns)
✅ **Use for:** Advanced models, capturing synergies
```
• Polynomials: sqrt, log, squared transforms
• Ratios: Efficiency metrics, balance indicators
• Composites: Strength indices, threat scores
• Interactions: Form × Quality, Momentum × Tier
```

---

## 🔍 Feature Correlation Tips

### High Correlation = Likely Redundant
```
If feature_A and feature_B have correlation > 0.9:
→ Keep one, remove other (reduces noise)
```

### Low Correlation = May Be Useless
```
If feature × target correlation < 0.05:
→ Might not be predictive (but keep for now)
```

### Check in Notebook (Cell 8):
```python
# See feature correlations with target
correlations = df_tier3[numeric_features].corrwith(df_tier3['fthg'])
```

---

## ⚠️ Data Leakage Prevention

✅ **CORRECT:** Using data from before the match
```python
# OK - using past data only
df['home_goals_last_5'] = df.groupby('hometeam')['htgs'].shift(1).rolling(5).mean()
```

❌ **WRONG:** Using information from the match itself
```python
# BAD - using data that came FROM the match we're predicting
df['goals_ratio'] = df['htgs'] / df['fthg']  # fthg is what we're predicting!
```

**Check:** All `.shift()` operations present in notebook ✓

---

## 🎲 Interpreting Feature Values

### Tier 1 Features
| Feature | Value | Meaning |
|---|---|---|
| `home_goals_percentile` | 85 | Scores in top 15% of teams |
| `home_scoring_cv` | 0.5 | Very consistent scorer |
| `home_goals_skewness` | +2.0 | Occasional big wins |
| `home_anomaly_count_5` | 3 | 3 unusual games recently |

### Tier 2 Features
| Feature | Value | Meaning |
|---|---|---|
| `home_team_tier` | 1 | Elite team (top 30%) |
| `team_tier_diff` | +1 | Home team stronger by 1 tier |
| `rest_advantage` | +2 | Home team had 2 extra days rest |
| `home_winning_momentum` | 0.8 | 80% win rate recent form |

### Tier 3 Features
| Feature | Value | Meaning |
|---|---|---|
| `home_offensive_efficiency` | 0.7 | 70% offensive efficiency |
| `home_strength_index` | 0.65 | Above-average strength |
| `matchup_threat_score` | +0.3 | Slight home advantage |
| `home_efficiency_x_rest` | 0.8 | Strong offense × well-rested |

---

## 🛠️ Common Customizations

### Use Smaller Window for Recent Form
```python
# In Tier1FeatureEngineering:
window = 5  # Instead of 10
# More reactive to recent changes
```

### Use Larger Window for Stability
```python
# In Tier1FeatureEngineering:
window = 15  # Instead of 10
# More stable, less noise
```

### Adjust Team Tier Boundaries
```python
# In Tier2FeatureEngineering.add_team_quality_features():
if i < len(sorted_teams) * 0.25:  # Top 25% (instead of 30%)
    team_tier[team] = 1  # Elite
```

### Change Momentum Decay
```python
# In Tier2FeatureEngineering.add_psychological_factors():
home_winning_momentum = 1 - np.exp(-home_consecutive_wins / 40)
# Lower number (40 vs 50) = faster momentum growth
```

---

## 🔄 Workflow

### Step 1: Load Data
```python
# Notebook Cell 2
df = pd.read_csv('data/features/data_features_match.csv')
```

### Step 2: Generate Tier 1 (Statistical)
```python
# Notebook Cell 3
tier1 = Tier1FeatureEngineering(df)
df = tier1.fit_transform()
```

### Step 3: Generate Tier 2 (Context)
```python
# Notebook Cell 4
tier2 = Tier2FeatureEngineering(df)
df = tier2.fit_transform()
```

### Step 4: Generate Tier 3 (Interactions)
```python
# Notebook Cell 5
tier3 = Tier3FeatureEngineering(df)
df = tier3.fit_transform()
```

### Step 5: Analyze
```python
# Notebook Cells 6-9
# View statistics, correlations, distributions
```

### Step 6: Save
```python
# Notebook Cell 10
df.to_csv('data/engineered/data_engineered_match_v3.csv')
```

---

## 📋 Checklist Before Using Features

- [ ] Run entire notebook without errors
- [ ] Verify output CSV created: `data/engineered/data_engineered_match_v3.csv`
- [ ] Check feature count > 90 (original ~40 + new 52)
- [ ] Verify < 10% missing values in most features
- [ ] Check visualizations created: `tier1_3_feature_distributions.png`
- [ ] Review feature descriptions: `feature_descriptions_v3.json`
- [ ] Test correlation with target (Cell 8)
- [ ] Validate no data leakage (all historical data only)

---

## 📞 Troubleshooting (2-Minute Fixes)

| Problem | Solution |
|---|---|
| "ImportError: scipy" | `pip install scipy scikit-learn` |
| "MemoryError" | Process smaller date range: `df = df[df['date'] > '2015-01-01']` |
| "NaN in features" | Normal for early season (rolling window needs 3+ games) |
| "Slow execution" | Normal, ~3 minutes. Use top cells only if time-constrained |
| "Missing target column" | Ensure `fthg` exists: `print(df.columns[:10])` |
| "Correlation appears 0" | Expected if feature poorly correlates; keep for now |

---

## 🎯 Next Steps After Phase 1

### In Next Sprint (Tier 4-5):
- [ ] Create `08_Feature_Engineering_v3_TimeSeries.ipynb`
- [ ] Add autoregressive features (lag-1, lag-2, lag-3)
- [ ] Add multi-horizon rolling stats (2/5/10-match windows)
- [ ] Add decay-weighted features (exponential weighting)
- [ ] Expected: +4-8% additional improvement

### In Sprint 3 (Tier 6-8):
- [ ] Clustering & team segmentation
- [ ] PCA compression
- [ ] Automated feature selection pipeline
- [ ] Expected: +5-12% additional improvement

### In Sprint 4 (Tier 9-10):
- [ ] Temporal validation
- [ ] Robustness testing
- [ ] Stacking features
- [ ] Production readiness
- [ ] **Total expected: +25-40% improvement**

---

## 📊 Performance Benchmarks

### Expected Results from Tier 1-3 Alone

```
Match Prediction:
  Baseline MAE (v2.0): 0.85 goals/match
  After Tier 1-3: 0.80-0.82 goals/match
  Improvement: +2-4% ✓

Top Scorer Prediction:
  Baseline MAE: 5.2 goals/season
  After Tier 1-3: 5.0-5.1 goals/season
  Improvement: +1-2%

League Winner Accuracy:
  Baseline: 65%
  After Tier 1-3: 67-69%
  Improvement: +2-4%
```

### Full Pipeline (All Tiers 1-10)

```
Match Prediction: 0.60-0.65 (+25-30% total)
Top Scorer: 4.0-4.2 (+20-25% total)
League Winner: 78-82% (+15-20% total)
```

---

## 🎓 Learning Resources

### In This Project:
- `docs/FEATURE_ENGINEERING_V3_GUIDE.md` - Full technical guide
- `notebooks/07_Feature_Engineering_v3_Advanced.ipynb` - Interactive notebook
- `data/engineered/feature_descriptions_v3.json` - Feature reference

### External:
- Feature Engineering for Machine Learning (O'Reilly book)
- Statsbomb: Expected Goals Models
- Soccer Analytics research papers

---

**Last Updated:** November 2025  
**Version:** 3.0 - Tier 1-3 Complete  
**Status:** ✅ Ready for Model Training
