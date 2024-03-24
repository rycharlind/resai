import os
from dotenv import load_dotenv
import requests
import json
import uuid

load_dotenv()

SEARCH_ENDPOINT = os.getenv("SEARCH_ENDPOINT")
SEARCH_API_KEY = os.getenv("SEARCH_API_KEY")


def index_data(
        search_service_name: str,
        index_name: str,
        blob_path: str,
        image_embedding,
        tags,
        content=None,
        content_embedding=None
):
    url = f"https://{search_service_name}.search.windows.net/indexes/{index_name}/docs/index?api-version=2023-11-01"

    print(f"Indexing data to {url}")

    file_name = get_file_name_from_url(blob_path)

    headers = {
        'Content-type': 'application/json',
        'api-key': SEARCH_API_KEY
    }

    doc_data = {
        # todo: change this to a hash of the file path so that we can update the index
        "id": str(uuid.uuid4()),
        "title": file_name,
        "file_path": blob_path,
        "image_vector": image_embedding,
        "tags": tags
    }

    if (content is not None):
        doc_data["content"] = content

    if (content_embedding is not None):
        doc_data["content_vector"] = content_embedding

    data = {"value": [doc_data]}

    response = requests.post(url, data=json.dumps(data), headers=headers)
    print(f"Index data status code {response.status_code}")
    print(f"Index data response text {response.text}")


# https://learn.microsoft.com/en-us/azure/search/hybrid-search-overview
def search_data(
        search_service_name: str,
        index_name: str,
        search_text: str = "",
        image_embedding=[],
        content="",
        content_embedding=[],
        top: int = 20
):
    url = f"https://{search_service_name}.search.windows.net/indexes/{index_name}/docs/search?api-version=2023-11-01"

    print(f"Posting search to {url}")

    headers = {
        'Content-type': 'application/json',
        'api-key': SEARCH_API_KEY
    }

    data = {
        "count": True,
        "select": "title, file_path, tags, content",
        "top": top,
    }

    if (image_embedding or content_embedding):
        data["vectorQueries"] = []

    if (image_embedding):
        data["vectorQueries"].append(
            {
                "vector": image_embedding,
                "k": top,
                "fields": "image_vector",
                "kind": "vector",
                "exhaustive": True
            }
        )

    if (content_embedding):
        data["vectorQueries"].append(
            {
                "vector": content_embedding,
                "k": top,
                "fields": "content_vector",
                "kind": "vector",
                "exhaustive": True
            }
        )

    if (search_text):
        data["search"] = search_text

    response = requests.post(url, data=json.dumps(data), headers=headers)
    print(f"Search complete with status_code {response.status_code}")
    return response.json()


def get_file_name_from_url(url):
    return url.split("/")[-1]


def delete_index(
        search_service_name: str,
        index_name: str
):
    url = f"https://{search_service_name}.search.windows.net/indexes/{index_name}?api-version=2023-11-01"

    print(f"Deleting index {url}")

    headers = {
        'Content-type': 'application/json',
        'api-key': SEARCH_API_KEY
    }

    response = requests.delete(url, headers=headers)
    print(f"Deleting index status code {response.status_code}")
    print(f"Deleting index complete for {index_name}")


def create_index(
        search_service_name: str,
        index_name: str
):
    url = f"https://{search_service_name}.search.windows.net/indexes?api-version=2023-11-01"

    print(f"Creating index {url}")

    headers = {
        'Content-type': 'application/json',
        'api-key': SEARCH_API_KEY
    }

    data = {
        "name": index_name,
        "fields": [
            {
                "name": "id",
                "type": "Edm.String",
                "searchable": False,
                "filterable": True,
                "retrievable": True,
                "sortable": True,
                "facetable": False,
                "key": True
            },
            {
                "name": "title",
                "type": "Edm.String",
                "searchable": True,
                "filterable": False,
                "retrievable": True,
                "sortable": True,
                "facetable": False
            },
            {
                "name": "file_path",
                "type": "Edm.String",
                "searchable": False,
                "filterable": True,
                "retrievable": True,
                "sortable": False,
                "facetable": False
            },
            {
                "name": "image_vector",
                "type": "Collection(Edm.Single)",
                "searchable": True,
                "retrievable": True,
                "dimensions": 1024,
                "vectorSearchProfile": "my-default-vector-profile"
            },
            {
                "name": "tags",
                "type": "Collection(Edm.String)",
                "searchable": True,
                "filterable": True,
                "retrievable": True,
                "sortable": False,
                "facetable": False
            },
            {
                "name": "content",
                "type": "Edm.String",
                "searchable": True,
                "filterable": True,
                "retrievable": True,
                "sortable": False,
                "facetable": False
            },
            {
                "name": "content_vector",
                "type": "Collection(Edm.Single)",
                "searchable": True,
                "retrievable": True,
                "dimensions": 1024,
                "vectorSearchProfile": "my-default-vector-profile"
            },
        ],
        "vectorSearch": {
            "algorithms": [
                {
                    "name": "my-hnsw-config-1",
                    "kind": "hnsw",
                    "hnswParameters": {
                        "metric": "cosine",
                        "m": 4,
                        "efConstruction": 400,
                        "efSearch": 500
                    }
                }
            ],
            "profiles": [
                {
                    "name": "my-default-vector-profile",
                    "algorithm": "my-hnsw-config-1"
                }
            ]
        }
    }

    response = requests.post(url, data=json.dumps(data), headers=headers)
    print(f"Create index status code {response.status_code}")
    print(f"Create index response text {response.text}")
