# ScoreSight - Streamlit Application

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run the Application

```bash
streamlit run app/main.py
```

The application will open in your default browser at `http://localhost:8501`

## 📱 Application Structure

```
app/
├── main.py                      # Home page / Dashboard
├── pages/                       # Multi-page app
│   ├── 1_🏆_League_Winner.py   # Predict Top 4 teams
│   ├── 2_⚽_Match_Winner.py     # Predict match outcomes
│   ├── 3_👟_Top_Scorer.py      # Predict player goals
│   └── 4_📊_Total_Points.py    # Predict season points
└── utils/                       # Utilities
    ├── model_loader.py          # ML model loading & caching
    └── data_loader.py           # Data loading utilities
```

## 🎯 Features

### 1. **League Winner Prediction** 🏆
- **Model:** RandomForest
- **Accuracy:** 95%
- **Input:** Team season statistics (wins, draws, losses, PPG, GF, GA)
- **Output:** Top 4 qualification probability

### 2. **Match Winner Prediction** ⚽
- **Model:** XGBoost
- **Accuracy:** 66%
- **Input:** Match statistics (points gap, form, streaks, goals)
- **Output:** Home Win / Draw / Away Win probabilities

### 3. **Top Scorer Prediction** 👟
- **Model:** XGBoost
- **R² Score:** 0.957
- **Input:** Player per-90 statistics (goals, assists, xG, npxG, xAG)
- **Output:** Predicted total goals for the season

### 4. **Total Points Prediction** 📊
- **Model:** Ridge Regression
- **R² Score:** 0.937
- **MAE:** 3.7 points
- **Input:** Current season stats (matches played, GF, GA, GD)
- **Output:** Predicted final points tally

## 🎨 Design Features

- **Dark Premium Theme** with gradient effects
- **Glassmorphism UI** with backdrop blur
- **Interactive Visualizations** using Plotly
- **Responsive Design** for all screen sizes
- **Real-time Predictions** with confidence scores

## 📊 Models Used

All predictions use **production-ready models** trained on:
- **6,840 matches** (18 seasons of EPL data)
- **2,274 player records**
- **96 engineered features**
- **Zero data leakage** - all features are pre-match/pre-event

## 🛠️ Technical Details

### Model Files
- `ps1_league_winner_best_model.joblib` - RandomForest (League Winner)
- `match_winner_best_model.joblib` - XGBoost (Match Winner)
- `ps2_top_scorer_goals_model.joblib` - XGBoost (Top Scorer)
- `ps3_total_points_best_model.joblib` - Ridge (Total Points)

### Data Files
- `data/league_winner/league_winner_data.csv`
- `data/match_winner/match_winner_data.csv`
- `data/top_scorer/top_scorer_data.csv`
- `data/points_tally/points_tally_data.csv`

## 🔧 Configuration

The app uses `streamlit`'s built-in caching:
- `@st.cache_resource` for ML models (loaded once)
- `@st.cache_data` for CSV data (loaded once)

## 📝 Usage Examples

### League Winner
```
Input: Wins=22, Draws=8, Losses=8, PPG=2.0, GF=70, GA=35
Output: TOP 4 LIKELY (95% confidence)
```

### Match Winner
```
Input: Home=Liverpool, Away=Chelsea
Output: Home Win 55%, Draw 25%, Away Win 20%
```

### Top Scorer
```
Input: goals_per_90=0.75, xG_per_90=0.80, 30 matches
Output: 23 goals predicted
```

### Total Points
```
Input: Played=20, GF=45, GA=22, GD=+23
Output: 78 points (Top 4)
```

## 🚨 Troubleshooting

### Port Already in Use
```bash
streamlit run app/main.py --server.port 8502
```

### Module Not Found
```bash
pip install -r requirements.txt
```

### Model File Not Found
Ensure you're running from the ScoreSight root directory where `models/` folder exists.

## 📞 Support

**Created by:** Prathamesh Fuke  
**Version:** 1.0  
**Last Updated:** November 24, 2025

## 📄 License

See LICENSE file in the repository root.
