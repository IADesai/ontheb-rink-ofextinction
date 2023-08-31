"""Libraries required for loading"""
from os import environ
from dotenv import load_dotenv
import pandas as pd

from database_functions import get_db_connection, add_cycle_information, add_botanist_information, add_species_information, add_plant_information

if __name__ == '__main__':

    load_dotenv()
    configuration = environ
    connection = get_db_connection(configuration)

    df = pd.read_csv("practice.csv")
    for row in df.itertuples():
        cycle = row[9]
        add_cycle_information(connection, cycle)
        add_botanist_information(connection, row)
        add_species_information(connection, row)
        add_plant_information(connection, row)
