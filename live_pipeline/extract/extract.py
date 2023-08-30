"""
Extract the plant data from the api into a dictionary.
Exports found data to Json is there to make it easy to view but can be removed.
Exports missing data to json for logging purposes. (Useful to keep)
"""
from datetime import datetime
import json
import time
import requests

"""
I'd log the error if a single endpoint returns 500. 
If the transform stage is being started but the dictionary being passed in is empty, 
this should stop the pipeline script from running (and alert/log something)
"""

START_ID = 1
END_ID = 51
URL = f"https://data-eng-plants-api.herokuapp.com/plants/"


def logs(plant_id: int, missing_plants: dict, code: int) -> None:
    """Logs the missing plant id and the current datetime to a json file."""

    current_datetime = datetime.now()

    if code == 404:
        missing_plants[str(current_datetime)
                       ] = f"Data not found for plant_id {plant_id}, 404"
    elif code == 500:
        missing_plants[str(current_datetime)
                       ] = f"Server error for plant_id {plant_id}, 500"

    try:
        with open("missing_plants.json", 'w') as file:
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
                json = response.json()
                plants[plant_id] = json
            elif response.status_code == 404:
                logs(plant_id, missing_plants, response.status_code)
            elif response.status_code == 500:
                print(f"500 for {plant_id}")
                logs(plant_id, missing_plants, response.status_code)

        return plants
    except requests.exceptions.RequestException as err:
        raise APIError(f"An exception occurred - {str(err)}")


if __name__ == "__main__":
    start = time.time()

    data = get_plants()
    with open("plants.json", 'w') as plant_file:
        json.dump(data, plant_file, indent=4)

    print(time.time() - start)
