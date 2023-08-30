""" Tests the functionality of the extract code."""
import pytest
import requests_mock
from extract import get_plants


def test_get_plants_successful():
    expected_data = {
        "botanist": {
            "email": "botanist@example.com",
            "name": "Botanist Name",
            "phone": "123-456-7890"
        },
        "last_watered": "2023-08-29T14:10:54Z",
        "name": "Test Plant",
        "origin_location": ["10.0", "20.0", "Location", "US", "America/New_York"],
        "plant_id": 1,
        "recording_taken": "2023-08-29T15:45:12Z",
        "soil_moisture": 75.0,
        "temperature": 25.0
    }

    with requests_mock.Mocker() as mocker:
        for plant_id in range(1, 51):
            mocker.get(
                f"https://data-eng-plants-api.herokuapp.com/plants/{plant_id}", json=expected_data, status_code=200)

        plants = get_plants()

        assert isinstance(plants, dict)
        assert len(plants) == 50
        assert all(plants[id] == expected_data for id in range(1, 51))
