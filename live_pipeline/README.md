=======

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

# FOLDERS

- Extract
- Load
  -- loads the data into an RDS Postgres Database. You will need credentials for the database including:
  DATABASE NAME, DATABASE USERNAME, DATABASE PASSWORD, DATABASE_IP, DATABASE_PORT
  -- tables design as per `schema.sql` file
  -- contains the following files: - requirements.txt will be necessary for the script to run - load_to_database.py - a script that will update the database with transformed data - database_functions.py - file containing the necessary functions for load_to_database to function - test_database_functions.py - pytest file containing a few tests to demonstrate functionality

- Transform
