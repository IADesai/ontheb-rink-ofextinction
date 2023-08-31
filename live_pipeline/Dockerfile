FROM python

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY ETL.sh .

COPY extract/extract.py .
COPY transform/transform.py .
COPY transform/transform_functions.py .
COPY load/load_to_database.py .
COPY load/database_functions.py .

CMD bash ETL.sh