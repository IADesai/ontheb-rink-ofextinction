FROM amazon/aws-lambda-python

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt .

RUN pip3 install --upgrade pip

RUN pip3 install -r requirements.txt

COPY archive.py .

CMD [ "archive.lambda_handler" ]
