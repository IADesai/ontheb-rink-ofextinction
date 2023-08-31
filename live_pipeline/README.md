# Live Pipeline

This folder contains all code and resources required for the ETL of the plant data collected from the API. The clean data is uploaded to Postgres RDS on AWS.

## Configure environment

```sh
python3 -m venv venv
source ./venv/bin/activate
pip3 install -r requirements.txt
```

## Configure environment variables

The following environment variables must be supplied in a `.env` file.

`ACCESS_KEY_ID`
`SECRET_ACCESS_KEY`
`EMAIL`
`DATABASE NAME`
`DATABASE USERNAME`
`DATABASE PASSWORD`
`DATABASE_IP`
`DATABASE_PORT`

## Run the code

```sh
bash ETL.sh
```

## Docker image

Build the docker image

```sh
docker build -t etl_pipeline . --platform "linux/amd64"
```

Run the docker image locally

```sh
docker run --env-file .env etl_pipeline
```

## Folders

### Extract

Contains all code and resources required for extracting the plant data from an api.
The extracted data is dumped into the plants.json file expect if the data is missing, a log is made of the missing plants.
To run the file individually : `python3 extract.py`
To run the test file: `pytest test_extract.py`

### Transform

Contains the scripts required to transform the raw data from extract into clean data for load.
To run the file individually: `python3 transform.py`
To run the test file: `pytest test_transform.py`

#### Assumptions and design decisions

Dates for 'Last Watered' and 'Time Recorded' are validated to ensure they are a real data, if erroneous or absent the data is stored as None and are then dropped from the dataframe as we cannot be sure of the validity of this data.

Temperature ranges have been set to be between 9 - 40 degrees, which has been determined from UK weather data, as this is where we expect plants to sustain life. Variation of 5 degree either side has been considered to be valid an alert is sent if this is the case. Any temperature above or below the 5 degrees leniency is unlikely to be a fluctuation of normal and is discarded as invalid. Ideally we would have a different database containing each specific plants optimal conditions for accurate results.

Soil moisture lower range is set at 21%. We have researched this value to be the lower end of normal. In a botanical garden we would expect the moisture quality to be better regulated and hence greater than this, otherwise it has not been watered in which case lower than 21 will send an alert. We have invalidated data which is less than 5% of a fluctuation as it is unlikely to have not been maintained that poorly.

### Load

Contains the script to load the clean data into an RDS Postgres Database.

Table design on the RDS is created as per `schema.sql`
To run the file individually: `python3 load_to_database.py`
To run the test file: `pytest test_database_functions.py`
