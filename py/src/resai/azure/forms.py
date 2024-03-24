import os
from dotenv import load_dotenv
import requests
import time

load_dotenv()

FORMS_ENDPOINT = os.getenv("FORMS_ENDPOINT") + "/formrecognizer"
FORMS_KEY = os.getenv("FORMS_KEY")


# https://westus.dev.cognitive.microsoft.com/docs/services/form-recognizer-api-v2-1/operations/AnalyzeWithCustomForm
# https://learn.microsoft.com/en-us/azure/ai-services/document-intelligence/quickstarts/get-started-sdks-rest-api?view=doc-intel-3.1.0&viewFallbackFrom=form-recog-3.0.0&preserve-view=true&pivots=programming-language-rest-api
def submit_form_analysis(file_path: str):
    api_url = FORMS_ENDPOINT + "/documentModels/prebuilt-document:analyze?api-version=2023-07-31"
    print(f"Submitted form for analysis {file_path}")

    headers = {
        "Content-type": "application/json",
        "Ocp-Apim-Subscription-Key": FORMS_KEY
    }

    data = {
        "urlSource": file_path
    }

    try:
        r = requests.post(api_url, json=data, headers=headers)

        if r.status_code == 202:
            return r.headers.get('Operation-Location') # This is the URL to get the results
        else:
            print(
                f"An error occurred while processing {file_path}. Error code: {r.status_code}.")
            print(r.text)

    except Exception as e:
        print(f"An error occurred while processing {file_path}: {e}")

    return None



def get_analyze_results(operation_location: str):
    print(f"Getting form analyze results for {operation_location}")

    headers = {
        "Content-type": "application/json",
        "Ocp-Apim-Subscription-Key": FORMS_KEY
    }

    try:
        r = requests.get(operation_location, headers=headers)

        if r.status_code == 200:
            return r.json()
        else:
            print(
                f"An error occurred while processing {operation_location}. Error code: {r.status_code}.")
            print(r.text)

    except Exception as e:
        print(f"An error occurred while processing {operation_location}: {e}")

    return None


def get_form_content(file_path: str, retry_count=3):
    operation_location = submit_form_analysis(file_path)

    while retry_count > 0:
        if operation_location:
            result = get_analyze_results(operation_location)
            if result is not None:
                status = result.get("status")
                print(f"Form Analyzer Status: {status}")
                if status == "succeeded":
                    result = result.get("analyzeResult")
                    return result.get("content")
            else:
                print(f"Failed to get form content for {file_path}, retrying...")
        else:
            print(f"Failed to get form content for {file_path}")
        
        time.sleep(5)
        retry_count -= 1

    return None