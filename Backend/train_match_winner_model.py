# train_model.py

import pandas as pd
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import seaborn as sns
import pickle
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

match_data = pd.read_csv("match_winner_data.csv")

match_data['is_home_win'] = match_data['FTR'].apply(lambda x: 1 if x == 'H' else 0)

team_streak_features = [
    'HTWinStreak3','HTWinStreak5','HTLossStreak3','HTLossStreak5',
    'ATWinStreak3','ATWinStreak5','ATLossStreak3','ATLossStreak5'
]

team_performance_features = [
    'HTP','ATP','HTFormPts','ATFormPts','HTGD','ATGD','DiffPts','DiffFormPts'
]

selected_features = team_streak_features + team_performance_features

clean_data = match_data.dropna(subset=selected_features + ['is_home_win'])

X = clean_data[selected_features]
y = clean_data['is_home_win']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42, stratify=y )

def create_model(input_dim):
    model = tf.keras.Sequential([
        tf.keras.layers.Dense(128, activation='relu', input_shape=(input_dim,)),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dropout(0.4),

        tf.keras.layers.Dense(64, activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dropout(0.3),

        tf.keras.layers.Dense(32, activation='relu'),
        tf.keras.layers.Dropout(0.2),

        tf.keras.layers.Dense(1, activation='sigmoid')
    ])

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss='binary_crossentropy',
        metrics=['accuracy', 'precision', 'recall']
    )
    return model

model = create_model(X_train.shape[1])

callbacks = [
    tf.keras.callbacks.EarlyStopping(monitor='val_loss', patience=12, restore_best_weights=True),
    tf.keras.callbacks.ModelCheckpoint("models/best_football_predictor.h5", save_best_only=True)
]

history = model.fit(X_train, y_train, epochs=120, batch_size=64,
                    validation_split=0.2, callbacks=callbacks, verbose=1)

test_pred = (model.predict(X_test) > 0.5).astype(int).flatten()
print("Accuracy:", accuracy_score(y_test, test_pred))
print(classification_report(y_test, test_pred))

pickle.dump(scaler, open("models/feature_scaler.pkl", "wb"))
