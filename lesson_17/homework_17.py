"""Download two Curiosity rover images using the NASA Images API."""

from pathlib import Path

import requests


BASE_URL = "https://images-api.nasa.gov"
OUTPUT_DIR = Path(__file__).resolve().parent


def get_jpg_url(nasa_id):
    """Return the first JPG link from an item's assets."""
    response = requests.get(f"{BASE_URL}/asset/{nasa_id}", timeout=30)
    response.raise_for_status()
    assets = response.json()["collection"]["items"]

    for asset in assets:
        url = asset["href"]
        if url.split("?", 1)[0].lower().endswith(".jpg"):
            return url
    return None


def main():
    """Search for Curiosity, then resolve assets and download two JPGs."""
    search_params = {
        "q": "Curiosity rover Mars",
        "media_type": "image",
        "page_size": 20,
    }
    response = requests.get(
        f"{BASE_URL}/search", params=search_params, timeout=30
    )
    response.raise_for_status()
    items = response.json()["collection"]["items"]

    downloaded = 0
    seen_ids = set()
    for item in items:
        nasa_id = item["data"][0]["nasa_id"]
        if nasa_id in seen_ids:
            continue
        seen_ids.add(nasa_id)

        jpg_url = get_jpg_url(nasa_id)
        if jpg_url is None:
            continue

        image_response = requests.get(jpg_url, timeout=60)
        image_response.raise_for_status()
        file_path = OUTPUT_DIR / f"mars_photo{downloaded + 1}.jpg"
        file_path.write_bytes(image_response.content)
        downloaded += 1
        print(f"Saved {file_path.name} (nasa_id: {nasa_id})")

        if downloaded == 2:
            return

    raise ValueError(f"Expected 2 JPG images, but downloaded {downloaded}.")


if __name__ == "__main__":
    main()