'''libraries required to connect to database'''
import psycopg2
import psycopg2.extras
from dotenv import dotenv_values


def get_db_connection(config):
    '''connect to the database with pokemon data'''
    try:
        return psycopg2.connect(
            user=config['DATABASE_USERNAME'],
            password=config['DATABASE_PASSWORD'],
            host=config['DATABASE_IP'],
            port=config['DATABASE_PORT'],
            database=config['DATABASE_NAME'])
    except ValueError:
        return "Error connecting to database."


def add_cycle_information(conn, cycle_name):
    '''function to add data from psql'''
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(
            """SELECT exists (SELECT 1 FROM cycle WHERE cycle_name = %s LIMIT 1);""", [cycle_name])
        result = cur.fetchone()
        if result['exists'] == True:
            cur.close()
        elif result['exists'] == False:
            cur.execute(
                """INSERT INTO cycle(cycle_name) VALUES (%s)""", [cycle_name])
        conn.commit()
        cur.close()


if __name__ == '__main__':
    config = dotenv_values()
    conn = get_db_connection(config)
