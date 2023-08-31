FROM amazon/aws-lambda-python

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt .

RUN pip install -r requirements.txt


COPY pipeline_functions.py .
COPY pipeline.py .

# Set the CMD to your handler (could also be done as a parameter override outside of the Dockerfile)
CMD [ "pipeline.handler" ]
