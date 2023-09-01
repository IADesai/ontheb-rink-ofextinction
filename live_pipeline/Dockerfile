FROM amazon/aws-lambda-python

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt .

RUN pip install -r requirements.txt


COPY pipeline_functions.py .
COPY pipeline.py .


CMD [ "pipeline.handler" ]
