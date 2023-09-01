"""Contains unit tests to be run with pytest.
Unit tests for the functions relating to the archiving of data older than 24 hours.
"""

from re import match
from unittest.mock import patch, MagicMock
import os

import pytest
import pandas as pd

from archive import (get_previous_day_timestamp, create_deleted_rows_dataframe,
                     create_csv_filename, create_archived_csv_file, select_and_delete_from_db)


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


def test_csv_file_name_includes_correct_date_formatting():
    """Tests the date formatting is correct in the csv filename."""
    res = create_csv_filename()
    assert len(res) == 23
    assert match(r"archived_\d{4}_\d{2}_\d{2}\.csv", res)


def test_csv_file_created():
    """Tests a .csv file is added to the local directory."""
    assert not os.path.exists("/tmp/unit_test_csv.csv")
    mock_df = pd.DataFrame({"a": [1, 2], "b": [3, 4]})
    create_archived_csv_file(mock_df, "unit_test_csv.csv")
    assert os.path.exists("/tmp/unit_test_csv.csv")
    os.remove("/tmp/unit_test_csv.csv")


@patch("archive.get_rows_to_be_deleted")
@patch("archive.create_deleted_rows_dataframe")
@patch("archive.create_csv_filename")
@patch("archive.create_archived_csv_file")
@patch("archive.upload_csv_to_s3")
@patch("archive.delete_old_rows")
def test_correct_call_counts_select_and_delete(fake_delete_rows, fake_upload_csv, fake_archive_csv,
                                               fake_csv_filename, fake_create_df, fake_get_delete_rows):
    """Tests the correct functions are called by the select and delete function."""
    fake_get_delete_rows.return_value = [(1, 2), (3, 4)]
    fake_create_df.return_value = []
    fake_csv_filename.return_value = ""
    fake_delete_rows.return_value = [(5, 6, 7), (8, 9, 10)]

    conn = MagicMock()
    delete_timestamp = MagicMock()
    configuration = MagicMock()

    select_and_delete_from_db(conn, delete_timestamp, configuration)

    assert fake_get_delete_rows.call_count == 1
    assert fake_create_df.call_count == 1
    assert fake_csv_filename.call_count == 1
    assert fake_archive_csv.call_count == 1
    assert fake_upload_csv.call_count == 1
    assert fake_delete_rows.call_count == 1
