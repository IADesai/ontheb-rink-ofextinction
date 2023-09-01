"""Streamlit dashboard application code

Module contains code for connecting to postgres database (RDS)
and using that data to create charts for data analysis.
"""
import sys
from os import environ, path, listdir
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from psycopg2 import connect, Error
from psycopg2.extensions import connection
from dotenv import load_dotenv

CSV_COLUMNS = [
    "entry_id", "species", "temperature", "soil_moisture",
    "last_watered", "recording_taken", "sunlight", "botanist_name", "cycle"
]


def get_db_connection():
    """Establishes a connection with the PostgreSQL database."""
    try:
        conn = connect(
            user=environ.get("DATABASE_USERNAME"),
            password=environ.get("DATABASE_PASSWORD"),
            host=environ.get("DATABASE_IP"),
            port=environ.get("DATABASE_PORT"),
            database=environ.get("DATABASE_NAME"),)
        print("Database connection established successfully.")
        return conn
    except Error as err:
        print("Error connecting to database: ", err)
        sys.exit()


def get_live_database(conn: connection) -> pd.DataFrame:
    """Retrieve plant data from the database and return as a DataFrame."""

    query = """
    SELECT p.plant_entry_id AS entry_id,
           s.s_name AS species,
           p.temperature,
           p.soil_moisture,
           p.last_watered AS last_watered,
           p.recording_taken AS recording_taken,
           sun.s_description AS sunlight,
           b.b_name AS botanist_name,
           c.cycle_name AS cycle
    FROM plant p
    LEFT JOIN species s ON p.species_id = s.species_id
    LEFT JOIN sunlight sun ON p.sunlight_id = sun.sunlight_id
    LEFT JOIN botanist b ON p.botanist_id = b.botanist_id
    LEFT JOIN cycle c ON p.cycle_id = c.cycle_id
    WHERE recording_taken > DATE_TRUNC('minute', CURRENT_TIMESTAMP::timestamp) + INTERVAL '59 minutes' AND recording_taken < DATE_TRUNC('minute', CURRENT_TIMESTAMP::timestamp) + INTERVAL '60 minutes';
    """

    with conn.cursor() as cur:
        cur.execute(query)
        data = cur.fetchall()

    data_df = pd.DataFrame(data, columns=CSV_COLUMNS)
    data_df["last_watered"] = pd.to_datetime(data_df["last_watered"])
    data_df["recording_taken"] = pd.to_datetime(data_df["recording_taken"])

    return data_df


def get_selected_archive() -> pd.DataFrame:
    """Creates the dropdown and which archived file 
    to select and return for display."""
    with st.sidebar:
        st.sidebar.title("Dropdown")

        csv_files = [f for f in listdir(
            "archived_data") if f.endswith('.csv')]

        #Dropdown to select a csv file.
        selected_csv = st.selectbox(
            "Select an archived file.", csv_files, on_change=on_toggle_or_archive_change)
        data = pd.read_csv(path.join("archived_data", selected_csv))
    return data


def on_toggle_or_archive_change() -> None:
    """Sets the index back to 0 for all of the graphs upon changing
    the toggle status or which archive is being viewed.
    """
    st.session_state.start_index = 0


def switch_data(db_connection: connection) -> pd.DataFrame:
    """Returns either the live data or the archived data 
    based on if toggle is on. (The default is live data)
    """
    data = get_live_database(db_connection)
    toggle_on = st.sidebar.toggle(
        label="Toggle for Archived Data", value=False, on_change=on_toggle_or_archive_change)
    if toggle_on:
        data = get_selected_archive()
    return data


def dashboard_header() -> None:
    """Creates a header for the dashboard and title on tab."""

    st.title("ONTHEB-RINK-OFEXTINCTION")
    st.markdown("An app for Liverpool Natural History Museum,\
                        #monitoring the health of our plants")


def plot_temp_for_plants(data_df) -> None:
    """creates a bar chart with temperature in y axis
    and the plant name in x axis.
    """
    st.title("Plant Temperature Bar Chart")
    st.write("Bar chart showing temperature values for different plants.")

    plt.figure(figsize=(10, 6))
    sns.barplot(x="species", y="temperature", data=data_df)
    plt.xlabel("Species")
    plt.ylabel("Temperature (°C)")
    plt.xticks(rotation=45)
    plt.title("Temperature Values for Different Plants")
    st.pyplot(plt)


def plot_soil_moisture_for_plants(data_df) -> None:
    """creates a bar chart with moisture in y axis
    and the plant name in x axis.
    """
    st.title("Plant Moisture Bar Chart")
    st.write("Bar chart showing Moisture values for different plants.")

    plt.figure(figsize=(10, 6))
    sns.barplot(x="species", y="soil_moisture", data=data_df)
    plt.xlabel("Species")
    plt.ylabel("Soil Moisture (%)")
    plt.xticks(rotation=45)
    plt.title("Soil Moisture Readings for Different Plants")
    st.pyplot(plt)


def handle_sidebar_options(plant_data_df) -> None:
    """Displays initial 10 rows of the data with options for next 10 and previous 10."""
    if "start_index" not in st.session_state:
        st.session_state.start_index = 0

    rows_to_show = 10

    with st.sidebar:
        st.sidebar.title("Pagination")
        if st.button("Show Previous 10 Rows"):
            st.session_state.start_index = max(
                0, st.session_state.start_index - rows_to_show)

        if st.button("Show Next 10 Rows"):
            st.session_state.start_index = min(st.session_state.start_index + rows_to_show,
                                               len(plant_data_df) - rows_to_show)

    data_to_show = plant_data_df[st.session_state.start_index:
                                 st.session_state.start_index + rows_to_show]
    plot_temp_for_plants(data_to_show)
    plot_soil_moisture_for_plants(data_to_show)


if __name__ == "__main__":
    st.set_page_config(page_title="Plant Monitoring Dashboard", layout="wide")
    load_dotenv()
    connection = get_db_connection()
    plant_data = switch_data(connection)
    dashboard_header()
    handle_sidebar_options(plant_data)
