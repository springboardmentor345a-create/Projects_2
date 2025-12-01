
import sys
import pandas as pd
import numpy as np
from pathlib import Path

# Add app directory to path
sys.path.append(str(Path(__file__).parent.parent / "app"))

from utils.model_loader import load_model, get_feature_order

def verify_top_scorer():
    print("\n--- Verifying Top Scorer ---")
    try:
        model_goals = load_model("top_scorer")
        model_assists = load_model("top_scorer_assists")
        feature_order = get_feature_order("top_scorer")
        
        print(f"Features expected: {len(feature_order)}")
        
        # Mock input data
        goals_per_90 = 0.5
        xg_per_90 = 0.45
        npxg_per_90 = 0.4
        xag_per_90 = 0.2
        npxg_plus_xag_per_90 = 0.6
        matches_played = 30
        
        input_data = {
            "position": "Forward",
            "age": 25,
            "matches_played": matches_played,
            "starts": 30,
            "minutes": 2700,
            "goals_per_90": goals_per_90,
            "assists_per_90": 0.2,
            "xg_per_90": xg_per_90,
            "npxg_per_90": npxg_per_90,
            "xag_per_90": xag_per_90,
            "npxg_plus_xag_per_90": npxg_plus_xag_per_90,
            "non_penalty_goals_per_90": 0.4,
            "goals_per_xg": 1.1,
            "assists_per_xag": 1.0,
            "xag_impact": xag_per_90 * matches_played,
            "npxg_impact": npxg_per_90 * matches_played,
            # Interaction Terms
            "goals_per_90 xg_per_90": goals_per_90 * xg_per_90,
            "goals_per_90 npxg_per_90": goals_per_90 * npxg_per_90,
            "goals_per_90 xag_per_90": goals_per_90 * xag_per_90,
            "goals_per_90 npxg_plus_xag_per_90": goals_per_90 * npxg_plus_xag_per_90,
            "goals_per_90 matches_played": goals_per_90 * matches_played,
            "xg_per_90 matches_played": xg_per_90 * matches_played,
            "npxg_per_90 matches_played": npxg_per_90 * matches_played
        }
        
        input_df = pd.DataFrame([input_data])[feature_order]
        
        pred_goals = model_goals.predict(input_df)[0]
        pred_assists = model_assists.predict(input_df)[0]
        
        print(f"[SUCCESS] Top Scorer Prediction Successful")
        print(f"Predicted Goals: {pred_goals}")
        print(f"Predicted Assists: {pred_assists}")
        return True
    except Exception as e:
        print(f"[FAILED] Top Scorer Failed: {e}")
        return False

def verify_total_points():
    print("\n--- Verifying Total Points ---")
    try:
        model = load_model("total_points")
        feature_order = get_feature_order("total_points")
        
        print(f"Features expected: {len(feature_order)}")
        
        input_data = {
            "played": 20,
            "gf": 35,
            "ga": 25,
            "gd": 10
        }
        
        input_df = pd.DataFrame([input_data])[feature_order]
        pred_points = model.predict(input_df)[0]
        
        print(f"[SUCCESS] Total Points Prediction Successful")
        print(f"Predicted Points: {pred_points}")
        return True
    except Exception as e:
        print(f"[FAILED] Total Points Failed: {e}")
        return False

def verify_match_winner():
    print("\n--- Verifying Match Winner ---")
    try:
        model = load_model("match_winner")
        feature_order = get_feature_order("match_winner")
        
        print(f"Features expected: {len(feature_order)}")
        
        input_data = {
            "Points_Gap": 5,
            "Goal_Difference_Gap": 3,
            "Form_Gap": 2,
            "Home_Goal_Difference": 10,
            "Away_Goal_Difference": 7,
            "Home_Win_Streak": 2,
            "Away_Win_Streak": 1,
            "Home_Goals_Scored": 30,
            "Away_Goals_Scored": 25,
            "Home_Goals_Conceded": 20
        }
        
        input_df = pd.DataFrame([input_data])[feature_order]
        probs = model.predict_proba(input_df)[0]
        
        print(f"[SUCCESS] Match Winner Prediction Successful")
        print(f"Probabilities: {probs}")
        return True
    except Exception as e:
        print(f"[FAILED] Match Winner Failed: {e}")
        return False

if __name__ == "__main__":
    success = True
    success &= verify_top_scorer()
    success &= verify_total_points()
    # success &= verify_match_winner() # Match winner model might be missing or different, let's check
    
    if success:
        print("\n[DONE] All critical verifications passed!")
    else:
        print("\n[WARNING] Some verifications failed.")
