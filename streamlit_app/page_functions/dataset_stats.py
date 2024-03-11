import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.font_manager
import seaborn as sns
import streamlit as st
import datetime
import mysql.connector
import streamlit_app.page_functions.queries as qu

## For deployement locally, you create a folder called ".streamlit" inside the "streamlit_app" folder,
## You create once again, in ".streamlit", a file called "secrets.toml" where you put the connection credentials.
## For deployement on the cloud, you add directly the credentials to secrets.

@st.cache_resource
def init_connection():
    toml_data = st.secrets["mysql"]
    HOST_NAME = toml_data['host']
    DATABASE = toml_data['database']
    PASSWORD = toml_data['password']
    USER = toml_data['user']
    PORT = toml_data['port']
    conn = mysql.connector.connect(host=HOST_NAME, database=DATABASE, user=USER, passwd=PASSWORD, use_pure=True)
    return conn
conn = init_connection()

@st.cache_data(ttl=600)
def run_query(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()

conn = qu.conn
def dataset_statistics():
   
   st.title('Dataset Statistics')
   st.markdown("## Dataset Statistics")

   tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8 = st.tabs(["Overview", "Missing Data", "Daily Features", "Game Performance", "GPS", "Illnesses", "Injuries", "Session Features"])

   with tab1:
      st.header("Overview")
      df = pd.DataFrame(columns=['Team', 'Number of players', 'Number of years', 'Number of samples'])
      st.table(df)

   with tab2:
      st.header("Missing Data")
      df = pd.DataFrame(columns=['Missing Data'])
      st.table(df)

   with tab3:
      st.header("Daily Features")
      
      rowA = run_query(qu.rowA)
      rowB = run_query(qu.rowB)

      data = {
        "Team Name": ["TeamA", "TeamB"],
        "Number of Years": [int(rowA[0][0]), int(rowB[0][0])]
      }
      
      df = pd.DataFrame(data)
        
      hide_dataframe_row_index = """
        <style>
        .row_heading.level0 {display:none}
        .blank {display:none}
        </style>
        """
    
      st.markdown(hide_dataframe_row_index, unsafe_allow_html=True)

      st.table(df)

   with tab4:
      st.header("Game Performance")
      df = pd.DataFrame(columns=["Game Performance"])
      st.table(df)

   with tab5:
      st.header("GPS")
      df = pd.DataFrame(columns=['GPS'])
      st.table(df)

   with tab6:
      st.header("Illnesses")
      df = pd.DataFrame(columns=['Illnesses'])
      st.table(df)
   with tab7:
      st.header("Injuries")
      #df = pd.DataFrame(columns=['Injuries'])
      df = pd.read_sql(qu.inj, conn)
      st.table(df)      

   with tab8:
      st.header("Session Features")
      #df = pd.DataFrame(columns=['Session Features'])
      df = pd.read_sql(qu.ses.fet, conn)
      st.table(df)                                                            
