from urllib.parse import urlparse
import os
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from datetime import datetime, timedelta
from dotenv import load_dotenv
import urllib.parse

load_dotenv()

AZURE_STORAGE_ACCOUNT_NAME = os.getenv('AZURE_STORAGE_ACCOUNT_NAME')
AZURE_STORAGE_CONTAINER_NAME = os.getenv('AZURE_STORAGE_CONTAINER_NAME')
AZURE_STORAGE_ACCOUNT_KEY = os.getenv('AZURE_STORAGE_ACCOUNT_KEY')
STORAGE_LOCAL_TMP_PATH = os.getenv('STORAGE_LOCAL_TMP_PATH')

azure_storage_account_url = f"https://{AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net"
azure_connection_string = f"DefaultEndpointsProtocol=https;AccountName={AZURE_STORAGE_ACCOUNT_NAME};AccountKey={AZURE_STORAGE_ACCOUNT_KEY};EndpointSuffix=core.windows.net"

blob_service_client = BlobServiceClient.from_connection_string(
    azure_connection_string)

def parse_azure_blob_url(blob_url: str):
    parsed_url = urlparse(blob_url)

    storage_account = parsed_url.netloc.split('.')[0]
    path_parts = parsed_url.path.lstrip('/').split('/')
    container_name = path_parts[0]
    blob_name_with_extension = path_parts[-1]
    blob_name = os.path.splitext(blob_name_with_extension)[0]
    blob_prefix = '/'.join(path_parts[1:-1])
    file_type = os.path.splitext(blob_name_with_extension)[1].lstrip('.')
    
    return storage_account, container_name, blob_name, blob_prefix, file_type

def get_blob_full_name(blob_url: str):
    _, _, blob_name, blob_prefix, file_type = parse_azure_blob_url(blob_url)
    blob_full_name = f"{blob_name}.{file_type}"
    if blob_prefix:
        blob_full_name = f"{blob_prefix}/{blob_full_name}"
    return blob_full_name

def get_blob_data(_blob_url: str):
    blob_url = urllib.parse.unquote(_blob_url)
    _, container_name, _, _, _ = parse_azure_blob_url(blob_url)
    blob_full_name = get_blob_full_name(blob_url)
    print(f"Container Name: {container_name}")
    print(f"Blob Full Name: {blob_full_name}")
    blob_client = blob_service_client.get_blob_client(container_name, blob_full_name)
    return blob_client.download_blob().readall()


def get_blob_sas_token(blob_url: str):
    blob_full_name = get_blob_full_name(blob_url)
    sas_token = generate_blob_sas(account_name=AZURE_STORAGE_ACCOUNT_NAME,
                                  container_name=AZURE_STORAGE_CONTAINER_NAME,
                                  blob_name=blob_full_name,
                                  account_key=AZURE_STORAGE_ACCOUNT_KEY,
                                  permission=BlobSasPermissions(read=True),
                                  expiry=datetime.utcnow() + timedelta(hours=1))  # Token valid for 1 hour

    return sas_token


def get_blob_url_with_sas(blob_url: str, sas_token: str):
    return f"{blob_url}?{sas_token}"


def get_file_type(file_path: str):
    _, file_extension = os.path.splitext(file_path)
    return file_extension.lower()


def save_blob(blob_container:str, blob_url: str, blob_data: bytes):
    blob_full_name = get_blob_full_name(blob_url)
    blob_client = blob_service_client.get_blob_client(blob_container, blob_full_name)
    blob_client.upload_blob(blob_data, overwrite=True)
    return blob_client.url