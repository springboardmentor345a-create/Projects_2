"""
Model Loading Utilities
Efficient caching and loading of trained models
"""
# Force reload: Updated features for ps3 models

import joblib
import streamlit as st
from pathlib import Path
import json

# Define model paths
MODELS_DIR = Path(__file__).parent.parent.parent / "models"

# Model configurations based on metadata
MODEL_CONFIG = {
    "league_winner": {
        "model_file": "ps1_league_winner_best_model.joblib",
        "metadata_file": "ps1_league_winner_metadata.json",
        "features": ["wins", "draws", "losses", "points_per_game", "goals_scored", "goals_conceded"],
        "target": "target_champion",
        "model_type": "RandomForest",
        "accuracy": 0.95
    },
    "match_winner": {
        "model_file": "match_winner_best_model.joblib",
        "metadata_file": "ps4_match_winner_metadata.json",
        "features": [
            "Points_Gap", "Goal_Difference_Gap", "Form_Gap",
            "Home_Goal_Difference", "Away_Goal_Difference",
            "Home_Win_Streak", "Away_Win_Streak",
            "Home_Goals_Scored", "Away_Goals_Scored", "Home_Goals_Conceded"
        ],
        "target": "match_outcome",
        "model_type": "XGBoost",
        "accuracy": 0.66
    },
    "top_scorer": {
        "model_file": "ps3_top_scorer_goals_model.joblib",
        "metadata_file": "ps3_top_scorer_goals_metadata.json",
        "features": [
            "position", "age", "matches_played", "starts", "minutes",
            "goals_per_90", "assists_per_90",
            "xg_per_90", "npxg_per_90", "xag_per_90", "npxg_plus_xag_per_90",
            "non_penalty_goals_per_90",
            "goals_per_xg", "assists_per_xag", "xag_impact", "npxg_impact",
            "goals_per_90 xg_per_90", "goals_per_90 npxg_per_90", "goals_per_90 xag_per_90",
            "goals_per_90 npxg_plus_xag_per_90", "goals_per_90 matches_played",
            "xg_per_90 matches_played", "npxg_per_90 matches_played"
        ],
        "target": "goals",
        "model_type": "XGBoost",
        "r2_score": 0.9408
    },
    "top_scorer_assists": {
        "model_file": "ps3_top_scorer_assists_model.joblib",
        "metadata_file": "ps3_top_scorer_assists_metadata.json",
        "features": [
            "position", "age", "matches_played", "starts", "minutes",
            "goals_per_90", "assists_per_90",
            "xg_per_90", "npxg_per_90", "xag_per_90", "npxg_plus_xag_per_90",
            "non_penalty_goals_per_90",
            "goals_per_xg", "assists_per_xag", "xag_impact", "npxg_impact",
            "goals_per_90 xg_per_90", "goals_per_90 npxg_per_90", "goals_per_90 xag_per_90",
            "goals_per_90 npxg_plus_xag_per_90", "goals_per_90 matches_played",
            "xg_per_90 matches_played", "npxg_per_90 matches_played"
        ],
        "target": "assists",
        "model_type": "XGBoost",
        "r2_score": 0.9778
    },
    "total_points": {
        "model_file": "ps3_total_points_best_model.joblib",
        "metadata_file": "ps3_total_points_metadata.json",
        "features": ["played", "gf", "ga", "gd"],
        "target": "points",
        "model_type": "Ridge",
        "r2_score": 0.937,
        "mae": 3.70
    }
}

@st.cache_resource
def load_model(model_name: str):
    """
    Load a trained model with caching
    
    Args:
        model_name: Name of the model (league_winner, match_winner, top_scorer, total_points)
        
    Returns:
        Loaded model object
    """
    if model_name not in MODEL_CONFIG:
        raise ValueError(f"Unknown model: {model_name}. Available: {list(MODEL_CONFIG.keys())}")
    
    config = MODEL_CONFIG[model_name]
    model_path = MODELS_DIR / config["model_file"]
    
    if not model_path.exists():
        raise FileNotFoundError(f"Model file not found: {model_path}")
    
    try:
        model = joblib.load(model_path)
        return model
    except Exception as e:
        raise RuntimeError(f"Failed to load model {model_name}: {str(e)}")

@st.cache_data
def load_metadata(model_name: str):
    """
    Load model metadata
    
    Args:
        model_name: Name of the model
        
    Returns:
        Dictionary containing metadata
    """
    if model_name not in MODEL_CONFIG:
        raise ValueError(f"Unknown model: {model_name}")
    
    config = MODEL_CONFIG[model_name]
    metadata_path = MODELS_DIR / config["metadata_file"]
    
    if not metadata_path.exists():
        return config  # Return basic config if metadata file not found
    
    try:
        with open(metadata_path, 'r') as f:
            metadata = json.load(f)
        return metadata
    except Exception as e:
        st.warning(f"Could not load metadata: {str(e)}")
        return config

def get_model_features(model_name: str):
    """
    Get the list of features required for a model
    
    Args:
        model_name: Name of the model
        
    Returns:
        List of feature names
    """
    if model_name not in MODEL_CONFIG:
        raise ValueError(f"Unknown model: {model_name}")
    
    return MODEL_CONFIG[model_name]["features"]

def get_model_info(model_name: str):
    """
    Get comprehensive model information
    
    Args:
        model_name: Name of the model
        
    Returns:
        Dictionary with model info
    """
    if model_name not in MODEL_CONFIG:
        raise ValueError(f"Unknown model: {model_name}")
    
    config = MODEL_CONFIG[model_name]
    metadata = load_metadata(model_name)
    
    return {
        "name": model_name,
        "type": config["model_type"],
        "features": config["features"],
        "target": config["target"],
        "metrics": metadata.get("metrics", {}),
        "config": config
    }

def validate_input(model_name: str, input_data: dict):
    """
    Validate input data for a model
    
    Args:
        model_name: Name of the model
        input_data: Dictionary of input features
        
    Returns:
        Tuple (is_valid, error_message)
    """
    required_features = get_model_features(model_name)
    
    # Check for missing features
    missing = set(required_features) - set(input_data.keys())
    if missing:
        return False, f"Missing required features: {', '.join(missing)}"
    
    # Check for extra features (warning, not error)
    extra = set(input_data.keys()) - set(required_features)
    if extra:
        st.warning(f"Extra features will be ignored: {', '.join(extra)}")
    
    # Check for None values
    none_features = [k for k, v in input_data.items() if v is None and k in required_features]
    if none_features:
        return False, f"Features cannot be None: {', '.join(none_features)}"
    
    return True, ""

def get_feature_order(model_name: str):
    """
    Get the correct order of features for a model
    
    Args:
        model_name: Name of the model
        
    Returns:
        List of feature names in correct order
    """
    return get_model_features(model_name)
