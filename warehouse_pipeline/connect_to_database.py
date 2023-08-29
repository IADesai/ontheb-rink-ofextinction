'''libraries required to connect to database'''
import psycopg2
from dotenv import dotenv_values


def get_db_connection(config):
    '''connect to the database with pokemon data'''
    try:
        return psycopg2.connect(
            user=config['DATABASE_USERNAME'],
            password=config['DATABASE_PASSWORD'],
            host=config['DATABASE_IP'],
            port=config['DATABASE_PORT'],
            database=config['INITIAL_DATABASE'])
    except ValueError:
        return "Error connecting to database."


if '__name__' == '__main__':
    config = dotenv_values()
    conn = get_db_connection(config)
