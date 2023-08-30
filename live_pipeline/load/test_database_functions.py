"""libraries required to test database functions"""
from unittest.mock import MagicMock
from database_functions import add_cycle_information, add_botanist_information, add_species_information, add_plant_information


def test_add_cycle_info_if_false():
    """Tests correct commands are called"""
    fake_connection = MagicMock()
    fake_fetch = fake_connection.cursor().__enter__().fetchone
    fake_fetch.return_value = {'exists': False}
    fake_execute = fake_connection.cursor().__enter__().execute

    result = add_cycle_information(fake_connection, 'test_cycle')

    assert fake_fetch.call_count == 1
    assert fake_execute.call_count == 2


def test_add_cycle_info_if_true():
    """Tests correct commands are called if data exists"""
    fake_connection = MagicMock()
    fake_fetch = fake_connection.cursor().__enter__().fetchone
    fake_fetch.return_value = {'exists': True}
    fake_execute = fake_connection.cursor().__enter__().execute

    result = add_cycle_information(fake_connection, 'test_cycle')

    assert fake_fetch.call_count == 1
    assert fake_execute.call_count == 1


def test_add_botanist_information():
    """Tests botanist information added if not already in database"""
    fake_connection = MagicMock()
    fake_fetch = fake_connection.cursor().__enter__().fetchone
    fake_fetch.return_value = {'exists': False}
    fake_execute = fake_connection.cursor().__enter__().execute

    result = add_botanist_information(fake_connection, {
        'name': 'test', 'email': 'test@gmail.com', 'phone': '406-2555-562'})

    assert fake_fetch.call_count == 1
    assert fake_execute.call_count == 2


def test_add_botanist_information_if_true():
    """Tests botanist information is not added as it already exists"""
    fake_connection = MagicMock()
    fake_fetch = fake_connection.cursor().__enter__().fetchone
    fake_fetch.return_value = {'exists': True}
    fake_execute = fake_connection.cursor().__enter__().execute

    result = add_botanist_information(fake_connection, {
        'name': 'test', 'email': 'test@gmail.com', 'phone': '406-2555-562'})

    assert fake_fetch.call_count == 1
    assert fake_execute.call_count == 1


def test_add_species_information():
    """Tests species information added if not already in database"""
    fake_connection = MagicMock()
    fake_fetch = fake_connection.cursor().__enter__().fetchone
    fake_fetch.return_value = {'exists': False}
    fake_execute = fake_connection.cursor().__enter__().execute

    result = add_species_information(fake_connection, {
        'scientific_name': 'test aurelia'})

    assert fake_fetch.call_count == 1
    assert fake_execute.call_count == 2


def test_add_plant_information():
    """Tests plant information added to database"""
    fake_connection = MagicMock()
    fake_fetch = fake_connection.cursor().__enter__().fetchone
    fake_execute = fake_connection.cursor().__enter__().execute

    result = add_plant_information(fake_connection, {'sunlight': 'full sun', 'botanist': 'jeremy', 'cycle': 'perennial', 'scientific_name': 'test aurelia',
                                   'temp': 30, 'soil_moisture': 0.32, 'humidity': 5, 'last_watered': '28/05/2023', 'recording_taken': '30/08/2023'})

    assert fake_fetch.call_count == 4
    assert fake_execute.call_count == 5
