import pytest
from extract import get_plants, APIError
import requests_mock


def test_get_plants_raises_500_error():
    """Checks that get_plants raises the correct error upon a 500 response."""
    plant_id = 1
    with requests_mock.Mocker() as mocker:
        mocker.get(
            f"https://data-eng-plants-api.herokuapp.com/plants/{plant_id}", status_code=500)
        with pytest.raises(APIError) as exception:
            get_plants()

        assert exception.value.message == "Unable to connect to server."
        assert exception.value.code == 500


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
