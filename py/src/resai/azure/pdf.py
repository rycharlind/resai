from pdf2image import convert_from_bytes
import io
from PIL import Image

def convert_pdf_to_image(blob_data: bytes):
    images = convert_from_bytes(blob_data)
    image_bytes = []
    for image in images:
        byte_arr = io.BytesIO()
        image.save(byte_arr, format='PNG')
        image_bytes.append(byte_arr.getvalue())
    return image_bytes

def convert_tiff_to_image(tiff_bytes: bytes):
    tiff_data = io.BytesIO(tiff_bytes)
    img = Image.open(tiff_data)
    png_data = io.BytesIO()
    img.save(png_data, 'PNG')
    return png_data.getvalue()

