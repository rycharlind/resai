import os
from dotenv import load_dotenv, find_dotenv
import boto3

_ = load_dotenv(find_dotenv())

aws_key = os.environ['AWS_ACCESS_KEY_ID']
aws_secret = os.environ['AWS_SECRET_ACCESS_KEY']
aws_s3_bucket = os.environ['AWS_S3_BUCKET']

session = boto3.Session(
    aws_access_key_id=aws_key,
    aws_secret_access_key=aws_secret,
)

s3_client = session.client("s3")


def read_file(file_path: str):
    response = s3_client.get_object(
        Bucket=aws_s3_bucket, Key=file_path)
    file_content = response["Body"].read().decode("utf-8")
    return file_content


def upload_file(file_key: str, file_content):
    return s3_client.put_object(Bucket=aws_s3_bucket, Key=file_key, Body=file_content)
