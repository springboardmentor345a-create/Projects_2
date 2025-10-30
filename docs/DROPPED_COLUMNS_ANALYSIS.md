# Dropped Columns Analysis

**Date:** October 30, 2025  
**Author:** Prathamesh Fuke  
**Branch:** Prathamesh_Fuke

---

## Overview

This document details all columns that were dropped from the datasets during preprocessing to ensure only relevant features are used for model training. A total of 33 columns were removed across all three datasets.

---

## Dataset 1: Match Prediction Dataset

### Summary
- **Original Columns:** 40
- **Dropped Columns:** 14
- **Final Columns:** 26
- **Records:** 6,840 matches

### Dropped Columns Table

| Column Name | Reason for Dropping |
|-------------|---------------------|
| unnamed:_0 | Index column - redundant |
| date_encoded | Temporal information already captured in match week (MW) |
| htformptsstr_encoded | Redundant - numeric form points (htformpts) already available |
| atformptsstr_encoded | Redundant - numeric form points (atformpts) already available |
| hm1_encoded | Individual match results redundant - form captured in streaks |
| hm2_encoded | Individual match results redundant - form captured in streaks |
| hm3_encoded | Individual match results redundant - form captured in streaks |
| hm4_encoded | Individual match results redundant - form captured in streaks |
| hm5_encoded | Individual match results redundant - form captured in streaks |
| am1_encoded | Individual match results redundant - form captured in streaks |
| am2_encoded | Individual match results redundant - form captured in streaks |
| am3_encoded | Individual match results redundant - form captured in streaks |
| am4_encoded | Individual match results redundant - form captured in streaks |
| am5_encoded | Individual match results redundant - form captured in streaks |

### Retained Features (26)
- **Match Scores:** fthg, ftag
- **Team Statistics:** htgs, atgs, htgc, atgc, htp, atp
- **Form Indicators:** htformpts, atformpts
- **Streaks:** htwinstreak3, htwinstreak5, htlossstreak3, htlossstreak5, atwinstreak3, atwinstreak5, atlossstreak3, atlossstreak5
- **Goal Difference:** htgd, atgd, diffpts, diffformpts
- **Match Context:** mw, hometeam_encoded, awayteam_encoded, ftr_encoded

---

## Dataset 2: Top Scorer Prediction Dataset

### Summary
- **Original Columns:** 34
- **Dropped Columns:** 13
- **Final Columns:** 21
- **Records:** 2,274 player-season records

### Dropped Columns Table

| Column Name | Reason for Dropping |
|-------------|---------------------|
| unnamed:_0 | Index column - redundant |
| starts | Redundant - matches_played is sufficient |
| minutes | Redundant - per_90 statistics already normalized |
| 90s_played | Redundant - per_90 statistics already normalized |
| goals_+_assists | Derived feature - can be calculated from goals + assists |
| non_penalty_goals_+_assists_per_90 | Derived feature - redundant with individual per_90 stats |
| xg_+_xag_per_90 | Derived feature - redundant with individual xG stats |
| npxg_+_xag_per_90 | Derived feature - redundant with individual npxG stats |
| yellow_cards | Not relevant for scoring prediction |
| red_cards | Not relevant for scoring prediction |
| progressive_carries | Not directly related to goal scoring |
| progressive_passes | Not directly related to goal scoring |
| progressive_receives | Not directly related to goal scoring |

### Retained Features (21)
- **Basic Info:** age, matches_played
- **Scoring Stats:** goals, assists, non_penalty_goals, penalty_goals_made, penalty_attempts
- **Expected Goals:** xg, npxg, xag, npxg_+_xag
- **Per-90 Metrics:** goals_per_90, assists_per_90, goals_+_assists_per_90, non_penalty_goals_per_90, xg_per_90, xag_per_90, npxg_per_90
- **Player Context:** player_encoded, nation_encoded, position_encoded

---

## Dataset 3: Points Tally & League Winner Dataset

### Summary
- **Original Columns:** 16
- **Dropped Columns:** 6
- **Final Columns:** 10
- **Records:** 180 team-season records

### Dropped Columns Table

| Column Name | Reason for Dropping |
|-------------|---------------------|
| target_top_4 | Secondary target - focus on champion and total points |
| target_top_6 | Secondary target - focus on champion and total points |
| target_relegated | Secondary target - focus on champion and total points |
| wins | Redundant - points_per_game captures win/draw/loss ratio |
| draws | Redundant - points_per_game captures win/draw/loss ratio |
| losses | Redundant - points_per_game captures win/draw/loss ratio |

### Retained Features (10)
- **Match Stats:** matches_played, points_per_game
- **Goal Stats:** goals_scored, goals_conceded, goal_difference
- **Target Variables:** target_total_points, target_league_position, target_champion
- **Context:** season_encoded, team_encoded

---

## Impact on Problem Statement

### Problem Statement Alignment

The ScoreSight project aims to predict:
1. **Match Outcomes** - Predict match scores and winners
2. **Top Scorer** - Identify the season's leading goal scorer
3. **League Winner & Points Tally** - Forecast team points and champion

### How Column Removal Helps

#### Match Prediction
- Removed redundant encoded features that duplicated information
- Kept essential form indicators (streaks, points, goal difference)
- Retained team identifiers and match context
- **Result:** Cleaner dataset with 35% fewer features, no information loss

#### Top Scorer Prediction
- Removed derived features that can be calculated from base features
- Eliminated discipline stats (cards) not relevant to scoring
- Kept core scoring metrics and normalized per-90 statistics
- **Result:** Focused dataset with 38% fewer features, better model performance expected

#### League Winner Prediction
- Removed secondary classification targets to focus on main objectives
- Eliminated redundant win/draw/loss counts (captured in points_per_game)
- Kept essential performance metrics and primary targets
- **Result:** Streamlined dataset with 37.5% fewer features, clearer target definition

---

## Summary Statistics

| Dataset | Original Columns | Dropped | Retained | Reduction |
|---------|-----------------|---------|----------|-----------|
| Match Prediction | 40 | 14 | 26 | 35.0% |
| Top Scorer | 34 | 13 | 21 | 38.2% |
| Points Tally | 16 | 6 | 10 | 37.5% |
| **Total** | **90** | **33** | **57** | **36.7%** |

---

## Benefits of Column Reduction

1. **Reduced Overfitting Risk** - Fewer features mean less chance of model memorizing noise
2. **Faster Training** - 36.7% fewer features significantly reduce computation time
3. **Better Interpretability** - Cleaner feature set makes model insights clearer
4. **Improved Generalization** - Focus on essential features improves prediction on new data
5. **Lower Memory Usage** - Smaller datasets are easier to handle and process

---

## Validation

All dropped columns were verified to be either:
- Redundant (information available in other features)
- Derived (can be calculated from retained features)
- Irrelevant (not related to prediction targets)
- Index/metadata (not actual features)

No information critical to the problem statement was lost in the column reduction process.

---

**Status:** Complete  
**Next Step:** Model training with cleaned datasets
