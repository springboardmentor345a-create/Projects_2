# 🚀 ScoreSight - Quick Start Guide

**Welcome to ScoreSight!** This guide will help you get started with the data preprocessing phase.

---

## ⚡ Quick Setup (5 Minutes)

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Launch Jupyter Notebook
```bash
jupyter notebook
```

### Step 3: Run Notebooks in Order
Execute these notebooks sequentially:
1. `01_Data_Loading_EDA.ipynb`
2. `02_Data_Cleaning.ipynb`
3. `03_Feature_Engineering.ipynb`
4. `04_Encoding_Feature_Selection.ipynb`
5. `05_Data_Visualization.ipynb`

---

## 📋 Detailed Instructions

### Prerequisites
- ✅ Python 3.8 or higher installed
- ✅ Jupyter Notebook installed
- ✅ Git installed (already done)
- ✅ Internet connection for package installation

### Installation Steps

#### 1. Verify Python Installation
```bash
python --version
```
Should show Python 3.8 or higher.

#### 2. Install Required Packages
```bash
pip install -r requirements.txt
```

This installs:
- pandas (data manipulation)
- numpy (numerical computing)
- matplotlib & seaborn (visualization)
- scikit-learn (machine learning)
- openpyxl (Excel file support)
- jupyter (notebook environment)

#### 3. Launch Jupyter Notebook
```bash
cd D:/ScoreSight
jupyter notebook
```

Your browser will open with the Jupyter interface.

---

## 📓 Notebook Execution Guide

### Notebook 01: Data Loading & EDA
**Purpose**: Load datasets and perform initial exploration

**What it does**:
- Loads Match Winner.csv
- Loads Goals & Assist.xlsx
- Loads League data CSV
- Displays data structure and statistics
- Identifies missing values
- Saves raw data files

**Expected Output**:
- `data_raw_match.csv`
- `data_raw_player.csv`
- `data_raw_league.csv`

**Execution Time**: ~2-3 minutes

---

### Notebook 02: Data Cleaning
**Purpose**: Clean and standardize datasets

**What it does**:
- Removes duplicate records
- Handles missing values
- Standardizes column names
- Fixes data types
- Saves cleaned data files

**Expected Output**:
- `data_cleaned_match.csv`
- `data_cleaned_player.csv`
- `data_cleaned_league.csv`

**Execution Time**: ~2-3 minutes

---

### Notebook 03: Feature Engineering
**Purpose**: Create new features for modeling

**What it does**:
- Creates match prediction features
- Generates player performance metrics
- Builds team strength indicators
- Saves feature-engineered data

**Expected Output**:
- `data_features_match.csv`
- `data_features_player.csv`
- `data_features_league.csv`

**Execution Time**: ~3-5 minutes

---

### Notebook 04: Encoding & Feature Selection
**Purpose**: Prepare data for machine learning

**What it does**:
- Encodes categorical variables
- Selects relevant features
- Creates final modeling datasets
- Saves encoded and final data

**Expected Output**:
- `data_encoded_match.csv`
- `data_encoded_player.csv`
- `data_encoded_league.csv`
- `data_final_match_prediction.csv`
- `data_final_top_scorer.csv`
- `data_final_points_tally.csv`

**Execution Time**: ~2-3 minutes

---

### Notebook 05: Data Visualization
**Purpose**: Visualize data patterns and insights

**What it does**:
- Creates correlation heatmaps
- Generates distribution plots
- Visualizes top performers
- Builds summary dashboards
- Saves visualization files

**Expected Output**:
- `viz_match_correlation.png`
- `viz_match_distributions.png`
- `viz_player_correlation.png`
- `viz_top_scorers.png`
- `viz_league_statistics.png`
- `viz_summary_dashboard.png`

**Execution Time**: ~3-5 minutes

---

## 🎯 Expected Results

After running all notebooks, you should have:

### 📁 Data Files (15 CSV files)
- 3 raw data files
- 3 cleaned data files
- 3 feature-engineered files
- 3 encoded data files
- 3 final modeling files

### 🖼️ Visualizations (6 PNG files)
- Correlation heatmaps
- Distribution plots
- Top scorer charts
- Summary dashboards

### 📊 Total Processing
- **Time**: ~15-20 minutes
- **Data Processed**: 6,841+ match records, player stats, league data
- **Features Created**: Varies based on data structure

---

## ✅ Verification Checklist

After running all notebooks, verify:

- [ ] All 15 CSV files created in project directory
- [ ] All 6 PNG visualization files created
- [ ] No error messages in notebook outputs
- [ ] Data quality metrics show:
  - Zero missing values
  - No duplicate records
  - Proper encoding of categorical variables
- [ ] Visualizations display correctly

---

## 🐛 Troubleshooting

### Issue: Module Not Found Error
**Solution**: Install missing package
```bash
pip install <package-name>
```

### Issue: File Not Found Error
**Solution**: Ensure you're in the correct directory
```bash
cd D:/ScoreSight
```

### Issue: Jupyter Kernel Crashes
**Solution**: Restart kernel
- In Jupyter: Kernel → Restart

### Issue: Memory Error
**Solution**: Close other applications and restart notebook

### Issue: Excel File Won't Load
**Solution**: Install openpyxl
```bash
pip install openpyxl
```

---

## 💡 Tips for Success

1. **Run Cells Sequentially**: Don't skip cells or run out of order
2. **Check Outputs**: Verify each cell's output before proceeding
3. **Save Progress**: Save notebooks frequently (Ctrl+S)
4. **Monitor Memory**: Close unused notebooks to free memory
5. **Read Comments**: Notebook cells contain helpful explanations

---

## 📚 Additional Resources

### Documentation
- `README.md` - Complete project overview
- `PREPROCESSING_SUMMARY.md` - Detailed preprocessing summary
- `PROJECT_STATUS.md` - Current project status

### Datasets
- `Match Winner.csv` - Match results (1.3 MB)
- `Goals & Assist.xlsx` - Player stats (487 KB)
- `ScoreSight_ML_Season_LeagueWinner_Champion.csv` - League data (14 KB)

### Reference
- `AI_ScoreSight Doc.pdf` - Project documentation

---

## 🎓 Learning Path

### Beginner Level
1. Run notebooks and observe outputs
2. Read markdown cells for explanations
3. Examine generated CSV files
4. Review visualizations

### Intermediate Level
1. Modify feature engineering logic
2. Experiment with different imputation strategies
3. Create additional visualizations
4. Analyze feature correlations

### Advanced Level
1. Add custom features
2. Integrate external datasets
3. Optimize preprocessing pipeline
4. Implement advanced encoding techniques

---

## 🚀 Next Steps After Preprocessing

Once all notebooks are executed:

1. **Review Outputs**: Examine all generated files
2. **Analyze Visualizations**: Study patterns and insights
3. **Verify Data Quality**: Check for any issues
4. **Begin Model Building**: Move to Phase 2
5. **Train ML Models**: Use final datasets for training

---

## 📞 Need Help?

If you encounter issues:
1. Check the troubleshooting section above
2. Review notebook comments and markdown cells
3. Verify all dependencies are installed
4. Ensure you're using Python 3.8+
5. Check that all data files are present

---

## ✨ Success Indicators

You'll know preprocessing is successful when:
- ✅ All notebooks execute without errors
- ✅ All expected files are generated
- ✅ Visualizations display correctly
- ✅ Data quality metrics are satisfactory
- ✅ No missing values in final datasets

---

## 🎉 Congratulations!

Once you complete all notebooks, you'll have:
- ✅ Clean, preprocessed datasets
- ✅ Engineered features ready for modeling
- ✅ Comprehensive visualizations
- ✅ Understanding of data patterns
- ✅ Foundation for model building

**You're now ready for Phase 2: Model Building!** 🚀

---

*Last Updated: October 28, 2025*  
*Author: Prathamesh Fuke*  
*Branch: Prathamesh_Fuke*
