""" 
This module glues the extract_s3 and streamlit files into one 
so that it can be run with a single command.
"""
from os import environ
from dotenv import load_dotenv
from boto3 import client

from extract_s3 import download_csv_files_
from streamlit_app import get_db_connection, switch_data, dashboard_header, handle_sidebar_options


if __name__ == "__main__":

    load_dotenv()

    s3 = client("s3",
                aws_access_key_id=environ.get("ACCESS_KEY_ID"),
                aws_secret_access_key=environ.get("SECRET_ACCESS_KEY")
                )

    download_csv_files_(
        s3, environ.get("BUCKET_NAME"), "archived", ".csv", "archived_data")

    connection = get_db_connection()
    plant_data = switch_data(connection)
    dashboard_header()
    handle_sidebar_options(plant_data)
