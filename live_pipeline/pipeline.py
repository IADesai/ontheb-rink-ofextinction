"""libraries needed for the overall pipeline script"""
import json
import time
from os import environ
from dotenv import load_dotenv
import pandas as pd

from pipeline_functions import get_plants, create_list_for_data, validate_time_for_last_watered, validate_time_for_time_recorded, check_temperature_within_correct_ranges, check_soil_moisture_within_correct_ranges, delete_rows_containing_invalid_data, send_alerts_for_abnormal_results, get_db_connection, add_cycle_information, add_botanist_information, add_species_information, add_plant_information


def handler(event=None, context=None):
    """Contains all the functions required to complete extract, transform and load"""
    start = time.time()

    data = get_plants()
    with open("/tmp/plants.json", 'w', encoding="utf-8") as plant_file:
        json.dump(data, plant_file, indent=4)

    print(time.time() - start)

    with open('/tmp/plants.json', 'r', encoding="utf-8") as f_obj:
        data = json.load(f_obj)

    all_plants = create_list_for_data(data)

    data_frame = pd.DataFrame.from_dict(all_plants)

    data_frame['Botanist_Name'] = data_frame['Botanist_Name'].apply(
        lambda x: x.title())

    data_frame['Last_Watered'] = data_frame['Last_Watered'].map(
        validate_time_for_last_watered)

    data_frame['Recording_Time'] = data_frame['Recording_Time'].map(
        validate_time_for_time_recorded)

    data_frame['Temperature'] = data_frame['Temperature'].map(
        check_temperature_within_correct_ranges)

    data_frame['Soil_Moisture'] = data_frame['Soil_Moisture'].map(
        check_soil_moisture_within_correct_ranges)

    clean_df = delete_rows_containing_invalid_data(data_frame)

    send_alerts_for_abnormal_results(clean_df)

    clean_df.to_csv('clean_data.csv')

    load_dotenv()
    configuration = environ
    connection = get_db_connection(configuration)

    data_frame = pd.read_csv("/tmp/clean_data.csv")
    for row in data_frame.itertuples():
        cycle = row[9]
        add_cycle_information(connection, cycle)
        add_botanist_information(connection, row)
        add_species_information(connection, row)
        add_plant_information(connection, row)

    print(time.time() - start)
    return {'status': "success"}


if __name__ == "__main__":

    handler(None, None)
