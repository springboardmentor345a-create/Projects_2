# ScoreSight - Repository Structure

**Last Updated:** October 28, 2025  
**Author:** Prathamesh Fuke  
**Branch:** Prathamesh_Fuke

---

## 📁 Repository Organization

The repository has been organized into a clean, professional structure with logical folder separation:

```
ScoreSight/
│
├── 📓 notebooks/                          # Jupyter Notebooks
│   ├── 01_Data_Loading_EDA.ipynb         # Data loading & exploration
│   ├── 02_Data_Cleaning.ipynb            # Data cleaning & preprocessing
│   ├── 03_Feature_Engineering.ipynb      # Feature creation
│   ├── 04_Encoding_Feature_Selection.ipynb  # Encoding & selection
│   ├── 05_Data_Visualization.ipynb       # Visualizations
│   └── README.md                         # Notebooks documentation
│
├── 📊 data/                               # All Data Files
│   ├── raw/                              # Raw data after loading
│   │   ├── data_raw_match.csv           # 6,840 matches
│   │   ├── data_raw_player.csv          # 2,274 player records
│   │   ├── data_raw_league.csv          # 180 team-season records
│   │   └── README.md
│   │
│   ├── cleaned/                          # Cleaned datasets
│   │   ├── data_cleaned_match.csv
│   │   ├── data_cleaned_player.csv
│   │   ├── data_cleaned_league.csv
│   │   └── README.md
│   │
│   ├── features/                         # Feature-engineered data
│   │   ├── data_features_match.csv
│   │   ├── data_features_player.csv
│   │   ├── data_features_league.csv
│   │   └── README.md
│   │
│   ├── encoded/                          # Encoded datasets
│   │   ├── data_encoded_match.csv
│   │   ├── data_encoded_player.csv
│   │   ├── data_encoded_league.csv
│   │   └── README.md
│   │
│   └── final/                            # Final modeling datasets
│       ├── data_final_match_prediction.csv   # For match prediction
│       ├── data_final_top_scorer.csv         # For top scorer prediction
│       ├── data_final_points_tally.csv       # For points tally prediction
│       └── README.md
│
├── 🗂️ datasets/                           # Original Datasets
│   ├── Match Winner.csv                  # 1.3 MB - Historical matches
│   ├── Goals & Assist.xlsx               # 487 KB - Player statistics
│   ├── ScoreSight_ML_Season_LeagueWinner_Champion.csv  # 14 KB - League data
│   └── README.md
│
├── 📈 visualizations/                     # Generated Visualizations
│   ├── viz_match_correlation.png         # Match feature correlations
│   ├── viz_match_distributions.png       # Distribution plots
│   ├── viz_player_correlation.png        # Player feature correlations
│   ├── viz_top_scorers.png               # Top 10 scorers chart
│   ├── viz_league_statistics.png         # League statistics
│   ├── viz_summary_dashboard.png         # Complete summary dashboard
│   └── README.md
│
├── 🔧 scripts/                            # Python Scripts
│   ├── execute_notebooks.py              # Automated notebook execution
│   ├── validate_data.py                  # Data quality validation
│   └── README.md
│
├── 📄 docs/                               # Documentation
│   ├── PREPROCESSING_SUMMARY.md          # Preprocessing details
│   ├── PROJECT_STATUS.md                 # Current project status
│   ├── QUICK_START_GUIDE.md              # Quick start instructions
│   ├── EXECUTION_REPORT.md               # Execution results
│   ├── AI_ScoreSight Doc.pdf             # Project documentation
│   └── README.md
│
├── 📋 Root Files
│   ├── README.md                         # Main project README
│   ├── REPOSITORY_STRUCTURE.md           # This file
│   ├── requirements.txt                  # Python dependencies
│   ├── LICENSE                           # License file
│   └── MIT LICENSE                       # MIT License
│
└── .git/                                  # Git repository
```

---

## 📊 Folder Details

### 1. notebooks/
**Purpose:** Contains all Jupyter notebooks for data preprocessing

**Contents:**
- 5 sequential preprocessing notebooks
- Each notebook is self-contained and well-documented
- Notebooks use relative paths to access data

**Usage:**
```bash
cd notebooks
jupyter notebook
```

---

### 2. data/
**Purpose:** Organized storage for all data files at different processing stages

#### 2.1 data/raw/
- **Purpose:** Raw data immediately after loading
- **Files:** 3 CSV files
- **Total Size:** ~1.6 MB
- **Records:** 9,294 total records

#### 2.2 data/cleaned/
- **Purpose:** Cleaned and standardized data
- **Files:** 3 CSV files
- **Quality:** 100% complete, no missing values

#### 2.3 data/features/
- **Purpose:** Feature-engineered datasets
- **Files:** 3 CSV files
- **Status:** Ready for encoding

#### 2.4 data/encoded/
- **Purpose:** Encoded datasets with categorical variables transformed
- **Files:** 3 CSV files
- **Features:** Increased column count due to encoding

#### 2.5 data/final/
- **Purpose:** Final datasets ready for machine learning
- **Files:** 3 CSV files
- **Status:** 100% ready for model training
- **Characteristics:**
  - Numeric columns only
  - Zero missing values
  - Zero duplicates

---

### 3. datasets/
**Purpose:** Original datasets from the repository

**Contents:**
- Match Winner.csv (1.3 MB) - 6,840 matches
- Goals & Assist.xlsx (487 KB) - Player statistics
- ScoreSight_ML_Season_LeagueWinner_Champion.csv (14 KB) - League data

**Note:** These are the source datasets. All processing starts from here.

---

### 4. visualizations/
**Purpose:** All generated visualizations and plots

**Contents:**
- 6 high-resolution PNG files
- Correlation heatmaps
- Distribution plots
- Top performers charts
- Summary dashboards

**Usage:** Reference these visualizations in reports and presentations

---

### 5. scripts/
**Purpose:** Python automation scripts

**Contents:**
- `execute_notebooks.py` - Runs all notebooks sequentially
- `validate_data.py` - Validates data quality

**Usage:**
```bash
cd scripts
python execute_notebooks.py  # Execute all notebooks
python validate_data.py       # Validate data quality
```

---

### 6. docs/
**Purpose:** Project documentation

**Contents:**
- Preprocessing summary
- Project status tracking
- Quick start guide
- Execution report
- Original project documentation PDF

**Usage:** Reference for understanding project workflow and results

---

## 🎯 Key Benefits of This Structure

### 1. **Clear Separation of Concerns**
- Notebooks in one place
- Data organized by processing stage
- Scripts separate from notebooks
- Documentation centralized

### 2. **Easy Navigation**
- Logical folder names
- README in each folder
- Clear file naming conventions

### 3. **Scalability**
- Easy to add new notebooks
- Simple to add new data stages
- Room for additional scripts

### 4. **Professional Organization**
- Industry-standard structure
- Clean repository appearance
- Easy for collaborators to understand

### 5. **Version Control Friendly**
- Logical .gitignore structure
- Clear separation of code and data
- Easy to track changes

---

## 📝 File Naming Conventions

### Notebooks
- Format: `##_Description.ipynb`
- Sequential numbering (01, 02, 03...)
- Descriptive names
- Example: `01_Data_Loading_EDA.ipynb`

### Data Files
- Format: `data_[stage]_[type].csv`
- Stages: raw, cleaned, features, encoded, final
- Types: match, player, league
- Example: `data_final_match_prediction.csv`

### Visualizations
- Format: `viz_[description].png`
- Descriptive names
- Example: `viz_match_correlation.png`

### Scripts
- Format: `[action]_[target].py`
- Action verbs (execute, validate, etc.)
- Example: `execute_notebooks.py`

### Documentation
- Format: `[TITLE]_[TYPE].md` or `[TITLE].md`
- All caps for major docs
- Example: `EXECUTION_REPORT.md`

---

## 🔄 Data Flow

```
datasets/
  ↓ (Load)
data/raw/
  ↓ (Clean)
data/cleaned/
  ↓ (Engineer Features)
data/features/
  ↓ (Encode)
data/encoded/
  ↓ (Select Features)
data/final/
  ↓ (Train Models)
[Model Building Phase]
```

---

## 📊 Storage Summary

| Folder | Files | Total Size | Purpose |
|--------|-------|------------|---------|
| notebooks/ | 5 + 1 README | ~60 KB | Jupyter notebooks |
| data/raw/ | 3 + 1 README | ~1.6 MB | Raw data |
| data/cleaned/ | 3 + 1 README | ~1.6 MB | Cleaned data |
| data/features/ | 3 + 1 README | ~1.6 MB | Feature-engineered |
| data/encoded/ | 3 + 1 README | ~1.9 MB | Encoded data |
| data/final/ | 3 + 1 README | ~1.4 MB | Final datasets |
| datasets/ | 3 + 1 README | ~1.8 MB | Original datasets |
| visualizations/ | 6 + 1 README | ~2-3 MB | PNG visualizations |
| scripts/ | 2 + 1 README | ~10 KB | Python scripts |
| docs/ | 5 + 1 README | ~200 KB | Documentation |

**Total Repository Size:** ~12-15 MB (excluding .git)

---

## 🚀 Getting Started with New Structure

### For New Users:
1. Start with `README.md` in root
2. Read `docs/QUICK_START_GUIDE.md`
3. Review `docs/PROJECT_STATUS.md`
4. Open `notebooks/` and run sequentially

### For Continuing Work:
1. Navigate to appropriate folder
2. Use relative paths in notebooks
3. Scripts automatically handle paths
4. All outputs go to correct folders

### For Model Building:
1. Use datasets from `data/final/`
2. Create new `models/` folder if needed
3. Reference visualizations from `visualizations/`
4. Document in `docs/`

---

## ✅ Organization Checklist

- [x] Notebooks organized in dedicated folder
- [x] Data files organized by processing stage
- [x] Original datasets preserved separately
- [x] Visualizations in dedicated folder
- [x] Scripts separated from notebooks
- [x] Documentation centralized
- [x] README files in each folder
- [x] Duplicate files removed
- [x] Executed notebooks removed
- [x] Clean root directory
- [x] Professional structure
- [x] Easy to navigate
- [x] Scalable design

---

## 🎓 Best Practices Applied

1. **Separation of Concerns:** Code, data, docs, and outputs separated
2. **Clear Naming:** Consistent, descriptive file names
3. **Documentation:** README in every folder
4. **No Duplicates:** Removed executed notebook copies
5. **Relative Paths:** Notebooks use relative paths
6. **Scalability:** Easy to add new components
7. **Professional:** Industry-standard structure

---

## 📞 Navigation Tips

### To Run Notebooks:
```bash
cd notebooks
jupyter notebook
# Open notebooks in order: 01 → 02 → 03 → 04 → 05
```

### To Validate Data:
```bash
cd scripts
python validate_data.py
```

### To View Visualizations:
```bash
cd visualizations
# Open PNG files in image viewer
```

### To Read Documentation:
```bash
cd docs
# Open markdown files in text editor or markdown viewer
```

---

## 🎉 Summary

The repository is now professionally organized with:
- ✅ **Clean structure** - Logical folder organization
- ✅ **No duplicates** - Executed notebooks removed
- ✅ **Clear navigation** - Easy to find files
- ✅ **Professional appearance** - Industry-standard layout
- ✅ **Scalable design** - Easy to extend
- ✅ **Well documented** - README in every folder

**Status:** ✅ **ORGANIZED AND READY FOR MODEL BUILDING**

---

*Document Created: October 28, 2025*  
*Repository Structure: Version 1.0*  
*Status: Complete*
