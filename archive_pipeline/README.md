# Archive Pipeline

This directory contains the code and supporting files for running the pipeline for removing old files from the database and archiving data in a AWS S3 Data Warehouse via .csv files.

## Configure environment

```sh
python3 -m venv venv
source ./venv/bin/activate
pip3 install -r requirements.txt
```

## Configure environment variables

The following environment variables must be supplied in a `.env` file.

- `DATABASE_NAME`
- `DATABASE_USERNAME`
- `DATABASE_PASSWORD`
- `DATABASE_IP`
- `DATABASE_PORT`
- `ACCESS_KEY_ID`
- `SECRET_ACCESS_KEY`
- `ARCHIVE_BUCKET_NAME`


## Run the code

```sh
python3 archive.py
```

## Assumptions and design decisions

The script has been written for the purpose of managing a data pipeline for the Liverpool Natural History Museum. Therefore the timezone has been assumed to be London. This timezone determines what is considered to be data from the last twenty four hours.

When a .csv file is created for archiving purposes it receives a file name in the form `archived_YYYY_MM_DD.csv` where the date is the previous day.