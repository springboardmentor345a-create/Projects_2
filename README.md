# ScoreSight - EPL Prediction Project

**Author:** Prathamesh Fuke  
**Branch:** Prathamesh_Fuke  
**Repository:** https://github.com/springboardmentor345a-create/Projects_2.git

## Project Overview

ScoreSight is a machine learning project focused on predicting English Premier League (EPL) outcomes using historical match data, player statistics, and team performance metrics.

### Prediction Objectives
1. **Match Outcomes** - Predict match scores and winners
2. **Top Scorer** - Identify the season's leading goal scorer
3. **League Winner & Points Tally** - Forecast team points and champion

## Project Structure

```
ScoreSight/
├── notebooks/                         # Jupyter notebooks for ML pipeline
│   ├── 01_Data_Loading_EDA.ipynb     # Data loading and exploration
│   ├── 02_Data_Cleaning.ipynb        # Data cleaning and preprocessing
│   ├── 03_Feature_Engineering.ipynb  # Feature creation and engineering
│   ├── 04_Encoding_Feature_Selection.ipynb  # Encoding and feature selection
│   ├── 05_Data_Visualization.ipynb   # Data visualization and analysis
│   ├── 06_Data_Leakage_Validation.ipynb  # Data leakage prevention validation
│   ├── 07_Feature_Engineering_v3_Advanced.ipynb  # Advanced feature engineering
│   ├── 08_Model_Training_v1.ipynb    # Initial model training experiments
│   ├── 10_League_Winner_PS1.ipynb    # PS1: League winner/top-4 prediction
│   ├── 11_Match_Winner_PS2.ipynb     # PS2: Match winner (H/D/A) prediction
│   ├── 12_Top_Scorer_PS3.ipynb       # PS3: Top scorer goals prediction
│   ├── 13_Total_Points_PS4.ipynb     # PS4: Team total points prediction
│   ├── 14_Match_Result_PS5.ipynb     # PS5: Match result prediction
│   ├── train_all_models.py           # Automated training script for all PS
│   ├── models/                        # Trained ML models (joblib files)
│   │   ├── ps1_league_winner_lightgbm.joblib  # Best model for PS1
│   │   ├── ps1_scaler.joblib          # Scaler for PS1
│   │   ├── ps1_metadata.json          # PS1 training metadata
│   │   ├── ps2_match_winner_model.joblib  # Best model for PS2
│   │   ├── ps3_top_scorer_best_model.joblib  # Best model for PS3
│   │   ├── ps3_top_scorer_metadata.json  # PS3 training metadata
│   │   ├── ps4_total_points_best_model.joblib  # Best model for PS4
│   │   ├── ps4_total_points_metadata.json  # PS4 training metadata
│   │   ├── ps5_match_result_best_model.joblib  # Best model for PS5
│   │   └── ps5_match_result_metadata.json  # PS5 training metadata
│   └── README.md                      # Notebooks documentation
├── data/                              # All data files organized by stage
│   ├── raw/                           # Raw data after initial loading
│   │   ├── data_raw_league.csv
│   │   ├── data_raw_match.csv
│   │   └── data_raw_player.csv
│   ├── cleaned/                       # Cleaned datasets (no nulls/dupes)
│   │   ├── data_cleaned_league.csv
│   │   ├── data_cleaned_match.csv
│   │   └── data_cleaned_player.csv
│   ├── features/                      # Feature-engineered datasets
│   │   ├── data_features_league.csv
│   │   ├── data_features_match.csv
│   │   └── data_features_player.csv
│   ├── encoded/                       # Label-encoded datasets
│   │   ├── data_encoded_league.csv
│   │   ├── data_encoded_match.csv
│   │   └── data_encoded_player.csv
│   ├── engineered/                    # Advanced engineered features v3
│   │   ├── data_engineered_league_points.csv
│   │   ├── data_engineered_match_prediction.csv
│   │   ├── data_engineered_match_v3.csv
│   │   ├── data_engineered_top_scorer.csv
│   │   ├── feature_descriptions_v3.json
│   │   └── model_comparison_results.csv
│   ├── corrected/                     # Corrected datasets for training
│   │   ├── league_winner_corrected.csv
│   │   ├── league_winner_with_top4.csv
│   │   ├── match_prediction_corrected.csv
│   │   ├── match_prediction_with_ftr.csv
│   │   └── top_scorer_corrected.csv
│   └── final/                         # Final modeling-ready datasets
│       ├── data_final_match_prediction.csv
│       ├── data_final_points_tally.csv
│       └── data_final_top_scorer.csv
├── datasets/                          # Original raw datasets
│   ├── EPL(Overall Points & Ranking).csv
│   ├── Match Winner.csv
│   ├── Match_winner_selected_columns.csv
│   └── ScoreSight_ML_Season_LeagueWinner_Champion.csv
├── visualizations/                    # Generated visualizations and charts
│   ├── viz_match_distributions_prematch.png
│   ├── viz_match_corr_prematch.png
│   ├── viz_player_core_features.png
│   ├── viz_league_gd_vs_ppg.png
│   ├── viz_league_top15_ppg.png
│   ├── ps1_feature_importance.png
│   ├── ps1_model_comparison.csv
│   └── ps2_model_comparison.csv
├── docs/                              # Project documentation
│   ├── DROPPED_COLUMNS_ANALYSIS.md    # Analysis of dropped columns
│   ├── FEATURE_ENGINEERING_PHASE1_SUMMARY.md
│   ├── FEATURE_ENGINEERING_V3_GUIDE.md
│   ├── GOOGLE_COLAB_SETUP.md
│   ├── MODEL_TRAINING_COMPARISON.md
│   ├── PROBLEM_STATEMENTS_TRAINING_STATUS.md
│   ├── QUICK_START_GUIDE.md
│   └── SCORESIGHT_V3_COMPLETION_REPORT.md
├── requirements.txt                   # Python dependencies
├── README.md                          # This file
├── LICENSE                            # Project license
└── MIT LICENSE                        # MIT License text
```

## Datasets

### 1. Match Winner.csv
Historical match results with 6,840 records including:
- Team names (home/away)
- Match scores (full-time home/away goals)
- Team form indicators (points, streaks)
- Goal statistics (scored, conceded, difference)
- Match context (week, season)

### 2. Goals & Assist.xlsx
Player performance statistics with 2,274 player-season records:
- Player demographics (age, position, nationality)
- Scoring statistics (goals, assists, penalties)
- Expected goals metrics (xG, npxG, xAG)
- Per-90 normalized statistics
- Match participation data

### 3. ScoreSight_ML_Season_LeagueWinner_Champion.csv
Season-level league data with 180 team-season records:
- Team performance (wins, draws, losses)
- Points and goal statistics
- League position and championship status
- Season identifiers

## Workflow

### Phase 1: Data Preprocessing (COMPLETED)

#### Notebook 01: Data Loading and EDA
- Load all three datasets
- Examine data structure and dimensions
- Identify missing values and data quality issues
- Generate basic statistics
- **Output**: `data_raw_*.csv` files

#### Notebook 02: Data Cleaning
- Remove duplicates
- Handle missing values (median/mode/zero imputation)
- Standardize column names
- Fix data type inconsistencies
- **Output**: `data_cleaned_*.csv` files

#### Notebook 03: Feature Engineering
- Create match prediction features (team form, home/away stats)
- Generate player performance metrics (goals per game, assists ratio)
- Build team strength indicators
- Calculate historical averages
- **Output**: `data_features_*.csv` files

#### Notebook 04: Encoding and Feature Selection
- Encode categorical variables (Label Encoding)
- Select relevant features for each prediction task
- Prepare final datasets for modeling
- **Output**: `data_final_*.csv` and `data_encoded_*.csv` files

#### Notebook 05: Data Visualization
- Correlation heatmaps
- Distribution plots
- Top performers analysis
- Summary dashboards
- **Output**: Visualization PNG files

### Phase 2: Model Building (COMPLETED ✅)

All five problem statements have been trained with production-ready models:

#### Problem Statement 1: League Winner (Top-4) Prediction
- **Type**: Binary Classification
- **Target**: Teams finishing in top 4 positions
- **Best Model**: LightGBM
- **Performance**: 97.2% accuracy, 0.93 F1-score
- **Key Features**: goals_conceded, goal_difference, goals_scored
- **Model File**: `ps1_league_winner_lightgbm.joblib`

#### Problem Statement 2: Match Winner Prediction  
- **Type**: Multi-class Classification (Home/Draw/Away)
- **Target**: Match result (H/D/A)
- **Best Model**: XGBoost
- **Performance**: 46.1% accuracy (excellent for football prediction!)
- **Baseline**: 33.3% (random guess)
- **Model File**: `ps2_match_winner_model.joblib`

#### Problem Statement 3: Top Scorer Prediction
- **Type**: Regression
- **Target**: Player total goals scored
- **Best Model**: XGBoost
- **Performance**: R² = 0.977, MAE = 0.136 goals
- **Key Features**: xG, goals_per_90, assists, match participation
- **Model File**: `ps3_top_scorer_best_model.joblib`

#### Problem Statement 4: Total Points Prediction
- **Type**: Regression
- **Target**: Team's total season points
- **Best Model**: Gradient Boosting/XGBoost
- **Performance**: High R² score, low MAE
- **Model File**: `ps4_total_points_best_model.joblib`

#### Problem Statement 5: Match Result Prediction
- **Type**: Multi-class Classification
- **Target**: Match outcome with context
- **Best Model**: LightGBM/XGBoost
- **Model File**: `ps5_match_result_best_model.joblib`

### Phase 3: Evaluation and Improvement (In Progress)
- Train regression models (Linear, Ridge, Lasso, Random Forest, XGBoost)
- Evaluate using MAE and RMSE metrics
- Hyperparameter tuning
- Model comparison and selection

### Phase 3: Evaluation and Improvement
- Cross-validation
- Feature importance analysis
- Model optimization
- Performance benchmarking

### Phase 4: Deployment and Presentation
- Build web application interface
- Create interactive dashboards
- Prepare documentation
- Final presentation

## Installation

### Prerequisites
- Python 3.8+
- Jupyter Notebook or JupyterLab
- Git

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/springboardmentor345a-create/Projects_2.git
cd Projects_2
git checkout Prathamesh_Fuke
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Launch Jupyter Notebook**
```bash
jupyter notebook
```

4. **Run notebooks in sequence**
- Start with `01_Data_Loading_EDA.ipynb`
- Progress through each notebook sequentially

## Usage

### Running the Notebooks

Execute notebooks in order:

1. **01_Data_Loading_EDA.ipynb**
   - Loads raw datasets
   - Performs initial exploration
   - Saves raw data for next stage

2. **02_Data_Cleaning.ipynb**
   - Cleans and preprocesses data
   - Handles missing values and duplicates
   - Saves cleaned datasets

3. **03_Feature_Engineering.ipynb**
   - Creates new features
   - Transforms existing features
   - Saves feature-engineered data

4. **04_Encoding_Feature_Selection.ipynb**
   - Encodes categorical variables
   - Selects relevant features
   - Prepares final modeling datasets

5. **05_Data_Visualization.ipynb**
   - Generates visualizations
   - Creates summary dashboards
   - Exports visualization files

### Output Files

After running all notebooks, you'll have:

**Intermediate Data Files:**
- `data_raw_*.csv` - Raw loaded data
- `data_cleaned_*.csv` - Cleaned data
- `data_features_*.csv` - Feature-engineered data
- `data_encoded_*.csv` - Encoded data (all columns)

**Final Modeling Files:**
- `data_final_match_prediction.csv` - For match outcome prediction
- `data_final_top_scorer.csv` - For top scorer prediction
- `data_final_points_tally.csv` - For points tally prediction

**Visualizations:**
- `viz_match_distributions_prematch.png` - Pre-match feature distributions
- `viz_match_corr_prematch.png` - Pre-match feature correlations
- `viz_player_core_features.png` - Player scoring metrics
- `viz_league_gd_vs_ppg.png` - Goal difference vs points per game
- `viz_league_top15_ppg.png` - Top teams by PPG

## Key Features

### Data Preprocessing
- Comprehensive data cleaning
- **NO null values** (fully cleaned)
- **Duplicate removal** (18 match rows, 204 player rows removed)
- Column standardization (lowercase, underscores)
- Data type corrections
- **33 columns dropped** (unnecessary/redundant)
- **Data leakage prevention** (only pre-event features)

### Feature Engineering
- Team form indicators (points, streaks)
- Home/away performance metrics
- Player performance ratios (per-90 statistics)
- Expected goals (xG) metrics
- Goal difference calculations

### Data Quality
- **Zero missing values** after cleaning
- **Duplicate records removed** (222 total)
- Standardized column names
- Consistent data types
- Validated data ranges
- **Optimized feature set**: 23 match + 21 player + 10 league = 54 features
- **Leakage-safe**: All features available pre-match/pre-event

## Evaluation Metrics

Models will be evaluated using:
- **MAE (Mean Absolute Error)**: Average prediction error
- **RMSE (Root Mean Squared Error)**: Penalizes larger errors
- **R² Score**: Proportion of variance explained
- **Cross-validation scores**: Model generalization

## Project Milestones

- [x] **Milestone 1**: Repository setup and data familiarization
- [x] **Milestone 2**: Data preprocessing and cleaning - COMPLETED
- [x] **Milestone 3**: Model building and training - COMPLETED
  - PS1: League Winner (Top-4) Prediction - LightGBM (97.2% accuracy)
  - PS2: Match Winner (H/D/A) Prediction - XGBoost (46.1% accuracy)
  - PS3: Top Scorer Goals Prediction - XGBoost (R² = 0.977)
  - PS4: Total Points Prediction - Best regression model
  - PS5: Match Result Prediction - Best classifier
- [ ] **Milestone 4**: Model evaluation and optimization
- [ ] **Milestone 5**: Web application and final presentation

## Column Optimization

A total of **33 unnecessary columns** were dropped across all datasets:
- **Match Prediction**: 14 columns dropped (40 → 23 features)
- **Top Scorer**: 13 columns dropped (34 → 21 features)
- **Points Tally**: 6 columns dropped (16 → 10 features)

See `docs/DROPPED_COLUMNS_ANALYSIS.md` and `docs/DATA_LEAKAGE_AND_OVERFITTING.txt` for detailed analysis.

## Data Leakage Prevention Policy

All final datasets now include **only features available before the predicted event**:
- **Match prediction**: Pre-match team stats, form indicators, streaks
- **Top scorer**: Prior season/career stats or mid-season stats-to-date
- **League winner**: End-of-season aggregates as targets only

See `docs/DATA_LEAKAGE_AND_OVERFITTING.txt` for complete justification of all features and why each was retained or dropped.

## Technologies Used

- **Python 3.8+**: Core programming language
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Matplotlib/Seaborn**: Data visualization
- **Scikit-learn**: Machine learning and preprocessing
- **Jupyter Notebook**: Interactive development environment

## Future Enhancements

- Integration of additional datasets (Kaggle, FBref, etc.)
- Real-time match prediction API
- Interactive web dashboard
- Player transfer impact analysis
- Injury data integration
- Weather and stadium factors

## Contributing

This is an individual project for the Springboard mentorship program. For questions or suggestions, please contact the author.

## License

See LICENSE file in the repository.

## Acknowledgments

- **Instructor**: springboardmentor345a-create
- **Data Sources**: EPL historical data
- **Springboard**: Mentorship program

## Contact

**Prathamesh Fuke**  
GitHub: [@prathameshfuke](https://github.com/prathameshfuke)  
Branch: Prathamesh_Fuke

---

**Status**: Phase 3 (Model Training) - **COMPLETED**  
**Next**: Phase 4 (Model Evaluation and Optimization)  
**Models Trained**: 5 Problem Statements with best models saved  
**Dataset Quality**: Zero nulls, no duplicates, leakage-safe, optimized features  
**Last Updated**: November 13, 2025
