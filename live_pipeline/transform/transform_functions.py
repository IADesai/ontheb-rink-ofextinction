"""libraries required for transformation functions"""
from datetime import datetime as dt
from os import environ
import json
from boto3 import client
from dotenv import load_dotenv


LOWER_TEMP_LIMIT = 9
UPPER_TEMP_LIMIT = 40
LOWER_SOIL_LIMIT = 21
UPPER_SOIL_LIMIT = 40


def create_dictionary_for_plant(raw_data: dict) -> dict:
    """Dictionary created from extracted file"""
    plant_dict = {}
    plant_dict['Botanist_Name'] = raw_data['botanist']['name']
    plant_dict['Botanist_Email'] = raw_data['botanist']['email']
    plant_dict['Botanist_Phone'] = raw_data['botanist']['phone']
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
    if type(raw_data['temperature']) != float:
        try:
            plant_dict['Temperature'] = float(raw_data['temperature'])
        except:
            plant_dict['Temperature'] = '-'
    else:
        plant_dict['Temperature'] = raw_data['temperature']

    if 'soil_moisture' not in raw_data.keys():
        plant_dict['Soil_Moisture'] = '-'
    if type(raw_data['soil_moisture']) != float:
        try:
            plant_dict['Soil_Moisture'] = float(raw_data['soil_moisture'])
        except:
            plant_dict['Soil_Moisture'] = '-'

    plant_dict['Soil_Moisture'] = raw_data['soil_moisture']

    if 'sunlight' not in raw_data.keys():
        plant_dict['Sunlight'] = '-'
    else:
        sun_choices = ''
        if len(raw_data['sunlight']) > 1:
            for sun_type in sorted(raw_data['sunlight']):
                sun_choices += sun_type.lower() + ', '
            sun_choices = sun_choices[:-2]
        else:
            sun_choices = raw_data['sunlight'][0].lower()

        plant_dict['Sunlight'] = sun_choices

    if 'humidity' in raw_data.keys():
        plant_dict['Humidity'] = raw_data['humidity']
    else:
        plant_dict['Humidity'] = '-'

    return plant_dict


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
        return dt.strptime(date, '%Y-%m-%d %H:%M:%S')
    except ValueError:
        return None


def validate_time_for_last_watered(date: dt) -> dt | str:
    """Check datetime for last watered is valid"""
    try:
        return dt.strptime(date, '%a, %d %b %Y %H:%M:%S %Z')
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
                   aws_secret_access_key=config["SECRET_ACCESS_KEY"])
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
