from resai.azure.forms import get_form_content
from resai.azure.search import index_data, delete_index, create_index
from resai.azure.vision import get_image_embedding, get_text_embedding, get_image_analysis_tags
from resai.azure.storage import get_blob_data
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

def index_blobs():
    container_client = blob_service_client.get_container_client(AZURE_STORAGE_CONTAINER_NAME)
    for blob in container_client.list_blobs():
        print()
        blob_url = f"{azure_storage_account_url}/{AZURE_STORAGE_CONTAINER_NAME}/{blob.name}"
        print(f"Indexing Blob URL: {blob_url}")
        blob_data: bytes = get_blob_data(blob_url)
        index_blob(blob_url, blob_data)


def index_blob(blob_url: str, blob_data: bytes):
    image_embedding = get_image_embedding(blob_data)
    tags = get_image_analysis_tags(blob_data)
    content = get_form_content(blob_url)
    content_embedding = get_text_embedding(content)
    index_data(
        search_service_name=SEARCH_SERVICE_NAME,
        index_name=SEARCH_INDEX_NAME,
        blob_path=blob_url,
        image_embedding=image_embedding,
        tags=tags,
        content=content,
        content_embedding=content_embedding
    )


if __name__ == "__main__":
    start_time = time.time()

    delete_index(SEARCH_SERVICE_NAME, SEARCH_INDEX_NAME)
    create_index(SEARCH_SERVICE_NAME, SEARCH_INDEX_NAME)
    index_blobs()

    end_time = time.time()
    execution_time_seconds = end_time - start_time
    execution_time_minutes = execution_time_seconds / 60
    print()
    print(f"Execution time: {execution_time_seconds} seconds")
    print(f"Execution time: {execution_time_minutes} minutes")
