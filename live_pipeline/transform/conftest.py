"""Libraries required for testing"""
import pytest
import pandas as pd


@pytest.fixture
def fake_raw_plant_data():
    return {
        "botanist": {
            "email": "fake_person@lnhm.co.uk",
            "name": "Fake Person",
            "phone": "001-481-273-3691x134"
        },
        "last_watered": "Wed, 30 Aug 2023 13:54:32 GMT",
        "name": "Fake plant",
        "origin_location": [
            "7.55",
            "-118.03917",
            "Fake location",
            "Fake",
            "Continent/Fake"
        ],
        "plant_id": 532,
        "recording_taken": "2023-08-30 14:56:09",
        "temperature": "12.070482937725064"
    }


@pytest.fixture
def fake_sunlight_options():
    return ['fake sun', 'fake SHade']


@pytest.fixture
def fake_float_valid():
    return "23.47257"


@pytest.fixture
def fake_float_invalid():
    return "invalid_fake"


@pytest.fixture
def fake_data():
    return {
        "1": {
            "botanist": {
                "email": "fake_person@lnhm.co.uk",
                "name": "Fake Person",
                "phone": "001-481-273-3691x134"
            },
            "last_watered": "Wed, 30 Aug 2023 13:54:32 GMT",
            "name": "Fake plant",
            "origin_location": [
                "7.55",
                "-118.03917",
                "Fake location",
                "Fake",
                "Continent/Fake"
            ],
            "plant_id": 532,
            "recording_taken": "2023-08-30 14:56:09",
            "soil_moisture": 96.36114621062993,
            "temperature": "12.070482937725064"
        },
        "2": {
            "botanist": {
                "email": "fake_person@lnhm.co.uk",
                "name": "Fake Person",
                "phone": "001-481-273-3691x134"
            },
            "last_watered": "Wed, 30 Aug 2023 13:54:32 GMT",
            "name": "Fake plant",
            "origin_location": [
                "7.55",
                "-118.03917",
                "Fake location",
                "Fake",
                "Continent/Fake"
            ],
            "plant_id": 532,
            "recording_taken": "2023-08-30 14:56:09",
            "soil_moisture": 96.36114621062993,
            "temperature": "12.070482937725064"
        }}


@pytest.fixture
def fake_time_recorded():
    return "2023-08-30 14:56:09"


@pytest.fixture
def fake_time_recorded_invalid():
    return "2023-13-30 14:56:09"


@pytest.fixture
def fake_last_watered():
    return "Wed, 30 Aug 2023 14:10:54 GMT"


@pytest.fixture
def fake_temperature_valid():
    return 25.3252


@pytest.fixture
def fake_temperature_invalid():
    return 100.32536


@pytest.fixture
def fake_soil_moisture_valid():
    return 80.000352


@pytest.fixture
def fake_dataframe():
    return pd.DataFrame.from_dict([{'Botanist_Name': 'Gertrude Jekyll', 'Botanist_Email': 'gertrude.jekyll@lnhm.co.uk', 'Botanist_Phone': '001-481-273-3691x127', 'Last_Watered': 'Wed, 30 Aug 2023 13:54:32 GMT', 'Plant_Name': 'Venus flytrap', 'Scientific_Name': '-', 'Recording_Time': '2023-08-30 14:56:09', 'Cycle': '-', 'Temperature': 12.070482937725064, 'Soil_Moisture': None, 'Sunlight': '-', 'Humidity': '-'},
                                   {'Botanist_Name': 'Carl Linnaeus', 'Botanist_Email': 'carl.linnaeus@lnhm.co.uk', 'Botanist_Phone': '(146)994-1635x35992', 'Last_Watered': 'Wed, 30 Aug 2023 14:10:54 GMT', 'Plant_Name': 'Corpse flower',
                                    'Scientific_Name': '-', 'Recording_Time': '2023-08-30 14:56:10', 'Cycle': '-', 'Temperature': 9.23359483252033, 'Soil_Moisture': 97.52850705914467, 'Sunlight': '-', 'Humidity': '-'},
                                   {'Botanist_Name': 'Eliza Andrews', 'Botanist_Email': 'eliza.andrews@lnhm.co.uk', 'Botanist_Phone': '(846)669-6651x75948', 'Last_Watered': 'Wed, 30 Aug 2023 14:50:16 GMT', 'Plant_Name': 'Rafflesia arnoldii',
                                    'Scientific_Name': '-', 'Recording_Time': '2023-08-30 14:56:11', 'Cycle': '-', 'Temperature': None, 'Soil_Moisture': 99.65892740826129, 'Sunlight': '-', 'Humidity': '-'},
                                   {'Botanist_Name': 'Carl Linnaeus', 'Botanist_Email': 'carl.linnaeus@lnhm.co.uk', 'Botanist_Phone': '(146)994-1635x35992', 'Last_Watered': 'Wed, 30 Aug 2023 13:16:25 GMT', 'Plant_Name': 'Black bat flower', 'Scientific_Name': '-', 'Recording_Time': '2023-08-30 14:56:12', 'Cycle': '-', 'Temperature': 11.376320865206864, 'Soil_Moisture': 94.04791885586481, 'Sunlight': '-', 'Humidity': '-'}])
