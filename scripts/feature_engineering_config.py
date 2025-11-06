"""
ScoreSight Feature Engineering v3.0 - Configuration Parameters

This file documents all tunable parameters in the feature engineering pipeline.
Modify these values to customize feature generation.

Author: Prathamesh Fuke
Version: 3.0
Last Updated: November 2025
"""

# ============================================================================
# TIER 1: STATISTICAL & DISTRIBUTIONAL FEATURES
# ============================================================================

# Window Size for Rolling Statistics
# Controls how many past games to use when calculating statistics
TIER1_ROLLING_WINDOW = 10
# Suggested values:
#   5  = Very responsive to recent form (high noise)
#   7  = Default - balanced response
#   10 = More stable (less noise)
#   15 = Very stable but less responsive

# Minimum observations for rolling window
# Prevents features from being calculated with too few data points
TIER1_MIN_PERIODS = 3
# Suggested values:
#   2  = More data but noisier estimates
#   3  = Default - requires 3 games minimum
#   5  = More stable, less early-season data

# Z-score threshold for anomaly detection
# Higher values = fewer anomalies detected
TIER1_ZSCORE_THRESHOLD = 2.0
# Suggested values:
#   1.5 = Aggressive (detect more anomalies)
#   2.0 = Default (±2σ = ~5% outliers)
#   2.5 = Conservative (fewer false positives)

# Percentile-of-score method
# Method for calculating percentiles
TIER1_PERCENTILE_METHOD = 'linear'
# Suggested values:
#   'linear' = Default, interpolates between ranks
#   'nearest' = Uses nearest rank (more discrete)
#   'lower' = Always rounds down

# ============================================================================
# TIER 2: MARKET & EXTERNAL CONTEXT FEATURES
# ============================================================================

# Team Quality Tier Thresholds
# Percentage of teams in each tier
TIER2_ELITE_THRESHOLD = 0.30      # Top 30% = Elite (Tier 1)
TIER2_MIDTABLE_THRESHOLD = 0.60   # Top 30-60% = Mid (Tier 2)
# Bottom 40% = Struggling (Tier 3)
# Suggested thresholds:
#   0.25, 0.50 = More polarized (fewer mid-table teams)
#   0.30, 0.60 = Default (balanced distribution)
#   0.35, 0.70 = Compressed (more teams in mid-table)

# Rest Advantage Calculation
# Default assumes 7-day rest between matches
TIER2_STANDARD_REST_DAYS = 7
# Suggested values:
#   5  = More aggressive on rest-related features
#   7  = Default (standard EPL 1-week cycle)
#   10 = Less sensitive to rest variations

# Midweek Fixture Definition
# Days of week considered "midweek" (0=Monday, 6=Sunday)
TIER2_MIDWEEK_DAYS = [0, 1, 2, 3]  # Monday-Thursday
# Suggested values:
#   [0, 1, 2, 3]     = Default (Mon-Thu)
#   [0, 1, 2, 3, 4]  = Include Friday
#   [0, 1, 2, 3]     = Strict Mon-Thu only

# Winning Streak Window
# How many recent games for momentum calculation
TIER2_MOMENTUM_WINDOW = 5
# Suggested values:
#   3  = Very recent form (3-game window)
#   5  = Default (1-month window)
#   7  = Longer-term form (1.5 months)

# Momentum Decay Factor
# Controls how exponential winning momentum grows
# Higher = slower growth, more dampening
TIER2_MOMENTUM_DECAY_FACTOR = 50.0
# Formula: momentum = 1 - exp(-win_pct / decay_factor)
# Suggested values:
#   30  = Fast growth (high acceleration)
#   50  = Default (moderate growth)
#   100 = Slow growth (dampened)

# ============================================================================
# TIER 3: NON-LINEAR & INTERACTION FEATURES
# ============================================================================

# Polynomial Transform Degree
# Degree of polynomial transformations (sqrt=0.5, log=ln, sq=2)
TIER3_POLY_DEGREES = [0.5, 2, 3]  # sqrt, squared, cubic
# Suggested combinations:
#   [0.5]           = Only sqrt (dampening)
#   [0.5, 2]        = sqrt + squared (default)
#   [0.5, 2, 3]     = sqrt + squared + cubic (more features)

# Efficiency Ratio Smoothing
# Denominator smoothing to prevent division by zero
TIER3_EFFICIENCY_SMOOTHING = 1
# Suggested values:
#   0.1 = More sensitive (less smoothing)
#   1   = Default (standard smoothing)
#   2   = Heavy smoothing (compressed values)

# Composite Index Weights
# Weights for Dynamic Strength Index components
TIER3_STRENGTH_WEIGHTS = {
    'form': 0.35,          # Form points weight
    'offensive_eff': 0.25, # Offensive efficiency
    'defensive_eff': 0.20, # Defensive efficiency
    'consistency': 0.20    # Consistency metric
}
# Note: Must sum to 1.0
# Example alternatives:
# Offensive focus:   {'form': 0.25, 'offensive': 0.40, 'defensive': 0.15, 'consistency': 0.20}
# Defensive focus:   {'form': 0.25, 'offensive': 0.15, 'defensive': 0.40, 'consistency': 0.20}
# Balanced (equal):  {'form': 0.25, 'offensive': 0.25, 'defensive': 0.25, 'consistency': 0.25}

# Away Team Adjustment Factor
# How much to discount away team strength (away teams generally underperform)
TIER3_AWAY_ADJUSTMENT = 0.85
# Formula: away_adjusted = away_strength * away_adjustment
# Suggested values:
#   0.80 = Aggressive home advantage (away worth 20% less)
#   0.85 = Default (away worth 15% less)
#   0.90 = Modest home advantage (away worth 10% less)
#   1.00 = No home advantage adjustment

# MinMax Scaling Range
# Range for normalized features
TIER3_SCALE_MIN = 0
TIER3_SCALE_MAX = 1
# Suggested values:
#   (0, 1)    = Standard [0-1] range
#   (-1, 1)   = Centered around zero
#   (0, 100)  = Percentage scale

# ============================================================================
# GENERAL FEATURE ENGINEERING PARAMETERS
# ============================================================================

# Data Leakage Check
# When enabled, prints warning if future data might be used
ENABLE_LEAKAGE_CHECKING = True
# Suggested values:
#   True  = Enable checks (recommended)
#   False = Disable (faster execution)

# Missing Data Handling Strategy
# How to handle NaN values in rolling calculations
MISSING_DATA_STRATEGY = 'forward_fill'  # Options: 'forward_fill', 'zero', 'mean', 'drop'
# Suggested strategies:
#   'forward_fill' = Use last known value (default, maintains trend)
#   'zero'         = Replace with 0 (conservative estimate)
#   'mean'         = Use feature mean (statistical approach)
#   'drop'         = Remove rows with NaN (strictest)

# Outlier Detection Method
# How to identify and handle outliers
OUTLIER_DETECTION = 'zscore'  # Options: 'zscore', 'iqr', 'isolation_forest', 'none'
# Suggested methods:
#   'zscore'           = Z-score based (|z| > 3 is outlier)
#   'iqr'              = Interquartile range (Q1-1.5*IQR, Q3+1.5*IQR)
#   'isolation_forest' = Multivariate anomaly detection
#   'none'             = No outlier handling

# Random Seed for Reproducibility
RANDOM_STATE = 42
# Suggested values:
#   42  = Default (famous answer to everything)
#   123 = Alternative fixed seed
#   None = True randomness (non-reproducible)

# Verbosity Level for Logging
# 0 = Silent, 1 = Basic, 2 = Detailed, 3 = Debug
VERBOSITY = 1

# ============================================================================
# FEATURE QUALITY THRESHOLDS
# ============================================================================

# Maximum allowed correlation between features (multicollinearity)
# Features with correlation > this value will be flagged
MAX_FEATURE_CORRELATION = 0.90
# Suggested values:
#   0.80 = Strict (flag more pairs)
#   0.90 = Default (standard threshold)
#   0.95 = Lenient (allow more correlation)

# Minimum correlation with target variable
# Features with |correlation| < this value may be dropped
MIN_TARGET_CORRELATION = 0.05
# Suggested values:
#   0.01 = Keep almost everything
#   0.05 = Default (remove very weak predictors)
#   0.10 = Aggressive (keep only strong predictors)

# Maximum allowed missing data percentage
# Features with > this % missing will be flagged
MAX_MISSING_PERCENTAGE = 10.0  # Percent
# Suggested values:
#   5   = Strict (flag 5%+ missing)
#   10  = Default (flag 10%+ missing)
#   20  = Lenient (allow 20%+ missing)

# ============================================================================
# OUTPUT & STORAGE
# ============================================================================

# Output file paths
OUTPUT_DIR = 'data/engineered/'
OUTPUT_FILENAME_FEATURES = 'data_engineered_match_v3.csv'
OUTPUT_FILENAME_DESCRIPTIONS = 'feature_descriptions_v3.json'
OUTPUT_FILENAME_STATS = 'feature_statistics_v3.json'
OUTPUT_FILENAME_VISUALIZATION = 'tier1_3_feature_distributions.png'

# Save intermediate outputs
SAVE_TIER1_INTERMEDIATE = False  # Save after Tier 1
SAVE_TIER2_INTERMEDIATE = False  # Save after Tier 2
SAVE_FINAL_ONLY = True           # Save only final output

# Visualization options
PLOT_FEATURE_DISTRIBUTIONS = True
PLOT_CORRELATION_MATRIX = True
PLOT_TOP_CORRELATIONS = True
DPI_VISUALIZATION = 300  # Resolution (300 for high-quality)

# ============================================================================
# ADVANCED OPTIONS
# ============================================================================

# Feature Scaling Before Composite Indices
# Whether to normalize features before combining
USE_SCALER_FOR_COMPOSITES = True
# Suggested values:
#   True  = Normalize first (recommended, prevents bias)
#   False = Use raw values (features with larger ranges dominate)

# Isolation Forest Anomaly Detection Parameters
ISOLATION_FOREST_CONTAMINATION = 0.1  # Expected % of anomalies
ISOLATION_FOREST_SAMPLES = 256         # Number of samples per tree
# Suggested:
#   contamination=0.05 to 0.15 (5-15% anomalies)
#   samples=256 (standard, adjust for memory)

# Date Format
DATE_FORMAT = '%d/%m/%y'  # Matches data_features_match.csv format
# Suggested alternatives:
#   '%Y-%m-%d' = YYYY-MM-DD format
#   '%d/%m/%y' = DD/MM/YY format (current)

# ============================================================================
# FEATURE SELECTION THRESHOLDS (For Future Tiers)
# ============================================================================

# Statistical Test Alpha Level
STAT_TEST_ALPHA = 0.05  # 95% confidence level

# Variance Inflation Factor (VIF) Threshold
# Features with VIF > this value indicate multicollinearity
MAX_VIF_THRESHOLD = 10.0
# Suggested values:
#   5   = Strict (remove multicollinear features)
#   10  = Default (standard threshold)
#   20  = Lenient (allow more correlation)

# Mutual Information Score Percentile
# Keep features in top X% by mutual information
MI_PERCENTILE = 70  # Keep top 70%
# Suggested values:
#   50 = Keep top 50% (aggressive selection)
#   70 = Default (keep top 70%)
#   90 = Keep top 90% (lenient)

# ============================================================================
# USAGE EXAMPLES
# ============================================================================

# Example 1: Quick Form-Focused Setup
"""
TIER1_ROLLING_WINDOW = 5           # Responsive to recent form
TIER2_MOMENTUM_WINDOW = 3          # Very recent momentum
TIER2_MOMENTUM_DECAY_FACTOR = 30   # Fast growth
"""

# Example 2: Stable Long-Term Setup
"""
TIER1_ROLLING_WINDOW = 15          # Stable statistics
TIER2_MOMENTUM_WINDOW = 7          # Longer-term momentum
TIER2_MOMENTUM_DECAY_FACTOR = 100  # Slow growth
"""

# Example 3: Aggressive Home Advantage
"""
TIER3_AWAY_ADJUSTMENT = 0.80       # Away teams worth 20% less
TIER2_ELITE_THRESHOLD = 0.20       # Only top 20% are elite
"""

# Example 4: Conservative Feature Set
"""
TIER3_STRENGTH_WEIGHTS = {
    'form': 0.5,               # Double weight on form
    'offensive_eff': 0.15,
    'defensive_eff': 0.15,
    'consistency': 0.20
}
MAX_FEATURE_CORRELATION = 0.85     # Stricter multicollinearity check
"""

# ============================================================================
# QUICK REFERENCE TABLE
# ============================================================================

"""
TIER 1 PARAMETERS:
  Parameter                      | Default | Fast | Stable
  ROLLING_WINDOW                 | 10      | 5    | 15
  MIN_PERIODS                    | 3       | 2    | 5
  ZSCORE_THRESHOLD               | 2.0     | 1.5  | 2.5

TIER 2 PARAMETERS:
  Parameter                      | Default | Quick | Stable
  ELITE_THRESHOLD                | 0.30    | 0.25 | 0.35
  MOMENTUM_WINDOW                | 5       | 3    | 7
  MOMENTUM_DECAY_FACTOR          | 50.0    | 30.0 | 100.0
  AWAY_ADJUSTMENT                | 0.85    | 0.80 | 0.90

TIER 3 PARAMETERS:
  Parameter                      | Default | Fast | Stable
  SCALE_MIN/MAX                  | 0/1     | 0/100| -1/1
  STRENGTH_WEIGHTS               | Balanced| Form | Defense
                                 |         | Focus| Focus
"""

# ============================================================================
# IMPLEMENTATION NOTES
# ============================================================================

"""
To use custom parameters in notebook:

1. At top of notebook, import this file:
   from feature_engineering_config import *

2. Or manually set parameters:
   TIER1_ROLLING_WINDOW = 7
   TIER2_MOMENTUM_DECAY_FACTOR = 60

3. Pass to feature engineering classes:
   tier1 = Tier1FeatureEngineering(
       df,
       rolling_window=TIER1_ROLLING_WINDOW,
       min_periods=TIER1_MIN_PERIODS
   )

4. Verify parameters at start of notebook:
   print(f"Rolling window: {TIER1_ROLLING_WINDOW}")
   print(f"Away adjustment: {TIER3_AWAY_ADJUSTMENT}")
"""

# ============================================================================
