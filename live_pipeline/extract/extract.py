"""
Extract the plant data from the api into a dictionary.
Exports found data to Json is there to make it easy to view but can be removed.
Exports missing data to json for logging purposes. (Useful to keep)
"""
from datetime import datetime
import json
import time
import requests


def log_missing(plant_id: int, missing_plants: dict) -> None:
    """Logs the missing plant id and the current datetime to a json file."""

    current_datetime = datetime.now()
    missing_plants[str(current_datetime)
                   ] = f"Data not found for plant_id {plant_id}"

    with open("missing_plants", 'w') as file:
        json.dump(missing_plants, file, indent=4)


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
        for plant_id in range(1, 51):
            response = requests.get(
                f"https://data-eng-plants-api.herokuapp.com/plants/{plant_id}")
            if response.status_code == 200:
                json = response.json()
                print(plant_id)
                plants[plant_id] = json
            elif response.status_code == 404:
                log_missing(plant_id, missing_plants)
            elif response.status_code == 500:
                raise APIError("Unable to connect to server.", code=500)

        return plants
    except requests.exceptions.RequestException as err:
        raise APIError(f"An exception occurred - {str(err)}")


if __name__ == "__main__":
    start = time.time()

    data = get_plants()
    with open("plants", 'w') as plant_file:
        json.dump(data, plant_file, indent=4)

    print(time.time() - start)
