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


## Run the code

```sh
python3 archive.py
```