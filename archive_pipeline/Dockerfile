FROM python

WORKDIR /archive

COPY requirements.txt .

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

COPY archive.py .

CMD python3 archive.py
