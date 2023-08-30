"""Script for removing data older than 24 hours and saving older data to a .csv file."""

from datetime import datetime, timedelta
from pytz import timezone

from dotenv import dotenv_values
from psycopg2 import connect
import pandas as pd

CSV_COLUMNS = ["plant_entry_id", "species_id", "temperature", "soil_moisture", "humidity", "last_watered", "recording_taken", "sunlight_id", "botanist_id", "cycle_id"]


def get_database_connection(config: dict): # pragma: no cover
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
        exit()


def get_previous_day_timestamp() -> str:
    """Returns the timestamp of the previous day."""
    current_datetime = datetime.now(tz=timezone("Europe/London"))
    previous_day = current_datetime - timedelta(days=1)
    previous_day_str = datetime.strftime(previous_day, "%Y-%m-%d %H:%M:%S")
    return previous_day_str


def delete_old_rows(conn, delete_timestamp: str) -> list[tuple]: # pragma: no cover
    """Removes rows from the Plant table that are older than a day.

    Returns the deleted rows.
    """
    with conn.cursor() as cur:
        cur.execute(
            """DELETE FROM plant
            WHERE recording_taken < %s
            RETURNING *;""", (delete_timestamp,))
        deleted_rows = cur.fetchall()
        conn.commit()
        cur.close()
        return deleted_rows


def create_deleted_rows_dataframe(deleted_rows: list[tuple]) -> pd.DataFrame:
    """Returns a single DataFrame containing all the rows of the deleted data."""
    return pd.DataFrame(deleted_rows, columns=CSV_COLUMNS)


if __name__ == "__main__": # pragma: no cover
    configuration = dotenv_values()
    connection = get_database_connection(configuration)

    timestamp = get_previous_day_timestamp()
    list_deleted_rows = delete_old_rows(connection, timestamp)

    deleted_rows_df = create_deleted_rows_dataframe(list_deleted_rows)

