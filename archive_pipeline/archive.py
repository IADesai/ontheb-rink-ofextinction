"""Script for removing data older than 24 hours and saving older data to a .csv file."""

from dotenv import dotenv_values
from psycopg2 import connect
from psycopg2.extras import RealDictCursor


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


def delete_old_rows(conn, delete_timestamp: str) -> dict:
    """Removes rows from the Plant table that are older than a day.

    Returns the deleted rows.
    """
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            """DELETE FROM plant
            WHERE recording_taken < %s
            RETURNING *;""", delete_timestamp)
        deleted_rows = cur.fetchall()
        conn.commit()
        cur.close()
        return deleted_rows


if __name__ == "__main__": # pragma: no cover
    configuration = dotenv_values()
    connection = get_database_connection(configuration)
