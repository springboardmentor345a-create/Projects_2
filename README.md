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
├── notebooks/                         # Jupyter notebooks
│   ├── 01_Data_Loading_EDA.ipynb
│   ├── 02_Data_Cleaning.ipynb
│   ├── 03_Feature_Engineering.ipynb
│   ├── 04_Encoding_Feature_Selection.ipynb
│   └── 05_Data_Visualization.ipynb
├── data/                              # All data files
│   ├── raw/                           # Raw data after loading
│   ├── cleaned/                       # Cleaned datasets
│   ├── features/                      # Feature-engineered data
│   ├── encoded/                       # Encoded datasets
│   └── final/                         # Final modeling datasets
├── datasets/                          # Original datasets
│   ├── Match Winner.csv
│   ├── Goals & Assist.xlsx
│   └── ScoreSight_ML_Season_LeagueWinner_Champion.csv
├── visualizations/                    # Generated visualizations
│   ├── viz_match_correlation.png
│   ├── viz_match_distributions.png
│   ├── viz_player_correlation.png
│   ├── viz_top_scorers.png
│   ├── viz_league_statistics.png
│   └── viz_summary_dashboard.png
├── scripts/                           # Python automation scripts
│   ├── execute_notebooks.py
│   └── validate_data.py
├── docs/                              # Documentation
│   ├── PREPROCESSING_SUMMARY.md
│   ├── PROJECT_STATUS.md
│   ├── QUICK_START_GUIDE.md
│   ├── EXECUTION_REPORT.md
│   └── AI_ScoreSight Doc.pdf
├── requirements.txt                   # Python dependencies
├── README.md                          # This file
├── LICENSE                            # License file
└── MIT LICENSE                        # MIT License
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

### Phase 1: Data Preprocessing (Current)

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

### Phase 2: Model Building (Next)
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
- `viz_match_correlation.png`
- `viz_match_distributions.png`
- `viz_player_correlation.png`
- `viz_top_scorers.png`
- `viz_league_statistics.png`
- `viz_summary_dashboard.png`

## Key Features

### Data Preprocessing
- Comprehensive data cleaning
- Missing value imputation (median/mode/zero)
- Duplicate removal
- Column standardization (lowercase, underscores)
- Data type corrections
- Unnecessary column removal (33 columns dropped)

### Feature Engineering
- Team form indicators (points, streaks)
- Home/away performance metrics
- Player performance ratios (per-90 statistics)
- Expected goals (xG) metrics
- Goal difference calculations

### Data Quality
- Zero missing values after cleaning
- No duplicate records
- Standardized column names
- Consistent data types
- Validated data ranges
- Optimized feature set (57 final features)

## Evaluation Metrics

Models will be evaluated using:
- **MAE (Mean Absolute Error)**: Average prediction error
- **RMSE (Root Mean Squared Error)**: Penalizes larger errors
- **R² Score**: Proportion of variance explained
- **Cross-validation scores**: Model generalization

## Project Milestones

- [x] **Milestone 1**: Repository setup and data familiarization
- [x] **Milestone 2**: Data preprocessing and cleaning - COMPLETED
- [ ] **Milestone 3**: Model building and evaluation
- [ ] **Milestone 4**: Web application and final presentation

## Column Optimization

A total of 33 unnecessary columns were dropped across all datasets:
- **Match Prediction**: 14 columns dropped (40 to 26 features)
- **Top Scorer**: 13 columns dropped (34 to 21 features)
- **Points Tally**: 6 columns dropped (16 to 10 features)

See `docs/DROPPED_COLUMNS_ANALYSIS.md` for detailed analysis.

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

**Status**: Phase 1 (Data Preprocessing) - COMPLETED  
**Next**: Phase 2 (Model Building)  
**Last Updated**: October 30, 2025
