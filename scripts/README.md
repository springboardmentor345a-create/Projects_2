# Scripts

Python Automation Scripts

This directory contains Python scripts for data processing and model preparation.

## Available Scripts

1. **execute_notebooks.py**
   - Executes all Jupyter notebooks sequentially
   - Ensures proper pipeline execution order
   - Usage: python execute_notebooks.py

2. **validate_data.py**
   - Validates data quality across all datasets
   - Checks for missing values, duplicates, data types
   - Usage: python validate_data.py

3. **drop_unnecessary_columns.py**
   - Removes redundant and unnecessary columns
   - Optimizes dataset size
   - Usage: python drop_unnecessary_columns.py

4. **analyze_dropped_columns.py**
   - Analyzes dropped columns and reasons
   - Generates detailed analysis report
   - Usage: python analyze_dropped_columns.py

5. **data_quality_check.py**
   - Performs comprehensive data quality assessment
   - Usage: python data_quality_check.py

6. **generate_visualizations.py**
   - Creates visualizations from datasets
   - Outputs PNG files to visualizations/
   - Usage: python generate_visualizations.py

7. **advanced_feature_engineering.py**
   - Generates advanced engineered features
   - Creates ~70 new features across datasets
   - Removes highly correlated features
   - Generates feature documentation
   - Usage: python advanced_feature_engineering.py

## Feature Engineering Script Details

Generates features for three datasets:

**Match Prediction Features (36 new):**
- Interaction features (home vs away comparisons)
- Ratio/percentage features (performance metrics)
- Polynomial features (non-linear relationships)
- Team strength indices (composite metrics)
- Home advantage indicators
- Momentum features (streaks)
- Temporal features (season progression)
- Dominance scores

**Top Scorer Features (25 new):**
- Efficiency metrics (goals/assists per match)
- Scoring consistency
- Age-performance interactions
- Experience-weighted metrics
- Expected vs actual performance gaps
- Composite scoring threat index
- Match availability

**League Points Features (22 new):**
- Performance consistency
- Competitive balance
- Offensive/defensive balance
- Goal difference analysis
- Performance tier classifications
- Championship likelihood indicators

## Output Files

Engineered Datasets:
- data/engineered/data_engineered_match_prediction.csv
- data/engineered/data_engineered_top_scorer.csv
- data/engineered/data_engineered_league_points.csv

Documentation:
- docs/FEATURE_ENGINEERING_REPORT.txt (feature descriptions)
- docs/FEATURE_ENGINEERING_GUIDE.txt (detailed guide)

## Requirements

- pandas
- numpy
- scikit-learn
- matplotlib
- seaborn

## Execution Order

For first-time setup:
1. python execute_notebooks.py
2. python advanced_feature_engineering.py
3. python validate_data.py
4. python generate_visualizations.py
