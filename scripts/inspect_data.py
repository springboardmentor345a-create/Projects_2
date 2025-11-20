import pandas as pd
from pathlib import Path

# Load data
data_path = Path('d:/ScoreSight/datasets/Match Winner.csv')
if not data_path.exists():
    print(f"File not found: {data_path}")
else:
    df = pd.read_csv(data_path)
    # Standardize columns as in the notebook
    df.columns = df.columns.str.lower().str.replace(' ', '_')
    
    # Standardize target column name
    possible_target_names = {
        'ftr': 'match_outcome',
        'result': 'match_outcome',
        'final_result': 'match_outcome',
        'match_result': 'match_outcome'
    }
    
    for name, new_name in possible_target_names.items():
        if name in df.columns and new_name not in df.columns:
            df.rename(columns={name: new_name}, inplace=True)
            break
    
    print("Available columns:", df.columns.tolist()[:15])
    
    # Pick a team, e.g., 'Arsenal'
    team = 'Arsenal'
    
    # Filter matches involving Arsenal
    team_matches = df[(df['hometeam'] == team) | (df['awayteam'] == team)].sort_values('date')
    
    print(f"\n--- Last 5 matches for {team} ---")
    # Check which columns exist
    desired_cols = ['date', 'hometeam', 'awayteam', 'fthg', 'ftag', 'match_outcome', 'htp', 'atp', 'htgs', 'atgs']
    cols = [c for c in desired_cols if c in df.columns]
    
    if len(team_matches) > 0:
        print(team_matches[cols].tail(5).to_string())
    else:
        print(f"No matches found for {team}")
