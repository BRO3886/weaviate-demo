import base64
import io

from PIL import Image


def img_to_base64(image: Image.Image, format="JPEG") -> str:
    buffered = io.BytesIO()
    image.save(buffered, format=format)
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return img_str
