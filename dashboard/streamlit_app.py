"""

Streamlit dashboard application code

Module contains code for connecting to postgres database (RDS)
and using that data to create charts for data analysis.
"""
import os
from os import environ
import streamlit as st
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from psycopg2 import connect
from psycopg2.extensions import connection
from dotenv import load_dotenv


def get_live_data(db_conn: connection) -> pd.DataFrame:
    """Function that gets the required data from the database connection 
    and puts all data into pandas DataFrame form"""
    cursor = db_conn.cursor()
    cursor.execute("SELECT * FROM plant")
    names = [x[0] for x in cursor.description]
    live_plants_data = pd.DataFrame(cursor.fetchall(), columns=names)
    return live_plants_data


def get_archived_data() -> pd.DataFrame:
    """Function that gets the required data from the s3 bucket and
    puts all data into pandas DataFrame form"""

    # Download all CSV files from the archive s3 bucket

    csv_files = [f for f in os.listdir("archived_data") if f.endswith('.csv')]
    dfs = []

    for csv in csv_files:
        csv_to_df = pd.read_csv("archived_data/"+csv)
        dfs.append(csv_to_df)

    archived_plants_data = pd.concat(dfs, ignore_index=True)

    # Delete all CSV files from the archived_data folder locally

    return archived_plants_data


def sidebar(db_connection: connection) -> None:
    """Function that sets up the sidebar for the dashboard"""
    #st.sidebar.title("ONTHEB-RINK-OFEXTINCTION")
    #st.sidebar.markdown("An app for Liverpool Natural History Museum,\
                        #monitoring the health of our plants")

    # data = get_live_data(db_connection)

    #print(data)

    toggle_on = st.sidebar.toggle(label="Toggle for Archived Data", value=False, )
    if toggle_on:
        data = get_archived_data()

    # with st.sidebar.expander("Expand to see information about the plants"):
    #     st.markdown("Lorem Ipsum")
    return data

def dashboard_header()-> None:
    """Create a header for the dashboard."""
    st.title("ONTHEB-RINK-OFEXTINCTION")
    st.markdown("An app for Liverpool Natural History Museum,\
                        #monitoring the health of our plants")



def get_data_from_database(conn: connection):
    """Retrieve plant data from the database and return as a DataFrame."""

    query = """
    SELECT p.plant_entry_id AS entry_id,
           s.scientific_name AS species,
           p.temperature,
           p.soil_moisture,
           p.humidity,
           p.last_watered AS last_watered,
           p.recording_taken AS recording_taken,
           sun.s_description AS sunlight,
           b.b_name AS botanist_name,
           c.cycle_name AS cycle
    FROM plant p
    LEFT JOIN species s ON p.species_id = s.species_id
    LEFT JOIN sunlight sun ON p.sunlight_id = sun.sunlight_id
    LEFT JOIN botanist b ON p.botanist_id = b.botanist_id
    LEFT JOIN cycle c ON p.cycle_id = c.cycle_id;
    """
    
    with conn.cursor() as cur:
        cur.execute(query)
        data = cur.fetchall()

    columns = ["entry_id", "species", "temperature", "soil_moisture", "humidity", "last_watered", "recording_taken", "sunlight", "botanist_name", "cycle"]
    data_df = pd.DataFrame(data, columns=columns)
    data_df["last_watered"] = pd.to_datetime(data_df["last_watered"])
    data_df["recording_taken"] = pd.to_datetime(data_df["recording_taken"])
    
    return data_df

def plot_temp_for_10_plants(data_df)-> None:
    # Create a bar chart using Seaborn
    plt.figure(figsize=(10, 6))
    sns.barplot(x="species", y="temperature", data=data_df)
    plt.xticks(rotation=45)
    plt.xlabel("Species")
    plt.ylabel("Temperature")
    plt.title("Temperature Values for Different Plants")
    st.pyplot()
    
if __name__ == "__main__":

    load_dotenv()
    config = environ

    conn = connect(
            user=config["DATABASE_USERNAME"],
            password=config["DATABASE_PASSWORD"],
            host=config["DATABASE_IP"],
            port=config["DATABASE_PORT"],
            database=config["DATABASE_NAME"],
        )
    
    st.set_option('deprecation.showPyplotGlobalUse', False)


    plant_data_df = get_data_from_database(conn)
    dashboard_header()
    # Initialize the starting index and number of rows to show
    start_index = 0
    rows_to_show = 10

    st.title("Plant Temperature Bar Chart")
    st.write("Bar chart showing temperature values for different plants.")

    # Sidebar options
    with st.sidebar:
        st.sidebar.title("Options")
        if st.button("Show Previous 10 Rows"):
            start_index = max(0, start_index - rows_to_show)
            data_to_show = plant_data_df[start_index:start_index+rows_to_show]
        if st.button("Show Next 10 Rows"):
            start_index += rows_to_show
            data_to_show = plant_data_df[start_index:start_index+rows_to_show]

    # Show the initial bar chart
    initial_data_to_show = plant_data_df[start_index:start_index+rows_to_show]
    plot_temp_for_10_plants(initial_data_to_show)
    #plant_data = sidebar(conn)
    
    # st.markdown(plant_data.style.hide(axis="index").to_html(), unsafe_allow_html=True)
    