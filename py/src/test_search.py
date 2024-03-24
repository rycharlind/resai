from resai.azure.search import search_data
from resai.azure.vision import get_image_embedding
import os
from dotenv import load_dotenv

load_dotenv()

SEARCH_SERVICE_NAME = os.getenv("SEARCH_SERVICE_NAME")
SEARCH_INDEX_NAME = os.getenv("SEARCH_INDEX_NAME")

if __name__ == "__main__":
    image1 = "https://calculatedhealth.blob.core.windows.net/neuron/sample_images/baseball.jpeg"

    response = search_data(SEARCH_SERVICE_NAME,
                            SEARCH_INDEX_NAME, get_image_embedding(image1))

    print("")
    print("SEARCH RESPONSE:")
    print(response)
    print("")
