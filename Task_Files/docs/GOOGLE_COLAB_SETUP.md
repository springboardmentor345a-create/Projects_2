# ScoreSight ML - Google Colab Setup Guide

## Data Files to Export

### RECOMMENDED: Use Engineered Datasets (Best Performance)

These datasets have been feature-engineered and have **MORE FEATURES** for better model performance:

| # | Problem Statement | Engineered File | Rows | Features | Target |
|---|---|---|---|---|---|
| **1** | League Winner | `data_engineered_league_points.csv` | 181 | 22+ | League champion |
| **2** | Match Winner | `data_engineered_match_prediction.csv` | 6,823 | 56+ | `mw` (Match winner) |
| **3** | Top Scorer | `data_engineered_top_scorer.csv` | 2,071 | 44+ | `goals` |
| **4** | Total Points | `data_engineered_league_points.csv` | 181 | 22+ | `target_total_points` |
| **5** | Match Result | `match_prediction_corrected.csv` | ? | Various | Result (H/D/A) |

### ALTERNATIVE: Use Base/Corrected Datasets (If you need less features)

| # | Problem Statement | Base File | Rows | Features | Target |
|---|---|---|---|---|---|
| **1** | League Winner | `league_winner_corrected.csv` | ? | ~10 | League champion |
| **2** | Match Winner | `data_final_match_prediction.csv` | 6,822 | 23 | `mw` |
| **3** | Top Scorer | `data_final_top_scorer.csv` | 2,070 | 21 | `goals` |
| **4** | Total Points | `data_final_points_tally.csv` | 180 | 10 | `target_total_points` |
| **5** | Match Result | `match_prediction_corrected.csv` | ? | Various | Result |

---

## RECOMMENDED Export List (Engineered Datasets)

Export these 4 engineered files (they include more features):
1. ✅ `data/engineered/data_engineered_league_points.csv` (for PS1 & PS4)
2. ✅ `data/engineered/data_engineered_match_prediction.csv` (for PS2)
3. ✅ `data/engineered/data_engineered_top_scorer.csv` (for PS3)
4. ✅ `data/corrected/match_prediction_corrected.csv` (for PS5)

**Total size:** ~10-15 MB (lightweight)

---

## Google Colab Setup Instructions

### Step 1: Upload Data to Google Drive
1. Create a folder in Google Drive: `/ScoreSight_Data/`
2. Upload all 5 CSV files to this folder

### Step 2: Mount Google Drive in Colab
```python
from google.colab import drive
drive.mount('/content/drive')

# Set working directory
import os
os.chdir('/content/drive/MyDrive/ScoreSight')

# Verify files exist
!ls -lh data/
```

### Step 3: Install Required Libraries
```python
!pip install pandas numpy scikit-learn xgboost lightgbm matplotlib seaborn -q

import pandas as pd
import numpy as np
import json
import joblib
from pathlib import Path
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Create models folder if it doesn't exist
Path('models').mkdir(exist_ok=True)

# Verify installations
print("All libraries installed successfully!")
```

### Step 4: Load Individual CSV Files
```python
# ENGINEERED DATASETS (Recommended - More Features)

# PS1 & PS4: League Winner & Total Points (same dataset, different targets)
league_df = pd.read_csv('data/data_engineered_league_points.csv')
print(f"League Data: {league_df.shape}")
print(f"Columns: {list(league_df.columns)}")

# PS2: Match Winner
match_winner_df = pd.read_csv('data/data_engineered_match_prediction.csv')
print(f"Match Winner: {match_winner_df.shape}")

# PS3: Top Scorer
top_scorer_df = pd.read_csv('data/data_engineered_top_scorer.csv')
print(f"Top Scorer: {top_scorer_df.shape}")

# PS5: Match Result
match_result_df = pd.read_csv('data/match_prediction_corrected.csv')
print(f"Match Result: {match_result_df.shape}")
```

---

## Data Folder Structure (For Google Colab)

```
/content/drive/MyDrive/ScoreSight/
├── data/                                            ← Upload all CSV files here
│   ├── data_engineered_league_points.csv           ← PS1 & PS4
│   ├── data_engineered_match_prediction.csv        ← PS2
│   ├── data_engineered_top_scorer.csv              ← PS3
│   └── match_prediction_corrected.csv              ← PS5
├── models/                                          ← Auto-created, stores trained models
└── notebooks/                                       ← Place all training notebooks here
    ├── 10_League_Winner_PS1.ipynb
    ├── 11_Match_Winner_PS2.ipynb
    ├── 12_Top_Scorer_PS3.ipynb
    ├── 13_Total_Points_PS4.ipynb
    └── 14_Match_Result_PS5.ipynb
```

---

## Quick Checklist

- [ ] Export `league_winner_corrected.csv`
- [ ] Export `data_final_match_prediction.csv`
- [ ] Export `data_final_top_scorer.csv`
- [ ] Export `data_final_points_tally.csv`
- [ ] Export `match_prediction_corrected.csv`
- [ ] Create `/ScoreSight_Data/` folder in Google Drive
- [ ] Upload all 5 CSV files
- [ ] Create new Colab notebook
- [ ] Run mount and data loading code
- [ ] Copy the 5 problem statement notebooks code

---

## Total Data Size

Approximately **10-50 MB** total (depending on file sizes)

All files are in CSV format - no special dependencies needed!

---

**Next Steps:**
1. Export these 5 files from your local project
2. Upload to Google Drive
3. Use the provided Colab setup code
4. Run the 5 training notebooks in order (PS1 → PS2 → PS3 → PS4 → PS5)
5. Models will be saved in `/content/drive/MyDrive/ScoreSight_Data/models/`
