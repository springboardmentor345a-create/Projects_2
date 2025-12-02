"""
Data Loading Utilities
Load and prepare data for predictions
"""

import pandas as pd
import streamlit as st
from pathlib import Path

# Define data paths
DATA_DIR = Path(__file__).parent.parent.parent.parent / "Task_Files" / "data"

@st.cache_data
def load_league_winner_data():
    """Load League Winner dataset"""
    data_path = DATA_DIR / "league_winner" / "league_winner_data.csv"
    if not data_path.exists():
        st.error(f"Data file not found: {data_path}")
        return None
    return pd.read_csv(data_path)

@st.cache_data
def load_match_winner_data():
    """Load Match Winner dataset"""
    data_path = DATA_DIR / "match_winner" / "match_winner_data.csv"
    if not data_path.exists():
        st.error(f"Data file not found: {data_path}")
        return None
    return pd.read_csv(data_path)

@st.cache_data
def load_top_scorer_data():
    """Load Top Scorer dataset"""
    data_path = DATA_DIR / "top_scorer" / "top_scorer_data.csv"
    if not data_path.exists():
        st.error(f"Data file not found: {data_path}")
        return None
    return pd.read_csv(data_path)

@st.cache_data
def load_points_tally_data():
    """Load Points Tally dataset"""
    data_path = DATA_DIR / "points_tally" / "points_tally_data.csv"
    if not data_path.exists():
        st.error(f"Data file not found: {data_path}")
        return None
    return pd.read_csv(data_path)

def get_unique_teams(data_source="match_winner"):
    """
    Get list of unique teams from datasets
    
    Args:
        data_source: Which dataset to use ('match_winner', 'league_winner', etc.)
        
    Returns:
        Sorted list of unique team names
    """
    if data_source == "match_winner":
        df = load_match_winner_data()
        if df is not None and 'hometeam' in df.columns:
            teams = pd.concat([df['hometeam'], df['awayteam']]).unique()
            return sorted(teams)
    elif data_source == "league_winner":
        df = load_league_winner_data()
        if df is not None and 'team' in df.columns:
            return sorted(df['team'].unique())
    
    return []

def get_team_stats(team_name, df, prefix='Home'):
    """
    Extract team statistics from match data
    
    Args:
        team_name: Name of the team
        df: DataFrame containing match data
        prefix: 'Home' or 'Away'
        
    Returns:
        Dictionary of team statistics
    """
    if df is None or df.empty:
        return {}
    
    # Filter for the team
    if prefix == 'Home':
        team_matches = df[df['hometeam'] == team_name]
    else:
        team_matches = df[df['awayteam'] == team_name]
    
    if team_matches.empty:
        return {}
    
    # Get most recent match stats
    latest = team_matches.iloc[-1]
    
    stats = {
        'current_points': latest.get(f'{prefix}_Current_Points', 0),
        'goals_scored': latest.get(f'{prefix}_Goals_Scored', 0),
        'goals_conceded': latest.get(f'{prefix}_Goals_Conceded', 0),
        'goal_difference': latest.get(f'{prefix}_Goal_Difference', 0),
        'win_streak': latest.get(f'{prefix}_Win_Streak', 0),
        'recent_points': latest.get(f'{prefix}_Recent_Points', 0),
    }
    
    return stats

def calculate_match_features(home_team, away_team, df):
    """
    Calculate features needed for match prediction
    
    Args:
        home_team: Home team name
        away_team: Away team name
        df: Match winner DataFrame
        
    Returns:
        Dictionary of calculated features
    """
    if df is None or df.empty:
        return None
    
    home_stats = get_team_stats(home_team, df, 'Home')
    away_stats = get_team_stats(away_team, df, 'Away')
    
    if not home_stats or not away_stats:
        return None
    
    features = {
        'Points_Gap': home_stats['current_points'] - away_stats['current_points'],
        'Goal_Difference_Gap': home_stats['goal_difference'] - away_stats['goal_difference'],
        'Form_Gap': home_stats['recent_points'] - away_stats['recent_points'],
        'Home_Goal_Difference': home_stats['goal_difference'],
        'Away_Goal_Difference': away_stats['goal_difference'],
        'Home_Win_Streak': home_stats['win_streak'],
        'Away_Win_Streak': away_stats['win_streak'],
        'Home_Goals_Scored': home_stats['goals_scored'],
        'Away_Goals_Scored': away_stats['goals_scored'],
        'Home_Goals_Conceded': home_stats['goals_conceded'],
    }
    
    return features

def get_sample_data(model_name: str, n_samples: int = 5):
    """
    Get sample data for demonstration
    
    Args:
        model_name: Name of the model
        n_samples: Number of samples to return
        
    Returns:
        DataFrame with sample data
    """
    if model_name == "league_winner":
        df = load_league_winner_data()
    elif model_name == "match_winner":
        df = load_match_winner_data()
    elif model_name == "top_scorer":
        df = load_top_scorer_data()
    elif model_name == "total_points":
        df = load_points_tally_data()
    else:
        return None
    
    if df is not None and not df.empty:
        return df.sample(min(n_samples, len(df)))
    
    return None
