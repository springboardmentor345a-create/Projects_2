import streamlit as st

st.title("EPL ScoreSight Dashboard")
st.write("Welcome to the Football Prediction Dashboard!")

team_name = st.text_input("Enter Team Name:")
if team_name:
    st.write(f"You entered: {team_name}")
