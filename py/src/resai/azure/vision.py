import os
from dotenv import load_dotenv
import requests
import json

load_dotenv()

VISION_ENDPOINT = os.getenv("VISION_ENDPOINT") + "/computervision"
VISION_KEY = os.getenv("VISION_KEY")

print(f"Vision Endpoint: {VISION_ENDPOINT}")
print(f"Vision Key: {VISION_KEY}")

def get_image_embedding(blob_data: bytes):
    api_url = VISION_ENDPOINT + "/retrieval:vectorizeImage?api-version=2023-02-01-preview&modelVersion=latest"
    print(f"Getting embedding for blob from {api_url}")

    headers = {
        'Ocp-Apim-Subscription-Key': VISION_KEY,
        'Content-Type': 'application/octet-stream'
    }

    try:
        r = requests.post(api_url, data=blob_data, headers=headers)

        if r.status_code == 200:
            image_vector = r.json()["vector"]
            return image_vector
        else:
            print(
                f"An error occurred while processing blob. Error code: {r.status_code}.")
            print(r.text)

    except Exception as e:
        print(f"An error occurred while processing blob: {e}")

    return None


def get_text_embedding(prompt):
    text = {'text': prompt}
    api_url = VISION_ENDPOINT + "/retrieval:vectorizeText?api-version=2023-02-01-preview&modelVersion=latest"

    headers = {
        'Content-type': 'application/json',
        'Ocp-Apim-Subscription-Key': VISION_KEY
    }

    try:
        r = requests.post(api_url,
                          data=json.dumps(text), headers=headers)

        if r.status_code == 200:
            text_vector = r.json()['vector']
            return text_vector
        else:
            print(
                f"An error occurred while processing the prompt '{text}'. Error code: {r.status_code}.")

    except Exception as e:
        print(f"An error occurred while processing the prompt '{text}': {e}")

    return None


def get_image_analysis_tags(blob_data: bytes):
    response = get_image_analysis(blob_data)
    tag_names = [tag['name'] for tag in response['tagsResult']['values']]
    return tag_names


# API Docs: https://eastus.dev.cognitive.microsoft.com/docs/services/Cognitive_Services_Unified_Vision_API_2023-10-01/operations/61d65934cd35050c20f73ab6
# Must be an image (not a PDF).
def get_image_analysis(blob_data: bytes):
    api_url = VISION_ENDPOINT + "/imageanalysis:analyze?api-version=2023-02-01-preview&modelVersion=latest&features=tags"

    headers = {
        'Content-Type': 'application/octet-stream',
        "Ocp-Apim-Subscription-Key": VISION_KEY
    }

    try:
        r = requests.post(api_url, data=blob_data, headers=headers)

        if r.status_code == 200:
            return r.json()
        else:
            print(
                f"An error occurred while processing blob. Error code: {r.status_code}.")
            print(r.text)

    except Exception as e:
        print(f"An error occurred while processing blob: {e}")

    return None
