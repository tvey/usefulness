import base64
from io import BytesIO

from PIL import Image


def image_to_base64(image_path: str) -> str:
    with open(image_path, 'rb') as image_file:
        base64_string = base64.b64encode(image_file.read())
        return base64_string.decode()


def base64_to_image(base64_string: str):
    image_bytes = BytesIO(base64.b64decode(base64_string))
    image = Image.open(image_bytes)
    image.show()


encoded = image_to_base64('image.jpeg')
base64_to_image(encoded)
