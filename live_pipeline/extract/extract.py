"""
Extract the plant data from the api into a dictionary.
Exports found data to Json is there to make it easy to view but can be removed.
Exports missing data to json for logging purposes. (Useful to keep)
"""
from datetime import datetime
import json
import time
import requests
import aiohttp
import asyncio


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


async def plant_get_request(url: str, session, plant_id: int, missing_plants: dict) -> dict:
    """Performs a GET request for a plant."""
    req = await session.request("GET", url=url)
    if req.status == 200:
        req_data = {plant_id: await req.json()}
        return req_data
    print(f"Plant id: {plant_id}, Status: {req.status}")
    logs(plant_id, missing_plants, req.status)


async def parallel_requests() -> list[dict]:
    """Creates the instructions for a GET request for each plant."""
    missing_plants = {}
    try:
        async with aiohttp.ClientSession() as session:
            tasks = []
            for plant_id in range(START_ID, END_ID):
                url = f"{URL}{plant_id}"
                tasks.append(plant_get_request(
                    url=url, session=session, plant_id=plant_id, missing_plants=missing_plants))
            results = await asyncio.gather(*tasks, return_exceptions=True)
            return results
    except requests.exceptions.RequestException as err:
        raise APIError(f"An exception occurred - {str(err)}")


def transform_plants_list_to_dict(plant_data_list: list[dict]) -> dict:
    """Converts a list of dictionaries to a single dictionary."""
    new_data = {}
    for d in plant_data_list:
        if d:
            for k in d.keys():
                new_data[k] = d[k]
    return new_data


if __name__ == "__main__":
    start = time.time()

    plant_data = asyncio.run(parallel_requests())
    plant_data_dict = transform_plants_list_to_dict(plant_data)

    with open("plants_refactor.json", 'w') as plant_file:
        json.dump(plant_data_dict, plant_file, indent=4)

    print(time.time() - start)
