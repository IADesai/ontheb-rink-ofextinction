# Dashboard

This folder contains all code and resources required to extract the 
files from the s3 bucket and load it into the dashboard with visualisations.

## Configure environment

```sh
python3 -m venv venv
source ./venv/bin/activate
pip3 install -r requirements.txt
```

## Configure environment variables

The following environment variables must be supplied in a `.env` file.

`BUCKET_NAME`
`ACCESS_KEY_ID`
`SECRET_ACCESS_KEY`
`DATABASE NAME`
`DATABASE USERNAME`
`DATABASE PASSWORD`
`DATABASE_IP`
`DATABASE_PORT`

## Run the code
To run the entire pipeline
- Run `streamlit run pipeline.py`

To run just the extract_s3.py
- Run `python3 extract_s3.py`

To run just the streamlit_app.py
- Run `streamlit run streamlit_app.py`

# Docker image

Build the docker image

```sh
docker build -t plant-dashboard . --platform "linux/amd64"
```

Run the docker image locally

```sh
docker run -it --env-file .env -p 8501:8501 plant-dashboard 
```

## Files

### extract_s3.py

Contains all code and resources required for extracting the plant data from an s3 bucket.
To run the file individually : `python3 extract_s3.py`

### streamlit_app.py

Contains all code and resources required for the dashboard.
Toggle the button to switch from the live-data(default) to archived data.
To run the file individually : `streamlit run streamlit_app.py`

### Design Decisions
- We chose to use pagination to display 10 plants at a time so the user is not overwhelmed.
- Added temperature and moisture values for each data in bar chart to make it easier for user to view the values.
- Toggle button to give the user power over the data they want to view instead of just displaying the live data and archive data in the same page.

