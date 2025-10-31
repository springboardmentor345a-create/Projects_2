import pandas as pd

# Original columns from the Match Winner dataset (from image)
original_cols = [
    'Date', 'HomeTeam', 'AwayTeam', 'FTHG', 'FTAG', 'FTR', 
    'HTGS', 'ATGS', 'HTGC', 'ATGC', 'HTP', 'ATP', 
    'HM1', 'HM2', 'HM3', 'HM4', 'HM5', 
    'AM1', 'AM2', 'AM3', 'AM4', 'AM5', 
    'MW', 'HTFormPtsStr', 'ATFormPtsStr', 'HTFormPts', 'ATFormPts', 
    'HTWinStreak3', 'HTWinStreak5', 'HTLossStreak3', 'HTLossStreak5', 
    'ATWinStreak3', 'ATWinStreak5', 'ATLossStreak3', 'ATLossStreak5', 
    'HTGD', 'ATGD', 'DiffPts', 'DiffFormPts'
]

# Load final dataset
final_df = pd.read_csv('data/final/data_final_match_prediction.csv')
final_cols_lower = [c.lower() for c in final_df.columns]

print("="*80)
print("MATCH WINNER DATASET - COLUMN ANALYSIS")
print("="*80)
print(f"\nOriginal columns (from image): {len(original_cols)}")
print(f"Final columns (after optimization): {len(final_df.columns)}")

# Analyze what happened to each original column
print("\n" + "="*80)
print("COLUMN MAPPING ANALYSIS")
print("="*80)

retained = []
dropped = []
encoded = []

for col in original_cols:
    col_lower = col.lower().replace(' ', '_')
    col_encoded = col_lower + '_encoded'
    
    if col_lower in final_cols_lower:
        retained.append(col)
    elif col_encoded in final_cols_lower:
        encoded.append(col)
    else:
        dropped.append(col)

print(f"\n1. RETAINED AS-IS ({len(retained)} columns):")
print("-" * 80)
for i, col in enumerate(retained, 1):
    final_name = col.lower().replace(' ', '_')
    print(f"   {i:2d}. {col:20s} -> {final_name}")

print(f"\n2. ENCODED ({len(encoded)} columns):")
print("-" * 80)
for i, col in enumerate(encoded, 1):
    final_name = col.lower().replace(' ', '_') + '_encoded'
    print(f"   {i:2d}. {col:20s} -> {final_name}")

print(f"\n3. DROPPED ({len(dropped)} columns):")
print("-" * 80)
for i, col in enumerate(dropped, 1):
    print(f"   {i:2d}. {col}")

# Provide reasons for dropped columns
print("\n" + "="*80)
print("REASONS FOR DROPPING COLUMNS")
print("="*80)

reasons = {
    'Date': 'Temporal information already captured in MW (Match Week)',
    'HTFormPtsStr': 'Redundant - numeric HTFormPts already available',
    'ATFormPtsStr': 'Redundant - numeric ATFormPts already available',
    'HM1': 'Individual match results redundant - form captured in streaks',
    'HM2': 'Individual match results redundant - form captured in streaks',
    'HM3': 'Individual match results redundant - form captured in streaks',
    'HM4': 'Individual match results redundant - form captured in streaks',
    'HM5': 'Individual match results redundant - form captured in streaks',
    'AM1': 'Individual match results redundant - form captured in streaks',
    'AM2': 'Individual match results redundant - form captured in streaks',
    'AM3': 'Individual match results redundant - form captured in streaks',
    'AM4': 'Individual match results redundant - form captured in streaks',
    'AM5': 'Individual match results redundant - form captured in streaks',
}

for col in dropped:
    if col in reasons:
        print(f"\n{col}:")
        print(f"  Reason: {reasons[col]}")

print("\n" + "="*80)
print("SUMMARY")
print("="*80)
print(f"Total original columns: {len(original_cols)}")
print(f"Retained as-is: {len(retained)}")
print(f"Encoded (kept): {len(encoded)}")
print(f"Dropped: {len(dropped)}")
print(f"Final columns: {len(final_df.columns)}")
print(f"Reduction: {len(dropped)} columns ({len(dropped)/len(original_cols)*100:.1f}%)")
