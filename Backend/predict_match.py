import numpy as np
import tensorflow as tf
import pickle

loaded_model = tf.keras.models.load_model("models/best_football_predictor.h5")
scaler = pickle.load(open("models/feature_scaler.pkl", "rb"))

def predict_match(features):
    scaled = scaler.transform([features])
    prob = loaded_model.predict(scaled)[0][0]
    result = "HOME WIN" if prob > 0.5 else "AWAY/DRAW"
    return result, prob
