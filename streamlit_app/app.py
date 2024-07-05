import os
import sys
from pathlib import Path
import streamlit as st
import pickle

# Add the project root directory to the Python path
project_root_dir = Path(__file__).parent.parent
sys.path.append(str(project_root_dir))

# Import the modules from the appropriate directories
from streamlit_app.page_functions.player_stats import player_statistics
from streamlit_app.page_functions.team_stats import team_statistics
from streamlit_app.page_functions.queries import team_information_db
from streamlit_app.page_functions.gps_stats import gps_information
from streamlit_app.page_functions.player_gps_report import player_gps_report
from streamlit_app.page_functions.dataset_stats import dataset_statistics

# Configuration of the page
st.set_page_config(
    page_title="Soccer Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="auto",
    menu_items={
        'Get Help': 'https://www.simula.no',
        'Report a bug': "https://www.simula.no",
        'About': "Please read the README.md file for more information about this Simula Research Lab project"
    }
)

# Set the paths to the pickled data
path_to_teams = project_root_dir / "data/pickles/teams.pkl"
path_to_models = project_root_dir / "arima_forecasting"

@st.cache_data(ttl=600)
def load_in_pickles(path_to_data):
    try:
        with open(path_to_data, 'rb') as file:
            return pickle.load(file)
    except Exception as e:
        st.error(f"Error loading {path_to_data}: {e}")
        return {}

@st.cache_data(ttl=600)
def load_in_arima_models(path_to_arima):
    models = {}
    for file in os.listdir(path_to_arima):
        file_path = path_to_arima / file
        try:
            with open(file_path, 'rb') as f:
                models[file] = pickle.load(f)
        except Exception as e:
            st.error(f"Error loading {file}: {e}")
    return models

# Load in the pickled data and models
models = load_in_arima_models(path_to_models)
teams = load_in_pickles(path_to_teams)

# Define a dictionary of page names and associated functions
page_names_to_funcs = {
    "Dataset Statistics": dataset_statistics,
    "Player Information": player_statistics,
    "Team Information": team_statistics,
    "Team Information - DB": team_information_db,
    "GPS Information": gps_information,
    "Player GPS Report": player_gps_report
}

# Display a dropdown in the sidebar to select a page
selected_page = st.sidebar.selectbox("Select a page", list(page_names_to_funcs.keys()))

# Call the selected function with the teams and models if required
if selected_page in ["Player Information", "Team Information"]:
    page_names_to_funcs[selected_page](teams, models)
else:
    page_names_to_funcs[selected_page]()
