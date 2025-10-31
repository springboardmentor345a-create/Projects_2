import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

OUTPUT_DIR = os.path.join('visualizations')
os.makedirs(OUTPUT_DIR, exist_ok=True)

sns.set(style='whitegrid')


def savefig(path: str):
	plt.tight_layout()
	plt.savefig(path, dpi=150)
	plt.close()


def load_data():
	match_path = os.path.join('data', 'final', 'data_final_match_prediction.csv')
	player_path = os.path.join('data', 'final', 'data_final_top_scorer.csv')
	league_path = os.path.join('data', 'final', 'data_final_points_tally.csv')
	match_df = pd.read_csv(match_path)
	player_df = pd.read_csv(player_path)
	league_df = pd.read_csv(league_path)
	return match_df, player_df, league_df


def plot_match_distributions(match_df: pd.DataFrame):
	# Plot a few core pre-match numeric features
	features = [
		'htp', 'atp', 'htgd', 'atgd', 'diffpts', 'diffformpts', 'htformpts', 'atformpts'
	]
	features = [f for f in features if f in match_df.columns]
	if not features:
		return

	n = len(features)
	cols = 4
	rows = (n + cols - 1) // cols
	plt.figure(figsize=(4 * cols, 3 * rows))
	for i, col in enumerate(features, 1):
		plt.subplot(rows, cols, i)
		sns.histplot(match_df[col], kde=True, bins=30, color='#2b8cbe')
		plt.title(col)
		plt.xlabel('value')
		plt.ylabel('count')
	savefig(os.path.join(OUTPUT_DIR, 'viz_match_distributions_prematch.png'))


def plot_match_correlation(match_df: pd.DataFrame):
	# Correlation of pre-match numeric features
	numeric_cols = match_df.select_dtypes(include=['number']).columns.tolist()
	# Exclude encoded team ids for clearer heatmap if present
	exclude = {'hometeam_encoded', 'awayteam_encoded'}
	numeric_cols = [c for c in numeric_cols if c not in exclude]
	if len(numeric_cols) < 2:
		return
	corr = match_df[numeric_cols].corr().clip(-1, 1)
	plt.figure(figsize=(10, 8))
	sns.heatmap(corr, cmap='vlag', center=0, square=False, cbar_kws={'shrink': .8})
	plt.title('Match (Pre-Match Features) Correlation Heatmap')
	savefig(os.path.join(OUTPUT_DIR, 'viz_match_corr_prematch.png'))


def plot_player_core_features(player_df: pd.DataFrame):
	# Show distributions for key scoring features (note: usage policy depends on timing)
	features = [
		'goals', 'assists', 'non_penalty_goals', 'xg', 'npxg', 'xag'
	]
	features = [f for f in features if f in player_df.columns]
	if not features:
		return
	plt.figure(figsize=(16, 9))
	for i, col in enumerate(features, 1):
		plt.subplot(2, 3, i)
		sns.boxplot(x=player_df[col], color='#74a9cf')
		plt.title(col)
	plt.suptitle('Player Scoring/Expected Metrics (see usage policy to avoid leakage)', y=1.02)
	savefig(os.path.join(OUTPUT_DIR, 'viz_player_core_features.png'))


def plot_league_relationships(league_df: pd.DataFrame):
	# Scatter: goal_difference vs points_per_game colored by champion
	if not {'goal_difference', 'points_per_game', 'target_champion'}.issubset(league_df.columns):
		return
	plt.figure(figsize=(7, 5))
	sns.scatterplot(
		data=league_df,
		x='goal_difference', y='points_per_game',
		hue='target_champion', palette={0: '#2b8cbe', 1: '#de2d26'}, alpha=0.8
	)
	plt.title('League: Goal Difference vs Points Per Game')
	savefig(os.path.join(OUTPUT_DIR, 'viz_league_gd_vs_ppg.png'))

	# Bar: average PPG by team (top 15 for readability)
	if not {'team_encoded', 'points_per_game'}.issubset(league_df.columns):
		return
	ppg_by_team = league_df.groupby('team_encoded')['points_per_game'].mean().sort_values(ascending=False).head(15)
	plt.figure(figsize=(10, 5))
	sns.barplot(x=ppg_by_team.index.astype(str), y=ppg_by_team.values, color='#2ca25f')
	plt.title('League: Top-15 Teams by Average Points Per Game')
	plt.xlabel('team_encoded')
	plt.ylabel('avg points_per_game')
	savefig(os.path.join(OUTPUT_DIR, 'viz_league_top15_ppg.png'))


def main():
	match_df, player_df, league_df = load_data()
	# Generate plots based on updated, leakage-free datasets
	plot_match_distributions(match_df)
	plot_match_correlation(match_df)
	plot_player_core_features(player_df)
	plot_league_relationships(league_df)
	print(f"Visualizations saved to: {OUTPUT_DIR}")


if __name__ == '__main__':
	main()
