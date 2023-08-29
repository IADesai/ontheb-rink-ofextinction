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
    except ValueError:
        return "Error connecting to database."


if __name__ == "__main__": # pragma: no cover
    configuration = dotenv_values()
    connection = get_database_connection(configuration)
