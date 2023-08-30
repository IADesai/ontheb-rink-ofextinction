"""Contains unit tests to be run with pytest for the functions relating to the archiving of data older than 24 hours."""

from re import match
from unittest.mock import patch

import pytest
import pandas as pd

from archive import get_previous_day_timestamp, create_deleted_rows_dataframe


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


@patch("archive.CSV_COLUMNS", ["column_a", "column_b"])
def test_data_frame_returned_from_creation():
    """Tests a DataFrame is returned if valid data is supplied."""
    deleted_rows = [(1, 2), (3, 4)]
    res = create_deleted_rows_dataframe(deleted_rows)
    assert isinstance(res, pd.DataFrame)


def test_exception_raised_empty_dataframe():
    """Checks an exception is raised if there are no deleted rows to create a DataFrame."""
    deleted_rows = []
    with pytest.raises(ValueError):
        create_deleted_rows_dataframe(deleted_rows)
