"""Pipeline script containing all of extract, transform and load, created for AWS Lambda.
    Libraries required for pipeline function"""
from datetime import datetime as dt
from os import environ
import json
import requests
import pytz
from boto3 import client
from dotenv import load_dotenv
from psycopg2 import connect
from psycopg2.extras import RealDictCursor


START_ID = 1
END_ID = 51
URL = f"https://data-eng-plants-api.herokuapp.com/plants/"
LOWER_TEMP_LIMIT = 8
UPPER_TEMP_LIMIT = 40
LOWER_SOIL_LIMIT = 21


def logs(plant_id: int, missing_plants: dict, code: int) -> None:
    """Logs the missing plant id and the current datetime to a json file."""

    current_datetime = dt.now()

    if code == 404:
        missing_plants[str(current_datetime)
                       ] = f"Data not found for plant_id {plant_id}, 404"
    elif code == 500:
        missing_plants[str(current_datetime)
                       ] = f"Server error for plant_id {plant_id}, 500"

    try:
        with open("/tmp/missing_plants.json", 'w') as file:
            json.dump(missing_plants, file, indent=4)
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")


class APIError(Exception):
    """Describes an error triggered by a failing API call."""

    def __init__(self, message: str, code: int = 500):
        """Creates a new APIError instance."""
        self.message = message
        self.code = code


def get_plants() -> dict:
    """ Hit's each endpoint and fetches all the available plant data"""
    plants = {}
    missing_plants = {}
    try:
        for plant_id in range(START_ID, END_ID):
            response = requests.get(
                f"{URL}{plant_id}")
            if response.status_code == 200:
                json_file = response.json()
                plants[plant_id] = json_file
            elif response.status_code == 404:
                logs(plant_id, missing_plants, response.status_code)
            elif response.status_code == 500:
                print(f"500 for {plant_id}")
                logs(plant_id, missing_plants, response.status_code)

        return plants
    except requests.exceptions.RequestException as err:
        raise APIError(f"An exception occurred - {str(err)}")


def create_dictionary_for_plant(raw_data: dict) -> dict:
    """Dictionary created from extracted file"""
    plant_dict = {}
    plant_dict['Botanist_Name'] = raw_data['botanist']['name']
    plant_dict['Botanist_Email'] = raw_data['botanist']['email']
    plant_dict['Botanist_Phone'] = str(raw_data['botanist']['phone'])
    plant_dict['Last_Watered'] = raw_data['last_watered']
    plant_dict['Plant_Name'] = raw_data['name']

    if 'scientific_name' in raw_data.keys():
        plant_dict['Scientific_Name'] = raw_data['scientific_name'][0]
    else:
        plant_dict['Scientific_Name'] = '-'

    plant_dict['Recording_Time'] = raw_data['recording_taken']

    if 'cycle' not in raw_data.keys():
        plant_dict['Cycle'] = '-'
    else:
        plant_dict['Cycle'] = raw_data['cycle']

    if 'temperature' not in raw_data.keys():
        plant_dict['Temperature'] = '-'
    else:
        temperature = validate_float(raw_data['temperature'])
        plant_dict['Temperature'] = temperature

    if 'soil_moisture' not in raw_data.keys():
        plant_dict['Soil_Moisture'] = '-'
    else:
        soil_moisture = validate_float(raw_data['soil_moisture'])
        plant_dict['Soil_Moisture'] = soil_moisture

    if 'sunlight' not in raw_data.keys():
        plant_dict['Sunlight'] = '-'
    else:
        sun_choices = format_sun_choices(raw_data['sunlight'])
        plant_dict['Sunlight'] = sun_choices

    return plant_dict


def format_sun_choices(sunlight: list) -> str:
    """Takes list of sunlight given and formats to string"""
    sun_choices = ''
    if len(sunlight) > 1:
        for sun_type in sorted(sunlight):
            sun_choices += sun_type.lower() + ', '
        if sun_choices[0] == ' ':
            sun_choices = sun_choices[1:]
        sun_choices = sun_choices[:-2]
    else:
        sun_choices = sunlight[0].lower()

    return sun_choices


def validate_float(float_variable: float) -> float | str:
    """Function to ensure temperature is correctly formatted"""
    if float_variable != float:
        try:
            float_variable = float(float_variable)
        except ValueError:
            float_variable = '-'

    return float_variable


def create_list_for_data(plant_data: json) -> list:
    """Create list for all plant data ready for a dataframe"""
    all_plant_data = []
    for number in plant_data.keys():
        transformed_plant = create_dictionary_for_plant(plant_data[number])
        all_plant_data.append(transformed_plant)
    return all_plant_data


def validate_time_for_time_recorded(date: dt) -> dt | str:
    """Checks whether datetime is appropriate"""
    try:
        date = dt.strptime(date, '%Y-%m-%d %H:%M:%S')
        return date.astimezone(pytz.timezone(("Europe/London")))
    except ValueError:
        return None


def validate_time_for_last_watered(date: dt) -> dt | str:
    """Check datetime for last watered is valid"""
    try:
        date = dt.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')
        return date.astimezone(pytz.timezone(("Europe/London")))
    except ValueError:
        return None


def check_temperature_within_correct_ranges(temperature: float) -> float | str:
    """Marks out invalid temperatures, those unlikely to be a fluctuation"""
    if temperature < LOWER_TEMP_LIMIT - 5:
        return None
    if temperature > UPPER_TEMP_LIMIT + 5:
        return None

    return temperature


def check_soil_moisture_within_correct_ranges(soil_moisture: float) -> float | str:
    """Marks out invalid temperatures, those unlikely to be a fluctuation"""
    if soil_moisture < LOWER_SOIL_LIMIT - 5:
        return None

    return soil_moisture


def delete_rows_containing_invalid_data(dataframe: object) -> object:
    """Removal of invalid rows of data"""
    return dataframe.dropna(how='any', axis=0)


def send_alert(config, task: str, message: str):
    """Sends alert email to the relevant botanist"""

    if not isinstance(task, str):
        raise ValueError("Task should be a string")
    if not isinstance(message, str):
        raise ValueError("Message should be a string")
    email = client('ses', aws_access_key_id=config["ACCESS_KEY_ID"],
                   aws_secret_access_key=config["SECRET_ACCESS_KEY"], region_name='eu-west-2')
    email.send_email(
        Source=config["EMAIL"],
        Destination={
            'ToAddresses': [
                config["EMAIL"],
            ]
        },
        Message={
            'Subject': {
                'Data': f'{task}',
            },
            'Body': {
                'Html': {
                    'Data': f'{message}',
                }
            }
        }
    )


def send_alerts_for_abnormal_results(dataframe: object) -> object:
    """Compares temperature to hard-coded ranges"""
    load_dotenv()
    config = environ

    for row in dataframe.itertuples():
        temperature = row[9]
        soil_moisture = row[10]
        if temperature < LOWER_TEMP_LIMIT:
            send_alert(config, 'ALERT: Temperature too low!',
                       f'Temperature for {row[5]} was noted to be low at {temperature}.')
        if temperature > UPPER_TEMP_LIMIT:
            send_alert(config, 'ALERT: Temperature too high!',
                       f'Temperature for {row[5]} was noted to be high at {temperature}.')
        if soil_moisture < LOWER_SOIL_LIMIT - 5:
            send_alert(config, 'ALERT: Soil moisture too low!',
                       f'Soil moisture for {row[5]} was noted to be high at {soil_moisture}.')


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
