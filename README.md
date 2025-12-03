# ⚽ EPL Score Sight

**EPL Score Sight** is a comprehensive machine learning-powered application designed to predict various outcomes in the English Premier League (EPL). From predicting match winners to forecasting player stats like goals and assists, this tool leverages historical data and advanced algorithms to provide actionable insights.

---

## 🚀 Features

The application consists of five main prediction modules:

### 1. 🏆 Match Winner Prediction
Predict the outcome of a specific match between a Home Team and an Away Team.
*   **Input**: Select Home Team and Away Team.
*   **Output**: Probability of Home Win, Draw, or Away Win.
*   **Model**: Random Forest Classifier.
*   **Key Features**: Goal difference gap, points gap, form, win streaks.

### 2. 🥇 League Winner Prediction
Analyze whether a team has the statistical profile of a potential League Champion.
*   **Input**: Team stats (Goals Scored, Goals Conceded, etc.).
*   **Output**: Probability of being a Champion.
*   **Model**: Logistic Regression.

### 3. 📈 Total Points Estimation
Estimate the total points a team is likely to accumulate in a season based on their performance metrics.
*   **Input**: Goals Scored, Goals Conceded, Goal Difference.
*   **Output**: Predicted Total Points.
*   **Model**: Ridge Regression.

### 4. ⚽ Player Goals Prediction
Forecast the number of goals a player is expected to score.
*   **Input**: Player position, minutes played, shots, xG, etc.
*   **Output**: Predicted number of goals.
*   **Model**: Ridge Regression.

### 5. 👟 Player Assists Prediction
Forecast the number of assists a player is expected to provide.
*   **Input**: Player position, passes, key passes, xA, etc.
*   **Output**: Predicted number of assists.
*   **Model**: Ridge Regression.

---

## 🛠️ Tech Stack

*   **Frontend**: [Streamlit](https://streamlit.io/) - For building the interactive web interface.
*   **Language**: Python 3.x
*   **Machine Learning**: [Scikit-learn](https://scikit-learn.org/) - For model training and evaluation.
*   **Data Manipulation**: [Pandas](https://pandas.pydata.org/) & [NumPy](https://numpy.org/).
*   **Model Persistence**: Joblib.

---

## 📂 Project Structure

```text
EPL Score Sight/
├── app.py                  # Main entry point for the Streamlit application
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
├── backend/                # Backend utilities
│   └── utils/
│       └── model_loader.py # Helper to load trained models
├── frontend/               # Frontend pages and components
│   └── pages/              # Individual Streamlit pages for each feature
│       ├── match_winner.py
│       ├── league_winner.py
│       ├── total_points.py
│       ├── goals.py
│       └── assists.py
└── model_training/         # Scripts and data for training models
    ├── train_models.py     # Script to retrain all models
    ├── Data/               # Raw CSV/Excel datasets
    └── models/             # Directory where trained .pkl models are saved
```

---

## 💻 Installation & Setup

### 1. Prerequisites
Ensure you have **Python 3.8+** installed on your system.

### 2. Clone the Repository
```bash
git clone <repository-url>
cd "EPL Score Sight/Final project"
```

### 3. Create a Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### 4. Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 🏃‍♂️ How to Run

To start the application, run the following command from the project root directory:

```bash
python -m streamlit run app.py
```

The application will launch automatically in your default web browser at `http://localhost:8501`.

---

## 🧠 Model Training

If you want to retrain the models with new data or modified algorithms:

1.  Place your updated datasets in the `model_training/Data/` folder.
2.  Run the training script:
    ```bash
    python model_training/train_models.py
    ```
3.  The script will:
    *   Process the data.
    *   Train all 5 models.
    *   Save the trained models (`.pkl` files) to `model_training/models/`.
    *   The app will automatically use these new models upon restart.

---

## ⚠️ Troubleshooting

*   **"Streamlit is not recognized"**: Make sure you have activated your virtual environment and installed the requirements. Try using `python -m streamlit run app.py`.
*   **FileNotFoundError**: Ensure you are running the command from the root directory (`Final project`) so that relative paths to models and data are correct.
