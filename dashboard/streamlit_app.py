"""Streamlit dashboard application code"""
import os
from os import environ
import streamlit as st
import pandas as pd
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
    st.sidebar.title("ONTHEB-RINK-OFEXTINCTION")
    st.sidebar.markdown("An app for Liverpool Natural History Museum,\
                        monitoring the health of our plants")

    data = get_live_data(db_connection)

    toggle_on = st.sidebar.toggle(label="Toggle for Archived Data", value=False, )
    if toggle_on:
        data = get_archived_data()

    with st.sidebar.expander("Expand to see information about the plants"):
        st.markdown("Lorem Ipsum")
    return data


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

    plant_data = sidebar(conn)

    st.markdown(plant_data.style.hide(axis="index").to_html(), unsafe_allow_html=True)
