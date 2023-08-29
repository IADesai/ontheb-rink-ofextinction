"""Contains unit tests to be run with pytest for the functions relating to the archiving of data older than 24 hours."""

from re import match

from archive import get_previous_day_timestamp


def test_timestamp_returns_string():
    """Tests the timestamp is returned as a string."""
    res = get_previous_day_timestamp()
    assert isinstance(res, str)


def test_timestamp_length_expected():
    """Tests the length of the timestamp corresponds to YYYY-mm-dd HH:MM:SS."""
    res = get_previous_day_timestamp()
    assert len(res) == 19


def test_timestamp_formatted_correctly():
    """Tests the timestamp is formatted in a way recognised by PostgreSQL."""
    res = get_previous_day_timestamp()
    assert match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", res)