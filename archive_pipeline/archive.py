"""Script for removing data older than 24 hours and saving older data to a .csv file."""

import sys
import os
from datetime import datetime, timedelta, date
from pytz import timezone


from dotenv import dotenv_values
from psycopg2 import connect
import pandas as pd
from boto3 import client

CSV_COLUMNS = ["entry_id", "species", "temperature", "soil_moisture",
               "humidity", "last_watered", "recording_taken", "sunlight",
               "botanist_name", "cycle"]


def get_database_connection(config: dict):  # pragma: no cover
    """Establishes a connection with the PostgreSQL database."""
    try:
        return connect(
            user=config['DATABASE_USERNAME'],
            password=config['DATABASE_PASSWORD'],
            host=config['DATABASE_IP'],
            port=config['DATABASE_PORT'],
            database=config['DATABASE_NAME'])
    except ValueError as err:
        print("Error connecting to database: ", err)
        sys.exit()


def get_previous_day_timestamp() -> str:
    """Returns the timestamp of the previous day."""
    current_datetime = datetime.now(tz=timezone("Europe/London"))
    previous_day = current_datetime - timedelta(days=1)
    previous_day_str = datetime.strftime(previous_day, "%Y-%m-%d %H:%M:%S")
    return previous_day_str


def delete_old_rows(conn, delete_timestamp: str) -> list[tuple]:  # pragma: no cover
    """Removes rows from the Plant table that are older than a day.

    Returns the deleted rows.
    """
    with conn.cursor() as cur:
        print("Deleting rows from RDS.")
        cur.execute(
            """DELETE FROM plant
            WHERE recording_taken < %s
            RETURNING *;""", (delete_timestamp,))
        deleted_rows = cur.fetchall()
        conn.commit()
        cur.close()
        print("Rows deleted from RDS.")
        return deleted_rows


def get_deleted_rows(conn, delete_timestamp: str) -> list[tuple]:  # pragma: no cover
    """Returns the rows that were recorded more than a day ago."""
    with conn.cursor() as cur:
        print("Fetching data to archive from RDS.")
        cur.execute("""
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
            LEFT JOIN cycle c ON p.cycle_id = c.cycle_id
            WHERE recording_taken < %s;""", (delete_timestamp,))
        deleted_rows = cur.fetchall()
        conn.commit()
        cur.close()
        print("Archive data fetched from RDS.")
        return deleted_rows


def select_and_delete_from_db(conn, delete_timestamp: str, configuration: dict) -> list[tuple]:  # pragma: no cover
    """Removes rows from the plant table that are older than a day.

    SELECT is performed to maintain consistency with live databatase interactions in the dashboard.
    Returns the deleted rows.
    """
    rows_to_delete = get_deleted_rows(conn, delete_timestamp)

    deleted_rows_df = create_deleted_rows_dataframe(rows_to_delete)
    archived_csv_filename = create_csv_filename()
    create_archived_csv_file(deleted_rows_df, archived_csv_filename)
    upload_csv_to_s3(archived_csv_filename, configuration)

    deleted_rows = delete_old_rows(conn, delete_timestamp)

    if len(rows_to_delete) != len(deleted_rows):
        print("Inconsistency between rows being deleted and rows being archived. " +
              "Script will continue.")
    return rows_to_delete


def create_deleted_rows_dataframe(deleted_rows: list[tuple]) -> pd.DataFrame:
    """Returns a single DataFrame containing all the rows of the deleted data."""
    archive_df = pd.DataFrame(deleted_rows, columns=CSV_COLUMNS)
    if archive_df.empty:
        raise ValueError("Empty DataFrame.")
    return archive_df


def create_csv_filename() -> str:
    """Creates a filename for a .csv file with the previous day's date."""
    today_date = date.today()
    yesterday_date = today_date - timedelta(days=1)
    yesterday_date_str = datetime.strftime(yesterday_date, "%Y_%m_%d")
    return "archived_" + yesterday_date_str + ".csv"


def create_archived_csv_file(archived_df: pd.DataFrame, csv_filename: str) -> None:
    """Creates a .csv file from a Pandas dataframe."""
    if os.path.exists(csv_filename):
        print(f"A file already exists locally with the name {csv_filename}. " +
              "This file will be overwritten.")
    archived_df.to_csv(csv_filename, index=False)


def upload_csv_to_s3(csv_filename: str, config: dict) -> None:  # pragma: no cover
    """Uploads the created .csv file to an S3 bucket."""
    print("Establishing connection to AWS.")
    s3_client = client("s3", aws_access_key_id=config["ACCESS_KEY_ID"],
                       aws_secret_access_key=config["SECRET_ACCESS_KEY"])
    print("Connection established.")
    print("Uploading .csv file.")
    s3_client.upload_file(
        csv_filename, config["ARCHIVE_BUCKET_NAME"], csv_filename)
    print(".csv file uploaded.")


if __name__ == "__main__":  # pragma: no cover
    configuration = dotenv_values()
    connection = get_database_connection(configuration)

    timestamp = get_previous_day_timestamp()
    select_and_delete_from_db(connection, timestamp, configuration)
