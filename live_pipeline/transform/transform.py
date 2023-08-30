import pandas as pd
import json


def create_dictionary_for_plant(raw_data: dict) -> dict:
    '''Dictionary created from extracted file'''
    plant_dict = {}
    plant_dict['Botanist Name'] = raw_data['botanist']['name']
    plant_dict['Botanist Email'] = raw_data['botanist']['email']
    plant_dict['Botanist Phone'] = raw_data['botanist']['phone']
    plant_dict['Last Watered'] = raw_data['last_watered']
    plant_dict['Plant Name'] = raw_data['name']
    if 'scientific_name' in raw_data.keys():
        plant_dict['Scientific Name'] = raw_data['scientific_name']
    else:
        plant_dict['Scientific Name'] = None

    plant_dict['Recording Time'] = raw_data['recording_taken']
    if 'cycle' in raw_data.keys():
        plant_dict['Cycle'] = raw_data['cycle']
    else:
        plant_dict['Cycle'] = None

    plant_dict['Temperature'] = raw_data['temperature']
    plant_dict['Soil Moisture'] = raw_data['soil_moisture']

    if 'sunlight' in raw_data.keys():
        plant_dict['Sunlight'] = raw_data['sunlight']
    else:
        plant_dict['Sunlight'] = None

    if 'humidity' in raw_data.keys():
        plant_dict['Humidity'] = raw_data['humidity']
    else:
        plant_dict['Humidity'] = None

    return plant_dict


if __name__ == "__main__":

    with open('plants.json', 'r') as f_obj:
        data = json.load(f_obj)

    all_plant_data = []
    for number in data.keys():
        transformed_plant = create_dictionary_for_plant(data[number])
        all_plant_data.append(transformed_plant)

    df = pd.DataFrame.from_dict(all_plant_data)
