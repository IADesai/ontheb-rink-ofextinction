"""
Extracts the archived csv files from bucket 
into the archived_data folder.
"""
import os
from os import environ
from os import path
from dotenv import load_dotenv
from boto3 import client
from botocore.client import BaseClient


def get_all_items_in_bucket(s3_client: BaseClient, bucket_name: str) -> list[str]:
    """
    Returns list[str]: A list of object keys.
    """
    return [o["Key"] for o in s3_client.list_objects(Bucket=bucket_name)["Contents"]]


def download_file_from_bucket(s3_client: BaseClient, bucket_name,
                              object_key: str, destination_path: str) -> None:
    """
    Downloads the file given a bucket-name, the file name and the destination.
    """
    s3_client.download_file(bucket_name, object_key, destination_path)


def download_csv_files_(s3_client: BaseClient, bucket_name: str,
                        filter_by: str, extension: str, dst_folder: str) -> str:
    """Downloads relevant files from S3 to a data/ folder."""
    files = get_all_items_in_bucket(s3_client, bucket_name)

    downloaded_file_paths = []
    os.makedirs(dst_folder, exist_ok=True)

    for file in files:
        if filter_by in file and file.endswith(extension):
            destination_path = f"{dst_folder}/{path.basename(file)}"
            download_file_from_bucket(
                s3_client, bucket_name, file, destination_path)
            downloaded_file_paths.append(destination_path)
    print("Downloaded files:", downloaded_file_paths)


if __name__ == "__main__":

    load_dotenv()

    s3 = client("s3",
                aws_access_key_id=environ.get("ACCESS_KEY_ID"),
                aws_secret_access_key=environ.get("SECRET_ACCESS_KEY")
                )

    download_csv_files_(
        s3, environ.get("BUCKET_NAME"), "archived", ".csv", "archived_data")
