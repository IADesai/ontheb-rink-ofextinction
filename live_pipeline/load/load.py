"""Live Pipeline Load File"""
from os import environ
from boto3 import client
from botocore.client import BaseClient
from dotenv import load_dotenv

def send_email(config, task: str, message: str):
    """Function that sends out emails"""
    if not isinstance(task, str):
        raise Exception("Task should be a string")
    if not isinstance(message, str):
        raise Exception("Message should be a string")
    email = client('ses', aws_access_key_id=config["ACCESS_KEY_ID"],
                   aws_secret_access_key=config["SECRET_ACCESS_KEY"])
    response = email.send_email(
        Source=config["EMAIL"],
        Destination={
            'ToAddresses': [
                config["EMAIL"],
            ]
        },
        Message={
            'Subject': {
                'Data': f'{task}',
            },
            'Body': {
                'Html': {
                    'Data': f'{message}',
                }
            }
        }
    )

if __name__ == "__main__":

    load_dotenv()
    config = environ

    example_message = "This is is a test message to test that the email is being sent as expected"

    send_email(config, "example task", example_message)
