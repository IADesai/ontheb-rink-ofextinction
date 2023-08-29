"""libraries required to connect to database"""
from psycopg2 import connect
from psycopg2.extras import RealDictCursor


def get_db_connection(config):
    """Connect to the database with plant data"""
    try:
        return connect(
            user=config['DATABASE_USERNAME'],
            password=config['DATABASE_PASSWORD'],
            host=config['DATABASE_IP'],
            port=config['DATABASE_PORT'],
            database=config['DATABASE_NAME'])
    except ValueError:
        return "Error connecting to database."


def add_cycle_information(conn, cycle_name: str):
    """Add cycle data to database"""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            """SELECT exists (SELECT 1 FROM cycle WHERE cycle_name = %s LIMIT 1);""", [cycle_name])
        result = cur.fetchone()
        if result['exists'] is True:
            cur.close()
        elif result['exists'] is False:
            cur.execute(
                """INSERT INTO cycle(cycle_name) VALUES (%s)""", [cycle_name])
        conn.commit()
        cur.close()


def add_botanist_information(conn, botanist_info: dict):
    """Add botanist info to database"""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            """SELECT exists (SELECT 1 FROM botanist WHERE b_email = %s LIMIT 1);""",
            botanist_info['email'])
        result = cur.fetchone()
        if result['exists'] is True:
            cur.close()
        elif result['exists'] is False:
            cur.execute(
                """INSERT INTO botanist(b_name, b_email, b_phone) VALUES 
                (%s, %s, %s)""", [botanist_info['name'], botanist_info['email'],
                                  botanist_info['phone']])
        conn.commit()
        cur.close()


def add_species_information(conn, species_info: dict):
    """Add species info to database"""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            """SELECT exists (SELECT 1 FROM species WHERE scientific_name = %s 
            LIMIT 1);""", [species_info['scientific_name']])
        result = cur.fetchone()
        if result['exists'] is True:
            cur.close()
        elif result['exists'] is False:
            cur.execute(
                """INSERT INTO species(scientific_name) VALUES (%s);""", [species_info['name']])
        conn.commit()
        cur.close()


def add_plant_information(conn, plant_record: dict):
    """Add plant data to database"""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            """SELECT sunlight_id FROM sunlight WHERE s_description = %s;""",
            [plant_record['sunlight']])
        sunlight_id = cur.fetchone()['sunlight_id']
        cur.execute(
            """SELECT botanist_id FROM botanist WHERE b_email = %s;""",
            [plant_record['botanist']])
        botanist_id = cur.fetchone()['botanist_id']
        cur.execute(
            """SELECT cycle_id FROM cycle WHERE cycle_id = %s;""",
            [plant_record['cycle']])
        cycle_id = cur.fetchone()['cycle_id']

        cur.execute(
            """INSERT INTO plant(temperature, soil_moisture, humidity, 
            last_watered, recording_taken, sunlight_id, botanist_id, cycle_id)
              VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""",
            plant_record['temp'], plant_record['soil_moisture'],
            plant_record['humidity'], plant_record['last_watered'],
            plant_record['recording_taken'], sunlight_id, botanist_id, cycle_id)
        conn.commit()
        cur.close()
