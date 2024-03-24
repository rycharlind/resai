from resai.azure.storage import get_blob_sas_token, get_blob_url_with_sas, get_blob_data
import urllib.parse

if __name__ == "__main__":
    # file_path = "https://stgwermkefennec.blob.core.windows.net/stage/001381-7207-O Rev C Blank FINAL.pdf"
    file_path = "https://stgwermkefennec.blob.core.windows.net/stage/001381-7207-O%20Rev%20C%20Blank%20FINAL.pdf"
    # file_path = "https://stgwermkefennec.blob.core.windows.net/stage/112015.pdf"
    # sas_token = get_blob_sas_token(file_path)
    # url = get_blob_url_with_sas(file_path, sas_token)
    # print(url)
    blob_data = get_blob_data(file_path)
    # print(blob_data)