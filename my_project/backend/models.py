# models.py

import pandas as pd
import joblib

# ----------------------------
#  LOAD ALL TRAINED MODELS
# ----------------------------
league_winner_model = joblib.load("models/League_Winner_Model.pkl")
match_winner_model = joblib.load("models/Match_Winner_Model.pkl")
goals_assists_model = joblib.load("models/Goals_and_Assists_Model.pkl")
total_points_model = joblib.load("models/Total_Team_Points.pkl")

# --------------------------------
#   PROBLEM 1: League Winner
# --------------------------------
def problem1_logic(df):
    return league_winner_model.predict(df)

# --------------------------------
#   PROBLEM 2: Match Winner
# --------------------------------
def problem2_logic(df):
    return match_winner_model.predict(df)

# --------------------------------
#   PROBLEM 3: Goals Prediction
#   (use only GOALS columns)
# --------------------------------
def problem3_logic(df):
    df_goals = df[["goals"]]  # ONLY goals column
    return goals_assists_model.predict(df_goals)

# --------------------------------
#   PROBLEM 4: Assists Prediction
#   (use only ASSISTS columns)
# --------------------------------
def problem4_logic(df):
    df_assists = df[["assists"]]  # ONLY assists column
    return goals_assists_model.predict(df_assists)

# --------------------------------
#   PROBLEM 5: Total Points
# --------------------------------
def problem5_logic(df):
    return total_points_model.predict(df)
