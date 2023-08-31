"""libraries needed for the overall pipeline script"""
import json
import time
from dotenv import load_dotenv
from os import environ
import pandas as pd

from pipeline_functions import get_plants, create_list_for_data, validate_time_for_last_watered, validate_time_for_time_recorded, check_temperature_within_correct_ranges, check_soil_moisture_within_correct_ranges, delete_rows_containing_invalid_data, send_alerts_for_abnormal_results, get_db_connection, add_cycle_information, add_botanist_information, add_species_information, add_plant_information


def handler(event=None, context=None):
    """Contains all the functions required to complete extract, transform and load"""
    start = time.time()

    data = get_plants()
    with open("/tmp/plants.json", 'w') as plant_file:
        json.dump(data, plant_file, indent=4)

    print(time.time() - start)

    with open('/tmp/plants.json', 'r', encoding='utf-8') as f_obj:
        data = json.load(f_obj)

    all_plants = create_list_for_data(data)

    df = pd.DataFrame.from_dict(all_plants)

    df['Botanist_Name'] = df['Botanist_Name'].apply(
        lambda x: x.title())

    df['Last_Watered'] = df['Last_Watered'].apply(
        lambda x: validate_time_for_last_watered(x))

    df['Recording_Time'] = df['Recording_Time'].apply(
        lambda x: validate_time_for_time_recorded(x))

    df['Temperature'] = df['Temperature'].apply(
        lambda x: check_temperature_within_correct_ranges(x))

    df['Soil_Moisture'] = df['Soil_Moisture'].apply(
        lambda x: check_soil_moisture_within_correct_ranges(x))

    clean_df = delete_rows_containing_invalid_data(df)

    send_alerts_for_abnormal_results(clean_df)

    clean_df.to_csv('/tmp/clean_data.csv')

    load_dotenv()
    configuration = environ
    connection = get_db_connection(configuration)

    df = pd.read_csv("/tmp/clean_data.csv")
    for row in df.itertuples():
        cycle = row[9]
        add_cycle_information(connection, cycle)
        add_botanist_information(connection, row)
        add_species_information(connection, row)
        add_plant_information(connection, row)

    print(time.time() - start)
    return {'status': "success"}


if __name__ == "__main__":

    handler()
