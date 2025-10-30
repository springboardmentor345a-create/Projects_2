import pandas as pd
import os

# Columns to drop analysis based on problem statement
# Problem: Predict Match Outcomes, Top Scorer, League Winner & Points Tally

print("="*80)
print("DROPPING UNNECESSARY COLUMNS")
print("="*80)

# ============================================================================
# MATCH PREDICTION DATASET
# ============================================================================
print("\n1. MATCH PREDICTION DATASET")
print("-"*80)

match_df = pd.read_csv('data/final/data_final_match_prediction.csv')
print(f"Original shape: {match_df.shape}")

# Columns to drop:
# - unnamed:_0: Index column (redundant)
# - date_encoded: Date not needed for prediction (temporal info captured in MW)
# - htformptsstr_encoded, atformptsstr_encoded: Redundant (htformpts/atformpts already numeric)
# - hm1-5, am1-5 encoded: Individual match results redundant (form captured in streaks/points)

match_drop_cols = [
    'unnamed:_0',
    'date_encoded',
    'htformptsstr_encoded',
    'atformptsstr_encoded',
    'hm1_encoded', 'hm2_encoded', 'hm3_encoded', 'hm4_encoded', 'hm5_encoded',
    'am1_encoded', 'am2_encoded', 'am3_encoded', 'am4_encoded', 'am5_encoded'
]

# 1. MATCH PREDICTION DATASET: REMOVE DATA LEAK FEATURES - ONLY PRE-MATCH STATS
# Drop all columns not available pre-match or that are targets
leak_cols = ['fthg', 'ftag', 'ftr_encoded']  # outcome variables
match_drop_cols += [col for col in leak_cols if col in match_df.columns]
match_df_clean = match_df.drop(columns=match_drop_cols, errors='ignore')
print(f"NEW: Also dropping leakage columns: {leak_cols}")

print(f"Dropped columns: {match_drop_cols}")
print(f"New shape: {match_df_clean.shape}")
print(f"Remaining columns: {list(match_df_clean.columns)}")

# Save cleaned dataset
match_df_clean.to_csv('data/final/data_final_match_prediction.csv', index=False)
print("Saved cleaned match prediction dataset")

# ============================================================================
# PLAYER (TOP SCORER) DATASET
# ============================================================================
print("\n2. TOP SCORER PREDICTION DATASET")
print("-"*80)

player_df = pd.read_csv('data/final/data_final_top_scorer.csv')
print(f"Original shape: {player_df.shape}")

# Columns to drop:
# - unnamed:_0: Index column (redundant)
# - starts: Redundant (matches_played is sufficient)
# - minutes, 90s_played: Redundant (per_90 stats already normalized)
# - goals_+_assists: Derived (goals + assists)
# - non_penalty_goals_+_assists_per_90: Derived
# - xg_+_xag_per_90: Derived
# - npxg_+_xag_per_90: Derived
# - yellow_cards, red_cards: Not relevant for scoring prediction
# - progressive_carries, progressive_passes, progressive_receives: Not directly related to scoring

player_drop_cols = [
    'unnamed:_0',
    'starts',
    'minutes',
    '90s_played',
    'goals_+_assists',
    'non_penalty_goals_+_assists_per_90',
    'xg_+_xag_per_90',
    'npxg_+_xag_per_90',
    'yellow_cards',
    'red_cards',
    'progressive_carries',
    'progressive_passes',
    'progressive_receives'
]

# Player Top Scorer Prediction: Only features available BEFORE season/event can be used for valid prediction. Many statistics are only known after the season. Use errors='ignore' to prevent error if columns do not exist as user may pre-trimmed data.
player_df_clean = player_df.drop(columns=player_drop_cols, errors='ignore')
print(f"Dropped columns: {player_drop_cols}")
print(f"New shape: {player_df_clean.shape}")
print(f"Remaining columns: {list(player_df_clean.columns)}")

# Save cleaned dataset
player_df_clean.to_csv('data/final/data_final_top_scorer.csv', index=False)
print("Saved cleaned top scorer dataset")

# ============================================================================
# LEAGUE (POINTS TALLY) DATASET
# ============================================================================
print("\n3. POINTS TALLY & LEAGUE WINNER DATASET")
print("-"*80)

league_df = pd.read_csv('data/final/data_final_points_tally.csv')
print(f"Original shape: {league_df.shape}")

# Columns to drop:
# - target_top_4, target_top_6, target_relegated: Secondary targets (focus on champion & points)
# - wins, draws, losses: Redundant (points_per_game captures this)

league_drop_cols = [
    'target_top_4',
    'target_top_6',
    'target_relegated',
    'wins',
    'draws',
    'losses'
]

# League Points Dataset: Only features available BEFORE end of season are valid - drop with errors='ignore' for safety
league_df_clean = league_df.drop(columns=league_drop_cols, errors='ignore')
print(f"Dropped columns: {league_drop_cols}")
print(f"New shape: {league_df_clean.shape}")
print(f"Remaining columns: {list(league_df_clean.columns)}")

# Save cleaned dataset
league_df_clean.to_csv('data/final/data_final_points_tally.csv', index=False)
print("Saved cleaned points tally dataset")

# ============================================================================
# SUMMARY
# ============================================================================
print("\n" + "="*80)
print("SUMMARY OF DROPPED COLUMNS")
print("="*80)
print(f"\nMatch Prediction: Dropped {len(match_drop_cols)} columns")
print(f"Top Scorer: Dropped {len(player_drop_cols)} columns")
print(f"Points Tally: Dropped {len(league_drop_cols)} columns")
print(f"\nTotal columns dropped: {len(match_drop_cols) + len(player_drop_cols) + len(league_drop_cols)}")
print("\nAll cleaned datasets saved successfully!")
