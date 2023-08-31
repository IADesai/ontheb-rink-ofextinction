# Live Pipeline

This folder contains all code and resources required for the ETL of the live pipeline

## Set-up and installation instructions

1. Create venv `python3 -m venv venv`
2. Activate venv `source .\venv\bin\activate`
3. Install Requirements `pip install -r requirements.txt`
4. Requires environment variables:

- ACCESS_KEY_ID
- SECRET_ACCESS_KEY
- EMAIL
- DATABASE NAME
- DATABASE USERNAME
- DATABASE PASSWORD
- DATABASE_IP
- DATABASE_PORT

# FOLDERS

- Extract
  -- contains all code and resources required for extracting the data from an api.
  -- Run python3 extract.py to run the extract program.
  -- Run pytest test_extract.py to run unit tests.
- Load
  -- loads the data into an RDS Postgres Database. You will need credentials for the database listed above
  -- tables design as per `schema.sql` file
  -- contains the following files: - requirements.txt will be necessary for the script to run - load_to_database.py - a script that will update the database with transformed data - database_functions.py - file containing the necessary functions for load_to_database to function - test_database_functions.py - pytest file containing a few tests to demonstrate functionality
- Transform
  -- Transformation of the data retrieved from extract
  -- Dates for last watered and time recorded are validated -- if erroneous these rows are dropped from our data due to uncertainty of their validity
  -- Temperature ranges are determined by the highest and lowest temperature in the UK which we expect plants to sustain life. We allow for a variation of 5 degrees either side for the measurement to be considered valid and an alert is sent if this is the case. Any temperatures above or below 5 degrees is unlikely to be a normal fluctuation and is discarded as invalid
  -- Soil moisture is expected to be greater than 21 -- which is a value we have researched to be the lower end of normal. We would expect the soil moisture in a botanical garden to be greater than this, otherwise it has not been watered and an alert will be sent for this too.

-- Testing files are made up of: conftest.py and test_transform.py which tests the functions outlined in transform_functions.py
