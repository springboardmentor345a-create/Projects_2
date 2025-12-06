# app.py
"""
Streamlit frontend for 5 problems:
1. League Winner        -> uses League_Winner_Cleaned.csv
2. Match Winner         -> uses Match_Winner_Cleaned.csv
3. Goals                -> uses Goals_Assist_Cleaned.csv (ONLY 'Goals' column)
4. Assists              -> uses Goals_Assist_Cleaned.csv (ONLY 'Assists' column)
5. Total Points         -> uses League_Winner_Cleaned.csv ('target_total_points' or 'points_per_game')

Put CSV files under ./data:
 - data/League_Winner_Cleaned.csv
 - data/Match_Winner_Cleaned.csv
 - data/Goals_Assist_Cleaned.csv
"""

import streamlit as st
import pandas as pd
from pathlib import Path

# Import your problem logic functions from models.py
# models.py must be in the same folder or in the PYTHONPATH
from models import problem1_logic, problem2_logic, problem3_logic, problem4_logic, problem5_logic

DATA_DIR = Path("data")
DEFAULT_LEAGUE = DATA_DIR / "League_Winner_Cleaned.csv"
DEFAULT_MATCH = DATA_DIR / "Match_Winner_Cleaned.csv"
DEFAULT_GOALS = DATA_DIR / "Goals_Assist_Cleaned.csv"

st.set_page_config(page_title="5 Problems Dashboard", layout="wide")
st.title("5 Problems Dashboard — League / Match / Goals / Assists / Total Points")

# --- Helper to load CSV with fallback ---
def load_csv(path: Path):
    try:
        return pd.read_csv(path)
    except Exception as e:
        st.warning(f"Could not load {path}: {e}")
        return None

# --- Upload or use default datasets ---
st.sidebar.header("Datasets (upload to override)")

league_file = st.sidebar.file_uploader("Upload League_Winner_Cleaned.csv", type=["csv"], key="league")
match_file = st.sidebar.file_uploader("Upload Match_Winner_Cleaned.csv", type=["csv"], key="match")
goals_file = st.sidebar.file_uploader("Upload Goals_Assist_Cleaned.csv", type=["csv"], key="goals")

if league_file:
    df_league = pd.read_csv(league_file)
else:
    df_league = load_csv(DEFAULT_LEAGUE)

if match_file:
    df_match = pd.read_csv(match_file)
else:
    df_match = load_csv(DEFAULT_MATCH)

if goals_file:
    df_goals = pd.read_csv(goals_file)
else:
    df_goals = load_csv(DEFAULT_GOALS)

# --- Utility: run model and display safely ---
def run_and_show(func, df, description: str):
    with st.spinner(f"Running {description}..."):
        try:
            result = func(df)
        except Exception as e:
            st.error(f"Error running {description}: {e}")
            return

    st.subheader(f"{description} — Output")
    # Display result intelligently
    if isinstance(result, (pd.DataFrame, pd.Series)):
        st.dataframe(result)
    elif isinstance(result, (list, tuple)):
        try:
            st.write(pd.DataFrame(result))
        except Exception:
            st.write(result)
    elif isinstance(result, dict):
        st.json(result)
    else:
        st.write(result)

# === Problem 1: League Winner ===
st.header("Problem 1 — League Winner")
st.markdown("Uses `League_Winner_Cleaned.csv` and `League_Winner_Model`.")
if df_league is None:
    st.warning("League dataset not loaded. Upload file in the sidebar or add data/League_Winner_Cleaned.csv")
else:
    st.markdown("Preview (first 5 rows):")
    st.dataframe(df_league.head())
    if st.button("Run Problem 1 - League Winner"):
        run_and_show(problem1_logic, df_league, "Problem 1 (League Winner)")

# === Problem 2: Match Winner ===
st.header("Problem 2 — Match Winner")
st.markdown("Uses `Match_Winner_Cleaned.csv` and `Match_Winner_Model`.")
if df_match is None:
    st.warning("Match dataset not loaded. Upload file in the sidebar or add data/Match_Winner_Cleaned.csv")
else:
    st.markdown("Preview (first 5 rows):")
    st.dataframe(df_match.head())
    if st.button("Run Problem 2 - Match Winner"):
        run_and_show(problem2_logic, df_match, "Problem 2 (Match Winner)")

# === Problem 3: Goals (ONLY Goals column) ===
st.header("Problem 3 — Goals")
st.markdown("Uses `Goals_Assist_Cleaned.csv` and `Goals_and_Assists_Model` — **only** the `Goals` column is passed.")
if df_goals is None:
    st.warning("Goals dataset not loaded. Upload file in the sidebar or add data/Goals_Assist_Cleaned.csv")
else:
    st.markdown("Preview (first 5 rows):")
    st.dataframe(df_goals.head())
    # Confirm column exists
    if "Goals" not in df_goals.columns:
        st.error("Column `Goals` not found in Goals_Assist_Cleaned.csv. Please ensure the column exists exactly as `Goals`.")
    else:
        # Create a small DataFrame with only Goals column per your requirement
        df_goals_only = df_goals[["Goals"]].copy()
        st.markdown("Goals-only data preview:")
        st.dataframe(df_goals_only.head())
        if st.button("Run Problem 3 - Goals"):
            run_and_show(problem3_logic, df_goals_only, "Problem 3 (Goals)")

# === Problem 4: Assists (ONLY Assists column) ===
st.header("Problem 4 — Assists")
st.markdown("Uses `Goals_Assist_Cleaned.csv` and `Goals_and_Assists_Model` — **only** the `Assists` column is passed.")
if df_goals is None:
    st.warning("Goals dataset not loaded. Upload file in the sidebar or add data/Goals_Assist_Cleaned.csv")
else:
    if "Assists" not in df_goals.columns:
        st.error("Column `Assists` not found in Goals_Assist_Cleaned.csv. Please ensure the column exists exactly as `Assists`.")
    else:
        df_assists_only = df_goals[["Assists"]].copy()
        st.markdown("Assists-only data preview:")
        st.dataframe(df_assists_only.head())
        if st.button("Run Problem 4 - Assists"):
            run_and_show(problem4_logic, df_assists_only, "Problem 4 (Assists)")

# === Problem 5: Total Points ===
st.header("Problem 5 — Total Points")
st.markdown("Uses `League_Winner_Cleaned.csv`. If column `target_total_points` exists it will be used; otherwise `points_per_game` is available.")
if df_league is None:
    st.warning("League dataset not loaded. Upload file in the sidebar or add data/League_Winner_Cleaned.csv")
else:
    st.markdown("Preview (first 5 rows):")
    st.dataframe(df_league.head())
    # Choose which column to use for total points (preference for target_total_points)
    if "target_total_points" in df_league.columns:
        df_total_points_input = df_league[["target_total_points"]].copy()
    elif "points_per_game" in df_league.columns:
        df_total_points_input = df_league[["points_per_game"]].copy()
    elif "points" in df_league.columns:
        df_total_points_input = df_league[["points"]].copy()
    else:
        st.error("No appropriate total points column found (expected one of: 'target_total_points', 'points_per_game', 'points'). Please update the CSV or upload a correct file.")
        df_total_points_input = None

    if df_total_points_input is not None:
        st.markdown("Total-points input preview:")
        st.dataframe(df_total_points_input.head())
        if st.button("Run Problem 5 - Total Points"):
            run_and_show(problem5_logic, df_total_points_input, "Problem 5 (Total Points)")

# Footer
st.markdown("---")
st.caption("If models/functions raise errors, check that models.py's functions accept a DataFrame and the expected column names match exactly.")
