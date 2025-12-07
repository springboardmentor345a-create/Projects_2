# models.py
import pandas as pd

def problem1_logic(user_input_df):
    """
    Simple prediction function for league winner.
    """
    try:
        # Extract values
        wins = user_input_df['Wins'].iloc[0] if 'Wins' in user_input_df.columns else 0
        points_per_game = user_input_df['Points_Per_Game'].iloc[0] if 'Points_Per_Game' in user_input_df.columns else 0
        goal_diff = (user_input_df['Goals_Scored'].iloc[0] - user_input_df['Goals_Conceded'].iloc[0]) if all(col in user_input_df.columns for col in ['Goals_Scored', 'Goals_Conceded']) else 0
        
        # Simple champion prediction
        if points_per_game >= 2.3 and wins >= 25 and goal_diff >= 30:
            return "Champion"
        elif points_per_game >= 2.2 and wins >= 22:
            return "Potential Champion"
        else:
            return "Not Champion"
            
    except Exception as e:
        # Return a fallback prediction
        return "Champion"  # Default to Champion for now