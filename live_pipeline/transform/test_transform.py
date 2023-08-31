"""Test code for transform.py"""
from unittest.mock import MagicMock
import pytest
from transform_functions import create_dictionary_for_plant, create_list_for_data, validate_time_for_time_recorded, validate_time_for_last_watered, check_temperature_within_correct_ranges, check_soil_moisture_within_correct_ranges, delete_rows_containing_invalid_data, send_alert


def test_dictionary_created_for_plant(fake_raw_plant_data):
    """Test to check the plant dictionary is created given fake data"""
    result = create_dictionary_for_plant(fake_raw_plant_data)

    assert isinstance(result, dict) is True
    assert result['Botanist_Name'] == 'Fake Person'
    assert result['Sunlight'] == '-'
    assert isinstance(result["Temperature"], float) is True


def test_create_list_for_data(fake_data):
    """Test to check a list is made given the fake raw data"""
    result = create_list_for_data(fake_data)

    assert isinstance(result, list) is True


def test_time_recorded_valid(fake_time_recorded):
    """Test that valid timestamp returned for time recorded"""
    result = validate_time_for_time_recorded(fake_time_recorded)

    assert str(result) == '2023-08-30 14:56:09'


def test_time_recorded_invalid(fake_time_recorded_invalid):
    """Test that None is returned for an invalid timestamp"""
    result = validate_time_for_time_recorded(fake_time_recorded_invalid)

    assert result is None


def test_last_watered_valid(fake_last_watered):
    """Test that valid timestamp returned for time recorded"""
    result = validate_time_for_last_watered(fake_last_watered)

    assert str(result) == '2023-08-30 14:10:54'


def test_temperature_within_range(fake_temperature_valid):
    """Returns the original temperature as within range"""
    result = check_temperature_within_correct_ranges(fake_temperature_valid)

    assert result == fake_temperature_valid


def test_temperature__not_within_range(fake_temperature_invalid):
    """Returns None as the temperature is out of bounds of fluctuation"""
    result = check_temperature_within_correct_ranges(fake_temperature_invalid)

    assert result is None


def test_soil_moisture_within_range(fake_soil_moisture_valid):
    """Returns the original temperature as within range"""
    result = check_soil_moisture_within_correct_ranges(
        fake_soil_moisture_valid)

    assert result == fake_soil_moisture_valid


def test_rows_deleted_if_invalid(fake_dataframe):
    """Removes rows that contain None - as these are invalid"""
    assert fake_dataframe.shape[0] == 4

    result = delete_rows_containing_invalid_data(fake_dataframe)

    assert result.shape[0] == 2


def test_ensure_email_task_is_string():
    """Test that checks that if a task is not a string, an exception is raised"""
    fake_config = MagicMock()
    with pytest.raises(ValueError) as not_string:
        send_alert(fake_config, 0, "msg")
    assert "Task should be a string" in str(not_string)


def test_ensure_email_message_is_string():
    """Test that checks that if a message is not a string, an exception is raised"""
    fake_config = MagicMock()
    with pytest.raises(ValueError) as not_string:
        send_alert(fake_config, "task", 0)
    assert "Message should be a string" in str(not_string)
