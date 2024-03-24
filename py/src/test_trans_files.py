from resai.azure.pdf import convert_pdf_to_image, convert_tiff_to_image
from resai.azure.storage import get_blob_data, get_file_type, save_blob, parse_azure_blob_url
import os
from dotenv import load_dotenv
from azure.storage.blob import BlobServiceClient
import time

load_dotenv()

SEARCH_SERVICE_NAME = os.getenv("SEARCH_SERVICE_NAME")
SEARCH_INDEX_NAME = os.getenv("SEARCH_INDEX_NAME")

AZURE_STORAGE_ACCOUNT_NAME = os.getenv('AZURE_STORAGE_ACCOUNT_NAME')
AZURE_STORAGE_CONTAINER_NAME = os.getenv('AZURE_STORAGE_CONTAINER_NAME')
AZURE_STORAGE_ACCOUNT_KEY = os.getenv('AZURE_STORAGE_ACCOUNT_KEY')
STORAGE_LOCAL_TMP_PATH = os.getenv('STORAGE_LOCAL_TMP_PATH')

azure_storage_account_url = f"https://{AZURE_STORAGE_ACCOUNT_NAME}.blob.core.windows.net"
azure_connection_string = f"DefaultEndpointsProtocol=https;AccountName={AZURE_STORAGE_ACCOUNT_NAME};AccountKey={AZURE_STORAGE_ACCOUNT_KEY};EndpointSuffix=core.windows.net"

blob_service_client = BlobServiceClient.from_connection_string(
    azure_connection_string)

print()
print()
print(f"Search Service Name: {SEARCH_SERVICE_NAME}")
print(f"Search Index Name: {SEARCH_INDEX_NAME}")
print(f"Azure Storage Container Name: {AZURE_STORAGE_CONTAINER_NAME}")
print(f"Azure Storage Account Key: {AZURE_STORAGE_ACCOUNT_KEY}")
print(f"Azure Storage Account URL: {azure_storage_account_url}")
print(f"Azure Connection String: {azure_connection_string}")
print()
print()

def transform_blobs(container_in: str, container_out: str):
    container_client = blob_service_client.get_container_client(container_in)
    for blob in container_client.list_blobs():
        blob_in_full_path = f"{azure_storage_account_url}/{container_in}/{blob.name}"
        blob_out_full_path = f"{azure_storage_account_url}/{container_out}/{blob.name}"
        transform_blob_to_image(blob_in_full_path, blob_out_full_path)


def transform_blob_to_image(blob_in_full_path: str, blob_out_full_path: str):
    _, _, blob_name, _, _file_type = parse_azure_blob_url(blob_out_full_path)
    file_type = _file_type.lower()

    print(f"Blob In Path: {blob_in_full_path}")
    print(f"Blob Out Path: {blob_out_full_path}")
    print(f"Blob Name: {blob_name}")
    print(f"File Type: {file_type}")

    if file_type in ['jpg', 'jpeg', 'png']:
        blob_data: bytes = get_blob_data(blob_in_full_path)
        save_blob(container_out, blob_out_full_path, blob_data)
    elif file_type in ['tif']:
        blob_data: bytes = get_blob_data(blob_in_full_path)
        image = convert_tiff_to_image(blob_data)
        blob_full_path = f"{azure_storage_account_url}/{container_out}/{blob_name}.png"
        save_blob(container_out, blob_full_path, image)
    elif file_type in ['pdf']:
        blob_data: bytes = get_blob_data(blob_in_full_path)
        images = convert_pdf_to_image(blob_data)
        for index, image in enumerate(images):
            blob_page_name = f"{blob_name}_{index+1}.png"
            blob_full_path = f"{azure_storage_account_url}/{container_out}/{blob_page_name}"
            save_blob(container_out, blob_full_path, image)
    else:
        print(f"File type {file_type} not supported")



if __name__ == "__main__":
    start_time = time.time()

    container_in = "stage"
    container_out = "stagesilver"

    transform_blobs(container_in, container_out)

    end_time = time.time()
    execution_time_seconds = end_time - start_time
    execution_time_minutes = execution_time_seconds / 60
    print()
    print(f"Execution time: {execution_time_seconds} seconds")
    print(f"Execution time: {execution_time_minutes} minutes")