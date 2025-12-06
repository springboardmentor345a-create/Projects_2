# main.py
from fastapi import FastAPI, HTTPException
import pandas as pd
from models import (
    problem1_logic,
    problem2_logic,
    problem3_logic,
    problem4_logic,
    problem5_logic,
)
import os

app = FastAPI(title="5 Problems API")

# Data file paths (adjust filenames if needed)
LEAGUE_CSV = os.path.join("data", "League_Winner_Cleaned.csv")
MATCH_CSV = os.path.join("data", "Match_Winner_Cleaned.csv")
GOALS_CSV = os.path.join("data", "Goals_and_Assists_Cleaned.csv")

# Load datasets at startup (if available). Keep as None if missing.
df_league = None
df_match = None
df_goals = None

def _try_load_csv(path):
    try:
        return pd.read_csv(path)
    except Exception as e:
        print(f"Warning: failed to load {path}: {e}")
        return None

df_league = _try_load_csv(LEAGUE_CSV)
df_match = _try_load_csv(MATCH_CSV)
df_goals = _try_load_csv(GOALS_CSV)


@app.get("/health")
def health():
    return {"status": "ok", "message": "Backend running"}


@app.get("/problem1")
def run_problem1():
    if df_league is None:
        raise HTTPException(status_code=500, detail="League dataset not available.")
    try:
        result = problem1_logic(df_league)
        return {"problem": 1, "dataset": "League_Winner_Cleaned", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/problem2")
def run_problem2():
    if df_match is None:
        raise HTTPException(status_code=500, detail="Match dataset not available.")
    try:
        result = problem2_logic(df_match)
        return {"problem": 2, "dataset": "Match_Winner_Cleaned", "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/problem3")
def run_problem3():
    if df_goals is None:
        raise HTTPException(status_code=500, detail="Goals/Assists dataset not available.")
    try:
        result = problem3_logic(df_goals)
        return {
            "problem": 3,
            "dataset": "Goals_and_Assists_Cleaned (Goals only)",
            "result": result,
        }
    except KeyError as ke:
        raise HTTPException(status_code=400, detail=str(ke))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/problem4")
def run_problem4():
    if df_goals is None:
        raise HTTPException(status_code=500, detail="Goals/Assists dataset not available.")
    try:
        result = problem4_logic(df_goals)
        return {
            "problem": 4,
            "dataset": "Goals_and_Assists_Cleaned (Assists only)",
            "result": result,
        }
    except KeyError as ke:
        raise HTTPException(status_code=400, detail=str(ke))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/problem5")
def run_problem5():
    if df_league is None:
        raise HTTPException(status_code=500, detail="League dataset not available.")
    try:
        result = problem5_logic(df_league)
        return {
            "problem": 5,
            "dataset": "League_Winner_Cleaned (Total Points)",
            "result": result,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
