"""Offline tests for NASA search, asset selection, and image downloads."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, call, patch

import requests

import homework_17


def make_response(payload=None, content=b""):
    response = Mock()
    response.json.return_value = payload
    response.content = content
    return response


def search_response(*nasa_ids):
    return make_response({
        "collection": {
            "items": [{"data": [{"nasa_id": nasa_id}]} for nasa_id in nasa_ids]
        }
    })


def asset_response(*urls):
    return make_response({
        "collection": {"items": [{"href": url} for url in urls]}
    })


class NasaImagesTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp_dir.cleanup)
        self.output_dir = Path(self.temp_dir.name)
        output_patch = patch.object(homework_17, "OUTPUT_DIR", self.output_dir)
        output_patch.start()
        self.addCleanup(output_patch.stop)

    @patch("homework_17.requests.get")
    def test_downloads_two_images_with_five_requests(self, get):
        first_url = "https://images-assets.nasa.gov/first~large.jpg"
        second_url = "https://images-assets.nasa.gov/second.JPG?download=1"
        get.side_effect = [
            search_response("first", "second", "unused"),
            asset_response("https://example.com/first.png", first_url),
            make_response(content=b"first image"),
            asset_response(second_url),
            make_response(content=b"second image"),
        ]

        homework_17.main()

        self.assertEqual(get.call_args_list, [
            call(f"{homework_17.BASE_URL}/search", params={
                "q": "Curiosity rover Mars",
                "media_type": "image",
                "page_size": 20,
            }, timeout=30),
            call(f"{homework_17.BASE_URL}/asset/first", timeout=30),
            call(first_url, timeout=60),
            call(f"{homework_17.BASE_URL}/asset/second", timeout=30),
            call(second_url, timeout=60),
        ])
        self.assertEqual(
            (self.output_dir / "mars_photo1.jpg").read_bytes(), b"first image"
        )
        self.assertEqual(
            (self.output_dir / "mars_photo2.jpg").read_bytes(), b"second image"
        )

    @patch("homework_17.requests.get")
    def test_uses_first_jpg_even_when_url_has_query_parameters(self, get):
        first_url = "https://example.com/image.JPG?download=1"
        large_url = "https://example.com/image~large.jpg"
        get.return_value = asset_response(
            "https://example.com/image.png", first_url, large_url
        )
        self.assertEqual(homework_17.get_jpg_url("first"), first_url)

    @patch("homework_17.requests.get")
    def test_skips_duplicates_and_assets_without_jpg(self, get):
        get.side_effect = [
            search_response("no-jpg", "first", "first", "second"),
            asset_response("https://example.com/image.png"),
            asset_response("https://example.com/first.jpg"),
            make_response(content=b"first"),
            asset_response("https://example.com/second.jpg"),
            make_response(content=b"second"),
        ]
        homework_17.main()
        self.assertEqual(get.call_count, 6)
        self.assertEqual(len(list(self.output_dir.glob("*.jpg"))), 2)

    @patch("homework_17.requests.get")
    def test_empty_search_reports_missing_images(self, get):
        get.return_value = search_response()
        with self.assertRaisesRegex(ValueError, "downloaded 0"):
            homework_17.main()
        get.assert_called_once()
        self.assertEqual(list(self.output_dir.iterdir()), [])

    @patch("homework_17.requests.get")
    def test_http_errors_stop_each_stage_without_writing(self, get):
        for stage in ("search", "asset", "download"):
            with self.subTest(stage=stage):
                failed_response = make_response(content=b"error page")
                failed_response.raise_for_status.side_effect = requests.HTTPError(
                    "HTTP request failed"
                )
                responses = {
                    "search": [failed_response],
                    "asset": [search_response("first"), failed_response],
                    "download": [
                        search_response("first"),
                        asset_response("https://example.com/first.jpg"),
                        failed_response,
                    ],
                }
                get.side_effect = responses[stage]
                with self.assertRaises(requests.HTTPError):
                    homework_17.main()
                self.assertEqual(list(self.output_dir.iterdir()), [])


if __name__ == "__main__":
    unittest.main()