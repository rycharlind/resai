from resai.azure.forms import get_form_content

if __name__ == "__main__":
    response = get_form_content("https://stgwermkefennec.blob.core.windows.net/stagedev/Gerding_68D111086_DWG.tif")
    print("")
    print("FORM CONTENT RESPONSE:")
    print(response)