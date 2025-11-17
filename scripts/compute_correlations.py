import json, pandas as pd, numpy as np, os
base = r'd:\ScoreSight'

reports = {}

def max_corr(df, features, target):
    # Drop duplicate columns (e.g., fthg/ftag repeated) to avoid ambiguity
    df = df.loc[:, ~df.columns.duplicated()]
    # Ensure target is not part of feature list selection
    cols = [c for c in features if c in df.columns and c != target]
    if target not in df.columns:
        return None
    sub = df[cols + [target]].select_dtypes(include=[np.number]).dropna()
    if sub.shape[0] == 0:
        return None
    corrs = []
    numeric_cols = set(sub.columns) - {target}
    for c in [c for c in cols if c in numeric_cols]:
        if pd.api.types.is_numeric_dtype(sub[c]):
            corr = sub[c].corr(sub[target])
            if pd.notna(corr):
                corrs.append((c, float(corr), float(abs(corr))))
    if not corrs:
        return None
    best = max(corrs, key=lambda x: x[2])
    return {'feature': best[0], 'corr': best[1], 'abs_corr': best[2]}

# PS1
ps1_features = json.load(open(os.path.join(base,'artifacts','feature_list_league_winner.json')))
ps1_df = pd.read_csv(os.path.join(base,'data','league_winner','league_winner_data.csv'))
ps1_target = 'target_champion'
reports['PS1'] = {'target': ps1_target, 'features': ps1_features, 'max_corr': max_corr(ps1_df, ps1_features, ps1_target)}

# PS2 (Top Scorer)
ps2_features = json.load(open(os.path.join(base,'artifacts','feature_list_top_scorer.json')))
ps2_df = pd.read_csv(os.path.join(base,'data','top_scorer','top_scorer_data.csv'))
ps2_target = 'goals'
reports['PS2'] = {'target': ps2_target, 'features': ps2_features, 'max_corr': max_corr(ps2_df, ps2_features, ps2_target)}

# PS3 home/away goals
ps3_features = json.load(open(os.path.join(base,'artifacts','feature_list_match_result.json')))
ps3_df = pd.read_csv(os.path.join(base,'data','match_result','match_result_data.csv'))
reports['PS3_home'] = {'target': 'fthg', 'features': ps3_features, 'max_corr': max_corr(ps3_df, ps3_features, 'fthg')}
reports['PS3_away'] = {'target': 'ftag', 'features': ps3_features, 'max_corr': max_corr(ps3_df, ps3_features, 'ftag')}

# PS4 points
ps4_features = json.load(open(os.path.join(base,'artifacts','feature_list_points_tally.json')))
ps4_df = pd.read_csv(os.path.join(base,'data','points_tally','points_tally_data.csv'))
ps4_target = 'points'
reports['PS4'] = {'target': ps4_target, 'features': ps4_features, 'max_corr': max_corr(ps4_df, ps4_features, ps4_target)}

# PS5 classification
ps5_features = json.load(open(os.path.join(base,'artifacts','feature_list_match_winner.json')))
ps5_df = pd.read_csv(os.path.join(base,'data','match_winner','match_winner_data.csv'))
ps5_target = 'target'
reports['PS5'] = {'target': ps5_target, 'features': ps5_features, 'max_corr': max_corr(ps5_df, ps5_features, ps5_target)}

print(json.dumps(reports, indent=2))
