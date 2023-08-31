"""libraries required for transformation"""
import pandas as pd
import json

from transform_functions import create_list_for_data, validate_time_for_last_watered, validate_time_for_time_recorded, check_temperature_within_correct_ranges, check_soil_moisture_within_correct_ranges, delete_rows_containing_invalid_data, send_alerts_for_abnormal_results


if __name__ == "__main__":

    with open('plants.json', 'r', encoding='utf-8') as f_obj:
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

    clean_df.to_csv('clean_data.csv')
