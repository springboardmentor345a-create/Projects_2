from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
import numpy as np
import joblib
from sklearn.preprocessing import StandardScaler
import os

app = Flask(__name__)
CORS(app)

# Global variables
model = None
scaler = StandardScaler()

def load_dataset():
    path = "ScoreSight_ML_Season_LeagueWinner_Champion (1).csv"
    df = pd.read_csv(path)
    
    selected_columns = [
        'matches_played',
        'wins',
        'draws',
        'losses',
        'goals_scored',
        'goals_conceded',
        'target_total_points',
        'target_top_4'
    ]
    
    return df[selected_columns]

def prepare_features(df):
    X = df.drop(['target_total_points', 'target_top_4'], axis=1)
    y = df['target_top_4']
    return X, y

def train_model():
    global model, scaler
    
    df = load_dataset()
    X, y = prepare_features(df)
    X_scaled = scaler.fit_transform(X)
    
    from sklearn.linear_model import LogisticRegression
    model = LogisticRegression(random_state=42, max_iter=1000)
    model.fit(X_scaled, y)
    
    joblib.dump(model, 'league_winner_model.pkl')
    joblib.dump(scaler, 'scaler.pkl')
    
    return "Model trained!"

def load_saved_model():
    global model, scaler
    try:
        model = joblib.load('league_winner_model.pkl')
        scaler = joblib.load('scaler.pkl')
        return True
    except:
        return False

if not load_saved_model():
    print("Training new model...")
    train_model()
    load_saved_model()

@app.route('/')
def home():
    return jsonify({"message": "League Winner Prediction API"})

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        
        input_features = np.array([[
            data.get('matches_played', 0),
            data.get('wins', 0),
            data.get('draws', 0),
            data.get('losses', 0),
            data.get('goals_scored', 0),
            data.get('goals_conceded', 0)
        ]])
        
        input_scaled = scaler.transform(input_features)
        prediction = model.predict(input_scaled)
        prediction_proba = model.predict_proba(input_scaled)
        top4_probability = float(prediction_proba[0][1]) * 100
        
        return jsonify({
            "success": True,
            "prediction": int(prediction[0]),
            "top4_probability": round(top4_probability, 2),
            "interpretation": "1 = Top 4, 0 = Not Top 4"
        })
        
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)