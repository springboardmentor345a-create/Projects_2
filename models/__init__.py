# models/__init__.py

 if st.session_state.selected_page == "league_winner":
    league_winner_prediction()
elif st.session_state.selected_page == "points_prediction":
    total_points_prediction_page()
elif st.session_state.selected_page == "goals_prediction":
    goals_prediction_page()
elif st.session_state.selected_page == "assist_prediction":
    assist_prediction_page()
elif st.session_state.selected_page == "match_winner":
    match_winner_prediction_page()