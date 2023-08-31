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
            database='practice')
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


def add_botanist_information(conn, botanist_info: list):
    """Add botanist info to database"""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            """SELECT exists (SELECT 1 FROM botanist WHERE b_email = %s LIMIT 1);""",
            [botanist_info[3]])
        result = cur.fetchone()
        if result['exists'] is True:
            cur.close()
        elif result['exists'] is False:
            cur.execute(
                """INSERT INTO botanist(b_name, b_email, b_phone) VALUES 
                (%s, %s, %s)""", [botanist_info[2], botanist_info[3],
                                  botanist_info[4]])
        conn.commit()
        cur.close()


def add_species_information(conn, species_info: list):
    """Add species info to database"""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            """SELECT exists (SELECT 1 FROM species WHERE s_name = %s 
            LIMIT 1);""", [species_info[6]])
        result = cur.fetchone()
        if result['exists'] is True:
            cur.close()
        elif result['exists'] is False:
            cur.execute(
                """INSERT INTO species(s_name) VALUES (%s);""", [species_info[6]])
        conn.commit()
        cur.close()


def add_plant_information(conn, plant_record: list):
    """Add plant data to database"""
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            """SELECT sunlight_id FROM sunlight WHERE s_description = %s;""",
            [plant_record[12]])
        sunlight_id = cur.fetchone()['sunlight_id']
        cur.execute(
            """SELECT botanist_id FROM botanist WHERE b_email = %s;""",
            [plant_record[3]])
        botanist_id = cur.fetchone()['botanist_id']
        cur.execute(
            """SELECT cycle_id FROM cycle WHERE cycle_name = %s;""",
            [plant_record[9]])
        cycle_id = cur.fetchone()['cycle_id']
        cur.execute(
            """SELECT species_id FROM species WHERE s_name = %s;""",
            [plant_record[6]])
        species_id = cur.fetchone()['species_id']
        cur.execute(
            """INSERT INTO plant(species_id, temperature, soil_moisture, 
            last_watered, recording_taken, sunlight_id, botanist_id, cycle_id)
              VALUES (%s, %s, %s, %s, %s, %s, %s, %s);""",
            [species_id, plant_record[10], plant_record[11], plant_record[5],
             plant_record[8], sunlight_id, botanist_id, cycle_id])
        conn.commit()
        cur.close()
