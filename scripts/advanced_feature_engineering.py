import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

class AdvancedFeatureEngineering:
    """
    Comprehensive feature engineering for ScoreSight EPL prediction models.
    Generates advanced features for match prediction, top scorer, and league points datasets.
    """
    
    def __init__(self, correlation_threshold=0.95):
        self.correlation_threshold = correlation_threshold
        self.new_features_info = {}
        self.removed_features = []
        
    def engineer_match_features(self, df):
        """
        Generate advanced features for match prediction dataset.
        
        Input: DataFrame with columns including team stats, form points, streaks
        Output: DataFrame with new engineered features
        """
        df_eng = df.copy()
        print("Generating Match Prediction Features...")
        
        # 1. INTERACTION FEATURES (Home vs Away Comparison)
        df_eng['home_offensive_vs_away_defensive'] = (
            df_eng['htgs'] / (df_eng['atgc'] + 1)
        )
        self.new_features_info['home_offensive_vs_away_defensive'] = (
            'Ratio of home goals scored to away goals conceded (offensive strength vs defensive weakness)'
        )
        
        df_eng['away_offensive_vs_home_defensive'] = (
            df_eng['atgs'] / (df_eng['htgc'] + 1)
        )
        self.new_features_info['away_offensive_vs_home_defensive'] = (
            'Ratio of away goals scored to home goals conceded'
        )
        
        df_eng['offensive_balance'] = (
            (df_eng['htgs'] - df_eng['atgs']) / (df_eng['htgs'] + df_eng['atgs'] + 1)
        )
        self.new_features_info['offensive_balance'] = (
            'Offensive balance between home and away teams'
        )
        
        df_eng['defensive_balance'] = (
            (df_eng['htgc'] - df_eng['atgc']) / (df_eng['htgc'] + df_eng['atgc'] + 1)
        )
        self.new_features_info['defensive_balance'] = (
            'Defensive balance between home and away teams'
        )
        
        # 2. RATIO AND PERCENTAGE FEATURES
        df_eng['home_points_pct'] = (
            df_eng['htp'] / (df_eng['htp'] + df_eng['atp'] + 1)
        )
        self.new_features_info['home_points_pct'] = (
            'Home team points as percentage of total available points'
        )
        
        df_eng['away_points_pct'] = (
            df_eng['atp'] / (df_eng['htp'] + df_eng['atp'] + 1)
        )
        self.new_features_info['away_points_pct'] = (
            'Away team points as percentage of total available points'
        )
        
        df_eng['form_points_ratio'] = (
            df_eng['htformpts'] / (df_eng['atformpts'] + 1)
        )
        self.new_features_info['form_points_ratio'] = (
            'Home form points to away form points ratio'
        )
        
        df_eng['home_goals_conceded_ratio'] = (
            df_eng['htgc'] / (df_eng['htgs'] + 1)
        )
        self.new_features_info['home_goals_conceded_ratio'] = (
            'Home goals conceded to home goals scored ratio'
        )
        
        df_eng['away_goals_conceded_ratio'] = (
            df_eng['atgc'] / (df_eng['atgs'] + 1)
        )
        self.new_features_info['away_goals_conceded_ratio'] = (
            'Away goals conceded to away goals scored ratio'
        )
        
        # 3. POLYNOMIAL FEATURES FOR NON-LINEAR RELATIONSHIPS
        df_eng['home_points_squared'] = df_eng['htp'] ** 2
        self.new_features_info['home_points_squared'] = (
            'Home team points squared (captures non-linear impact)'
        )
        
        df_eng['away_points_squared'] = df_eng['atp'] ** 2
        self.new_features_info['away_points_squared'] = (
            'Away team points squared'
        )
        
        df_eng['home_gd_squared'] = df_eng['htgd'] ** 2
        self.new_features_info['home_gd_squared'] = (
            'Home goal difference squared'
        )
        
        df_eng['away_gd_squared'] = df_eng['atgd'] ** 2
        self.new_features_info['away_gd_squared'] = (
            'Away goal difference squared'
        )
        
        df_eng['total_goals_interaction'] = df_eng['htgs'] * df_eng['atgs']
        self.new_features_info['total_goals_interaction'] = (
            'Interaction between home and away goals scored'
        )
        
        # 4. TEAM STRENGTH INDEX
        df_eng['home_strength_index'] = (
            (df_eng['htp'] * 0.4 + df_eng['htgs'] * 0.35 + df_eng['htgd'] * 0.25) / 10
        )
        self.new_features_info['home_strength_index'] = (
            'Composite home team strength (weighted: points 40%, goals 35%, GD 25%)'
        )
        
        df_eng['away_strength_index'] = (
            (df_eng['atp'] * 0.4 + df_eng['atgs'] * 0.35 + df_eng['atgd'] * 0.25) / 10
        )
        self.new_features_info['away_strength_index'] = (
            'Composite away team strength'
        )
        
        df_eng['strength_index_diff'] = (
            df_eng['home_strength_index'] - df_eng['away_strength_index']
        )
        self.new_features_info['strength_index_diff'] = (
            'Difference in team strength indices (home - away)'
        )
        
        # 5. HOME ADVANTAGE INDICATORS
        df_eng['home_goal_advantage'] = df_eng['htgs'] - df_eng['atgs']
        self.new_features_info['home_goal_advantage'] = (
            'Home goals scored minus away goals scored'
        )
        
        df_eng['home_form_advantage'] = df_eng['htformpts'] - df_eng['atformpts']
        self.new_features_info['home_form_advantage'] = (
            'Home form points minus away form points'
        )
        
        df_eng['home_points_advantage'] = df_eng['htp'] - df_eng['atp']
        self.new_features_info['home_points_advantage'] = (
            'Home total points minus away total points'
        )
        
        # 6. MOMENTUM FEATURES FROM STREAKS
        df_eng['home_positive_momentum'] = (
            df_eng['htwinstreak3'] + df_eng['htwinstreak5']
        )
        self.new_features_info['home_positive_momentum'] = (
            'Home team positive momentum (combined win streaks)'
        )
        
        df_eng['away_positive_momentum'] = (
            df_eng['atwinstreak3'] + df_eng['atwinstreak5']
        )
        self.new_features_info['away_positive_momentum'] = (
            'Away team positive momentum'
        )
        
        df_eng['home_negative_momentum'] = (
            df_eng['htlossstreak3'] + df_eng['htlossstreak5']
        )
        self.new_features_info['home_negative_momentum'] = (
            'Home team negative momentum (combined loss streaks)'
        )
        
        df_eng['away_negative_momentum'] = (
            df_eng['atlossstreak3'] + df_eng['atlossstreak5']
        )
        self.new_features_info['away_negative_momentum'] = (
            'Away team negative momentum'
        )
        
        df_eng['momentum_balance'] = (
            df_eng['home_positive_momentum'] - df_eng['away_positive_momentum']
        )
        self.new_features_info['momentum_balance'] = (
            'Home positive momentum minus away positive momentum'
        )
        
        # 7. TEMPORAL FEATURES (Matchweek progression)
        df_eng['matchweek_normalized'] = df_eng['mw'] / 38.0
        self.new_features_info['matchweek_normalized'] = (
            'Matchweek normalized to 0-1 scale (season progression)'
        )
        
        df_eng['early_season'] = (df_eng['mw'] <= 10).astype(int)
        self.new_features_info['early_season'] = (
            'Binary indicator: 1 if early season (MW 1-10), 0 otherwise'
        )
        
        df_eng['late_season'] = (df_eng['mw'] >= 29).astype(int)
        self.new_features_info['late_season'] = (
            'Binary indicator: 1 if late season (MW 29-38), 0 otherwise'
        )
        
        # 8. DOMINANCE SCORES
        df_eng['home_dominance_score'] = (
            (df_eng['htp'] / 38.0) * 0.4 +
            (df_eng['htgs'] / (df_eng['htgs'] + df_eng['htgc'] + 1)) * 0.3 +
            ((df_eng['htgd'] + 50) / 100.0) * 0.3
        )
        self.new_features_info['home_dominance_score'] = (
            'Home team dominance score (normalized 0-1): points efficiency, goal ratio, GD'
        )
        
        df_eng['away_dominance_score'] = (
            (df_eng['atp'] / 38.0) * 0.4 +
            (df_eng['atgs'] / (df_eng['atgs'] + df_eng['atgc'] + 1)) * 0.3 +
            ((df_eng['atgd'] + 50) / 100.0) * 0.3
        )
        self.new_features_info['away_dominance_score'] = (
            'Away team dominance score'
        )
        
        # 9. CUMULATIVE METRICS
        df_eng['total_goals_season'] = df_eng['htgs'] + df_eng['atgs']
        self.new_features_info['total_goals_season'] = (
            'Combined total goals scored by both teams'
        )
        
        df_eng['total_points_accumulated'] = df_eng['htp'] + df_eng['atp']
        self.new_features_info['total_points_accumulated'] = (
            'Combined total points accumulated by both teams'
        )
        
        df_eng['avg_points_per_team'] = df_eng['total_points_accumulated'] / 2.0
        self.new_features_info['avg_points_per_team'] = (
            'Average points per team'
        )
        
        # 10. CONSISTENCY FEATURES
        df_eng['form_consistency'] = np.abs(
            df_eng['htformpts'] - df_eng['atformpts']
        )
        self.new_features_info['form_consistency'] = (
            'Absolute difference in form points (form gap)'
        )
        
        df_eng['points_consistency'] = np.abs(
            df_eng['htp'] - df_eng['atp']
        )
        self.new_features_info['points_consistency'] = (
            'Absolute difference in total points'
        )
        
        print(f"Generated {len(self.new_features_info)} new match features")
        return df_eng
    
    def engineer_player_features(self, df):
        """
        Generate advanced features for top scorer prediction dataset.
        
        Input: DataFrame with player statistics
        Output: DataFrame with new engineered features
        """
        df_eng = df.copy()
        print("Generating Top Scorer Features...")
        
        # 1. EFFICIENCY METRICS
        df_eng['goals_per_match'] = (
            df_eng['goals'] / (df_eng['matches_played'] + 1)
        )
        self.new_features_info['goals_per_match'] = (
            'Goals per match (average goals scored per game)'
        )
        
        df_eng['assists_per_match'] = (
            df_eng['assists'] / (df_eng['matches_played'] + 1)
        )
        self.new_features_info['assists_per_match'] = (
            'Assists per match'
        )
        
        df_eng['combined_per_match'] = (
            (df_eng['goals'] + df_eng['assists']) / (df_eng['matches_played'] + 1)
        )
        self.new_features_info['combined_per_match'] = (
            'Combined goals and assists per match'
        )
        
        # 2. SCORING CONSISTENCY
        df_eng['scoring_consistency'] = (
            df_eng['goals_per_90'] / (df_eng['goals_per_90'] + 1)
        )
        self.new_features_info['scoring_consistency'] = (
            'Scoring consistency ratio (per-90 efficiency)'
        )
        
        df_eng['penalty_ratio'] = (
            df_eng['penalty_goals_made'] / (df_eng['penalty_attempts'] + 1)
        )
        self.new_features_info['penalty_ratio'] = (
            'Penalty conversion rate (penalties scored / attempts)'
        )
        
        df_eng['open_play_goal_ratio'] = (
            df_eng['non_penalty_goals'] / (df_eng['goals'] + 1)
        )
        self.new_features_info['open_play_goal_ratio'] = (
            'Open play goal ratio (non-penalty goals / total goals)'
        )
        
        # 3. AGE-PERFORMANCE INTERACTION
        df_eng['age_squared'] = df_eng['age'] ** 2
        self.new_features_info['age_squared'] = (
            'Age squared (captures non-linear age effects)'
        )
        
        df_eng['age_goals_interaction'] = df_eng['age'] * df_eng['goals']
        self.new_features_info['age_goals_interaction'] = (
            'Interaction between age and goals (age * goals)'
        )
        
        df_eng['age_efficiency_index'] = (
            df_eng['goals_per_90'] / (df_eng['age'] / 25.0 + 0.5)
        )
        self.new_features_info['age_efficiency_index'] = (
            'Efficiency adjusted for age (normalized to age 25)'
        )
        
        # 4. EXPERIENCE-WEIGHTED PERFORMANCE
        df_eng['experience_factor'] = (
            df_eng['matches_played'] / (df_eng['matches_played'] + 10.0)
        )
        self.new_features_info['experience_factor'] = (
            'Experience factor (0-1): matches played / (matches + 10)'
        )
        
        df_eng['experience_weighted_goals'] = (
            df_eng['goals'] * (1 + df_eng['experience_factor'] * 0.3)
        )
        self.new_features_info['experience_weighted_goals'] = (
            'Goals weighted by player experience'
        )
        
        df_eng['prime_age_indicator'] = (
            (26 - np.abs(df_eng['age'] - 26)) / 26.0
        )
        self.new_features_info['prime_age_indicator'] = (
            'Prime age indicator (peaks at age 26, 0-1 scale)'
        )
        
        # 5. EXPECTED VS ACTUAL PERFORMANCE
        df_eng['goals_vs_xg'] = df_eng['goals'] - df_eng['xg']
        self.new_features_info['goals_vs_xg'] = (
            'Goal overperformance vs expected (goals - xG)'
        )
        
        df_eng['goals_vs_xg_ratio'] = (
            df_eng['goals'] / (df_eng['xg'] + 1)
        )
        self.new_features_info['goals_vs_xg_ratio'] = (
            'Goal overperformance ratio (goals / xG)'
        )
        
        df_eng['npxg_performance'] = (
            df_eng['non_penalty_goals'] - df_eng['npxg']
        )
        self.new_features_info['npxg_performance'] = (
            'Non-penalty goal overperformance (non_penalty_goals - npxG)'
        )
        
        df_eng['assists_vs_xag'] = df_eng['assists'] - df_eng['xag']
        self.new_features_info['assists_vs_xag'] = (
            'Assist overperformance vs expected (assists - xAG)'
        )
        
        # 6. COMPOSITE SCORING THREAT INDEX
        df_eng['scoring_threat_index'] = (
            (df_eng['goals_per_90'] * 0.35) +
            (df_eng['xg_per_90'] * 0.25) +
            (df_eng['goals_vs_xg_ratio'] * 0.2) +
            ((df_eng['matches_played'] / 38.0) * 0.2)
        )
        self.new_features_info['scoring_threat_index'] = (
            'Composite scoring threat (goals/90: 35%, xG/90: 25%, overperformance: 20%, availability: 20%)'
        )
        
        # 7. INVOLVEMENT METRICS
        df_eng['total_involvement'] = df_eng['goals'] + df_eng['assists']
        self.new_features_info['total_involvement'] = (
            'Total goal involvement (goals + assists)'
        )
        
        df_eng['involvement_per_90'] = (
            df_eng['goals_+_assists_per_90']
        )
        self.new_features_info['involvement_per_90'] = (
            'Goal involvement per 90 minutes'
        )
        
        df_eng['primary_threat_ratio'] = (
            df_eng['goals'] / (df_eng['total_involvement'] + 1)
        )
        self.new_features_info['primary_threat_ratio'] = (
            'Primary threat ratio (goals / total involvement)'
        )
        
        # 8. MATCH AVAILABILITY
        df_eng['match_availability'] = (
            df_eng['matches_played'] / 38.0
        )
        self.new_features_info['match_availability'] = (
            'Match availability ratio (matches / 38 season games)'
        )
        
        df_eng['high_availability'] = (
            (df_eng['matches_played'] >= 30).astype(int)
        )
        self.new_features_info['high_availability'] = (
            'Binary: 1 if player available in 30+ matches, 0 otherwise'
        )
        
        # 9. COMBINED PERFORMANCE METRICS
        df_eng['overall_threat_score'] = (
            (df_eng['goals_per_90'] * 0.4) +
            (df_eng['assists_per_90'] * 0.3) +
            (df_eng['match_availability'] * 0.2) +
            (df_eng['prime_age_indicator'] * 0.1)
        )
        self.new_features_info['overall_threat_score'] = (
            'Overall threat score: goals/90 (40%), assists/90 (30%), availability (20%), age (10%)'
        )
        
        # 10. VOLATILITY AND CONSISTENCY
        df_eng['xg_consistency'] = (
            1 - (np.abs(df_eng['goals'] - df_eng['xg']) / (df_eng['xg'] + 1))
        ).clip(0, 1)
        self.new_features_info['xg_consistency'] = (
            'Consistency with expected output (1 = perfectly consistent)'
        )
        
        df_eng['penalty_dependence'] = (
            df_eng['penalty_goals_made'] / (df_eng['goals'] + 1)
        )
        self.new_features_info['penalty_dependence'] = (
            'Penalty dependence ratio (penalties / total goals)'
        )
        
        print(f"Generated {len([k for k in self.new_features_info.keys() if 'player' not in str(k).lower()])} new player features")
        return df_eng
    
    def engineer_league_features(self, df):
        """
        Generate advanced features for league points and winner prediction dataset.
        
        Input: DataFrame with season-level team aggregates
        Output: DataFrame with new engineered features
        """
        df_eng = df.copy()
        print("Generating League Points Features...")
        
        # 1. PERFORMANCE CONSISTENCY
        df_eng['goal_conversion_efficiency'] = (
            df_eng['goals_scored'] / (df_eng['goals_scored'] + df_eng['goals_conceded'] + 1)
        )
        self.new_features_info['goal_conversion_efficiency'] = (
            'Goal conversion efficiency (goals_scored / total_goals)'
        )
        
        df_eng['defensive_solidity'] = (
            1 - (df_eng['goals_conceded'] / (df_eng['goals_conceded'] + 10.0))
        )
        self.new_features_info['defensive_solidity'] = (
            'Defensive solidity index (1 - normalized goals conceded)'
        )
        
        df_eng['offensive_power'] = (
            df_eng['goals_scored'] / df_eng['matches_played']
        )
        self.new_features_info['offensive_power'] = (
            'Average goals scored per match'
        )
        
        df_eng['defensive_strength'] = (
            df_eng['goals_conceded'] / df_eng['matches_played']
        )
        self.new_features_info['defensive_strength'] = (
            'Average goals conceded per match'
        )
        
        # 2. COMPETITIVE BALANCE
        df_eng['point_accumulation_rate'] = (
            df_eng['points_per_game']
        )
        self.new_features_info['point_accumulation_rate'] = (
            'Points per game (already in data, included for reference)'
        )
        
        df_eng['win_equivalent_rate'] = (
            df_eng['points_per_game'] / 3.0
        )
        self.new_features_info['win_equivalent_rate'] = (
            'Equivalent wins per game (points_per_game / 3)'
        )
        
        df_eng['projected_final_points'] = (
            df_eng['points_per_game'] * 38.0
        )
        self.new_features_info['projected_final_points'] = (
            'Projected final season points (PPG * 38)'
        )
        
        # 3. OFFENSIVE/DEFENSIVE BALANCE
        df_eng['attacking_vs_defensive_balance'] = (
            (df_eng['goals_scored'] - df_eng['goals_conceded']) / 
            (df_eng['goals_scored'] + df_eng['goals_conceded'] + 1)
        )
        self.new_features_info['attacking_vs_defensive_balance'] = (
            'Balance between offensive and defensive performance'
        )
        
        df_eng['offensive_dominance'] = (
            df_eng['goals_scored'] / (df_eng['goals_scored'] + 1)
        )
        self.new_features_info['offensive_dominance'] = (
            'Offensive dominance index (goals_scored / normalized)'
        )
        
        df_eng['defensive_vulnerability'] = (
            df_eng['goals_conceded'] / (df_eng['goals_conceded'] + 1)
        )
        self.new_features_info['defensive_vulnerability'] = (
            'Defensive vulnerability index'
        )
        
        # 4. GOAL DIFFERENCE ANALYSIS
        df_eng['gd_per_match'] = (
            df_eng['goal_difference'] / df_eng['matches_played']
        )
        self.new_features_info['gd_per_match'] = (
            'Average goal difference per match'
        )
        
        df_eng['gd_squared'] = df_eng['goal_difference'] ** 2
        self.new_features_info['gd_squared'] = (
            'Goal difference squared (captures magnitude of dominance)'
        )
        
        df_eng['positive_gd_indicator'] = (df_eng['goal_difference'] > 0).astype(int)
        self.new_features_info['positive_gd_indicator'] = (
            'Binary: 1 if goal difference positive, 0 otherwise'
        )
        
        # 5. PERFORMANCE TIERS
        df_eng['elite_performance'] = (
            (df_eng['points_per_game'] >= 2.0).astype(int)
        )
        self.new_features_info['elite_performance'] = (
            'Binary: 1 if PPG >= 2.0 (elite), 0 otherwise'
        )
        
        df_eng['title_contender'] = (
            (df_eng['points_per_game'] >= 1.8).astype(int)
        )
        self.new_features_info['title_contender'] = (
            'Binary: 1 if PPG >= 1.8 (title contender), 0 otherwise'
        )
        
        df_eng['mid_table'] = (
            ((df_eng['points_per_game'] >= 1.2) & 
             (df_eng['points_per_game'] < 1.8)).astype(int)
        )
        self.new_features_info['mid_table'] = (
            'Binary: 1 if mid-table (1.2 <= PPG < 1.8), 0 otherwise'
        )
        
        # 6. STRENGTH COMPOSITE INDEX
        df_eng['team_strength_composite'] = (
            (df_eng['offensive_power'] / 3.0 * 0.3) +
            ((1 - df_eng['defensive_strength'] / 3.0) * 0.3) +
            ((df_eng['points_per_game'] / 3.0) * 0.4)
        )
        self.new_features_info['team_strength_composite'] = (
            'Composite team strength: offensive (30%), defensive (30%), points (40%)'
        )
        
        # 7. GOAL CONTRIBUTION DISTRIBUTION
        df_eng['goals_distribution_variance'] = (
            np.abs(df_eng['goals_scored'] - df_eng['goals_conceded']) / 
            (df_eng['goals_scored'] + df_eng['goals_conceded'] + 1)
        )
        self.new_features_info['goals_distribution_variance'] = (
            'Goal variance ratio (attacking vs defending balance)'
        )
        
        # 8. CONSISTENCY METRICS
        df_eng['performance_volatility'] = (
            np.abs(df_eng['goal_difference']) / (df_eng['goals_scored'] + 1)
        )
        self.new_features_info['performance_volatility'] = (
            'Performance volatility (GD relative to total goals)'
        )
        
        # 9. CHAMPIONSHIP LIKELIHOOD INDICATORS
        df_eng['championship_potential'] = (
            (df_eng['points_per_game'] / 3.0 * 0.5) +
            (df_eng['goal_conversion_efficiency'] * 0.25) +
            (df_eng['defensive_solidity'] * 0.25)
        )
        self.new_features_info['championship_potential'] = (
            'Championship potential score (PPG: 50%, efficiency: 25%, defense: 25%)'
        )
        
        # 10. PROJECTED STANDINGS
        df_eng['projected_upper_tier'] = (
            (df_eng['projected_final_points'] >= 75).astype(int)
        )
        self.new_features_info['projected_upper_tier'] = (
            'Binary: 1 if projected points >= 75 (upper tier), 0 otherwise'
        )
        
        print(f"Generated {len([k for k in self.new_features_info.keys() if 'league' not in str(k).lower()])} new league features")
        return df_eng
    
    def remove_highly_correlated_features(self, df, original_cols):
        """
        Remove features with correlation > threshold.
        Keep original columns, remove only new engineered features.
        """
        new_cols = [col for col in df.columns if col not in original_cols]
        
        if len(new_cols) == 0:
            return df, []
        
        df_new_features = df[new_cols].copy()
        
        # Calculate correlation matrix
        corr_matrix = df_new_features.corr().abs()
        
        # Find upper triangle
        upper = corr_matrix.where(
            np.triu(np.ones(corr_matrix.shape), k=1).astype(bool)
        )
        
        # Find features with correlation greater than threshold
        to_drop = [
            column for column in upper.columns 
            if any(upper[column] > self.correlation_threshold)
        ]
        
        self.removed_features = to_drop
        df_filtered = df.drop(columns=to_drop)
        
        print(f"Removed {len(to_drop)} highly correlated features: {to_drop}")
        
        return df_filtered, to_drop
    
    def generate_feature_report(self, output_path=None):
        """
        Generate a comprehensive feature engineering report.
        """
        report = "FEATURE ENGINEERING REPORT\n"
        report += "=" * 80 + "\n\n"
        
        report += f"Total New Features Generated: {len(self.new_features_info)}\n"
        report += f"Features Removed (High Correlation): {len(self.removed_features)}\n"
        report += f"Final New Features: {len(self.new_features_info) - len(self.removed_features)}\n\n"
        
        report += "NEW FEATURES DOCUMENTATION:\n"
        report += "-" * 80 + "\n"
        
        for i, (feature_name, description) in enumerate(self.new_features_info.items(), 1):
            if feature_name not in self.removed_features:
                report += f"{i}. {feature_name}\n"
                report += f"   Description: {description}\n\n"
        
        report += "\nREMOVED FEATURES (High Correlation):\n"
        report += "-" * 80 + "\n"
        for removed_feat in self.removed_features:
            report += f"- {removed_feat}\n"
        
        if output_path:
            with open(output_path, 'w') as f:
                f.write(report)
            print(f"Report saved to {output_path}")
        
        return report


def main():
    print("ScoreSight Advanced Feature Engineering")
    print("=" * 80)
    
    # Load datasets
    print("\nLoading datasets...")
    match_df = pd.read_csv('data/final/data_final_match_prediction.csv')
    player_df = pd.read_csv('data/final/data_final_top_scorer.csv')
    league_df = pd.read_csv('data/final/data_final_points_tally.csv')
    
    print(f"Match dataset shape: {match_df.shape}")
    print(f"Player dataset shape: {player_df.shape}")
    print(f"League dataset shape: {league_df.shape}")
    
    # Initialize feature engineering
    fe = AdvancedFeatureEngineering(correlation_threshold=0.95)
    
    # Store original columns
    match_orig_cols = match_df.columns.tolist()
    player_orig_cols = player_df.columns.tolist()
    league_orig_cols = league_df.columns.tolist()
    
    # Generate features
    print("\n" + "=" * 80)
    print("GENERATING ENGINEERED FEATURES")
    print("=" * 80 + "\n")
    
    match_engineered = fe.engineer_match_features(match_df)
    player_engineered = fe.engineer_player_features(player_df)
    league_engineered = fe.engineer_league_features(league_df)
    
    # Remove highly correlated features
    print("\n" + "=" * 80)
    print("REMOVING HIGHLY CORRELATED FEATURES")
    print("=" * 80 + "\n")
    
    match_final, match_removed = fe.remove_highly_correlated_features(
        match_engineered, match_orig_cols
    )
    player_final, player_removed = fe.remove_highly_correlated_features(
        player_engineered, player_orig_cols
    )
    league_final, league_removed = fe.remove_highly_correlated_features(
        league_engineered, league_orig_cols
    )
    
    # Save engineered datasets
    print("\n" + "=" * 80)
    print("SAVING ENGINEERED DATASETS")
    print("=" * 80 + "\n")
    
    match_final.to_csv('data/engineered/data_engineered_match_prediction.csv', index=False)
    player_final.to_csv('data/engineered/data_engineered_top_scorer.csv', index=False)
    league_final.to_csv('data/engineered/data_engineered_league_points.csv', index=False)
    
    print(f"Match dataset saved: {match_final.shape}")
    print(f"Player dataset saved: {player_final.shape}")
    print(f"League dataset saved: {league_final.shape}")
    
    # Generate report
    print("\n" + "=" * 80)
    print("GENERATING FEATURE ENGINEERING REPORT")
    print("=" * 80 + "\n")
    
    report = fe.generate_feature_report('docs/FEATURE_ENGINEERING_REPORT.txt')
    print(report)
    
    # Summary statistics
    print("\n" + "=" * 80)
    print("SUMMARY STATISTICS")
    print("=" * 80)
    print(f"\nMatch Prediction Dataset:")
    print(f"  Original features: {len(match_orig_cols)}")
    print(f"  New features generated: {len(match_engineered.columns) - len(match_orig_cols)}")
    print(f"  Features removed: {len(match_removed)}")
    print(f"  Final features: {len(match_final.columns)}")
    
    print(f"\nTop Scorer Dataset:")
    print(f"  Original features: {len(player_orig_cols)}")
    print(f"  New features generated: {len(player_engineered.columns) - len(player_orig_cols)}")
    print(f"  Features removed: {len(player_removed)}")
    print(f"  Final features: {len(player_final.columns)}")
    
    print(f"\nLeague Points Dataset:")
    print(f"  Original features: {len(league_orig_cols)}")
    print(f"  New features generated: {len(league_engineered.columns) - len(league_orig_cols)}")
    print(f"  Features removed: {len(league_removed)}")
    print(f"  Final features: {len(league_final.columns)}")
    
    print("\n" + "=" * 80)
    print("Feature engineering complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
