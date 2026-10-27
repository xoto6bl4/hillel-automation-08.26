"""Upload an image, get its URL, then delete it.

Start the server first: cd server && python app.py
Run this script: python homework_18.py path/to/photo.jpg
"""

import mimetypes
import sys
from pathlib import Path
from urllib.parse import urlsplit

import requests


BASE_URL = "http://127.0.0.1:8080"


def upload_get_delete(image_path):
    path = Path(image_path)
    mime_type = mimetypes.guess_type(path.name)[0]
    if not mime_type or not mime_type.startswith("image/"):
        raise ValueError("Choose an image file (for example, a .jpg or .png)")

    with path.open("rb") as image:
        response = requests.post(
            f"{BASE_URL}/upload",
            files={"image": (path.name, image, mime_type)},
            timeout=10,
        )
    response.raise_for_status()
    image_url = response.json()["image_url"]
    print("Uploaded:", image_url)

    # The filename in the returned URL is already URL-encoded.
    filename = urlsplit(image_url).path.rsplit("/", 1)[-1]
    response = requests.get(
        f"{BASE_URL}/image/{filename}", headers={"Content-Type": "text"}, timeout=10
    )
    response.raise_for_status()
    print("GET image URL:", response.json()["image_url"])

    response = requests.delete(f"{BASE_URL}/delete/{filename}", timeout=10)
    response.raise_for_status()
    print("Deleted:", response.json()["image_url"])


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python homework_18.py path/to/photo.jpg")
    upload_get_delete(sys.argv[1])