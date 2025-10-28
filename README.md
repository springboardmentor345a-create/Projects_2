# ScoreSight - Predicting EPL Points Tally, Top Scorer

## Project Overview

ScoreSight is a machine learning project aimed at predicting outcomes in the English Premier League (EPL). The project focuses on two primary objectives:
1.  **Predicting Match Results:** Forecasting match winners, scores, and ultimately, league champions.
2.  **Predicting Top Scorers:** Estimating individual player goals and assists for the upcoming season.

This project involves data preprocessing, model training (likely regression models using neural networks), evaluation, and eventually, deployment as a full-stack application.

## Current Status: Data Cleaning and Feature Selection

We have completed the initial phase of data cleaning and feature selection for the three primary datasets used in this project:
*   `Goals & Assist.xlsx` (for player performance prediction)
*   `Match Winner.csv` (for match outcome prediction)
*   `ScoreSight_ML_Season_LeagueWinner_Champion.csv` (for season outcome prediction)

Detailed reasoning for the columns kept and removed from each dataset can be found in:
[Docs/Datacleaning.md](Docs/Datacleaning.md)

The respective Jupyter notebooks (`Notebooks/1_Goals_Assist_Preprocessing.ipynb`, `Notebooks/2_Match_Winner_Preprocessing.ipynb`, `Notebooks/3_Season_Winner_Preprocessing.ipynb`) have been updated to include the code for these column removals.

## Next Steps

The upcoming phases of the ScoreSight project will involve:

1.  **Data Preprocessing (Continued):** Further cleaning, handling missing values, encoding categorical features, and scaling numerical features within the updated notebooks.
2.  **Feature Engineering:** Creating new, more powerful features from the existing data to enhance model performance.
3.  **Model Training:** Developing and training machine learning models (e.g., regression models, potentially neural networks as outlined in `AI_ScoreSight Doc.pdf`) for each prediction task.
4.  **Model Evaluation:** Rigorously evaluating the trained models using appropriate metrics (e.g., MAE, RMSE) and fine-tuning them for optimal performance.
5.  **Documentation and Presentation:** Preparing comprehensive documentation of the methodology, results, and conclusions, along with a presentation.
6.  **Application Development:** Building a full-stack application with a user interface to interact with the trained models.
