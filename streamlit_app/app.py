import streamlit as st
import pickle
import os

# Define a function to load in all the ARIMA models from a directory of pickled models
@st.cache_data(ttl=600)
def load_in_arima_models(path_to_arima='/backend_functions/'):
    models = {}
    try:
        all_files = os.listdir(path_to_arima)
        for file in all_files:
            file_path = os.path.join(path_to_arima, file)
            with open(file_path, 'rb') as f:
                models[file] = pickle.load(f)
    except Exception as e:
        st.error(f"Error loading ARIMA models: {e}")
    
    return models

# Load in the pickled data and models
models = load_in_arima_models("/path/to/your/arima/models/")

# Define a function to get a player by name from the teams dictionary
def get_player(teams, player_name): 
    all_players = {**teams["TeamA"].players, **teams["TeamB"].players}
    return all_players[player_name]

# Display a dropdown in the sidebar to select a page
selected_page = st.sidebar.selectbox("Select a page", page_names_to_funcs.keys())

# Call the selected function with the teams and models
if selected_page == "Player Information" or selected_page == "Team Information":
    page_names_to_funcs[selected_page](teams, models)
else:
    page_names_to_funcs[selected_page]()
