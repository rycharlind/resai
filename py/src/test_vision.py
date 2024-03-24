from resai.azure.vision import get_image_analysis, get_text_embedding


if __name__ == "__main__":
    # response = get_image_analysis(
    #     "https://calculatedhealth.blob.core.windows.net/neuron/sample_images/baseball.jpeg")

    # print("")
    # print("IMAGE ANALYSES RESPONSE:")
    # print(response)
    # print("")

    text_embeddings = get_text_embedding("Hello world")

    print("")
    print("Text Embedding Response:")
    print(len(text_embeddings))
    print("")
