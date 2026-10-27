"""Tests for the image server and the requests client."""

import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import requests

import homework_18
from server import app as server


class ImageServerTests(unittest.TestCase):
    def setUp(self):
        temp_dir = tempfile.TemporaryDirectory()
        self.addCleanup(temp_dir.cleanup)
        upload_patch = patch.object(server, "UPLOAD_DIR", Path(temp_dir.name))
        upload_patch.start()
        self.addCleanup(upload_patch.stop)
        self.client = server.app.test_client()

    def test_upload_get_and_delete(self):
        uploaded = self.client.post(
            "/upload",
            data={"image": (io.BytesIO(b"jpeg content"), "photo 1.jpg", "image/jpeg")},
            content_type="multipart/form-data",
        )
        self.assertEqual(uploaded.status_code, 201)
        image_url = uploaded.json["image_url"]
        self.assertTrue(image_url.endswith("/uploads/photo_1.jpg"))

        response = self.client.get("/image/photo_1.jpg", headers={"Content-Type": "text"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["image_url"], image_url)
        response = self.client.get("/image/photo_1.jpg", headers={"Content-Type": "image"})
        self.assertEqual(response.data, b"jpeg content")
        response.close()
        response = self.client.get("/uploads/photo_1.jpg")
        self.assertEqual(response.data, b"jpeg content")
        response.close()

        deleted = self.client.delete("/delete/photo_1.jpg")
        self.assertEqual(deleted.status_code, 200)
        self.assertEqual(deleted.json["image_url"], image_url)
        self.assertEqual(self.client.get("/image/photo_1.jpg").status_code, 404)

    def test_non_image_is_rejected(self):
        response = self.client.post(
            "/upload",
            data={"image": (io.BytesIO(b"text"), "notes.txt", "text/plain")},
            content_type="multipart/form-data",
        )
        self.assertEqual(response.status_code, 400)


class ImageClientTests(unittest.TestCase):
    @patch("homework_18.requests.delete")
    @patch("homework_18.requests.get")
    @patch("homework_18.requests.post")
    def test_client_makes_post_get_delete_in_order(self, post, get, delete):
        image_url = f"{homework_18.BASE_URL}/uploads/photo.jpg"
        post.return_value = Mock(**{"json.return_value": {"image_url": image_url}})
        get.return_value = Mock(**{"json.return_value": {"image_url": image_url}})
        delete.return_value = Mock(**{"json.return_value": {"image_url": image_url}})

        with tempfile.TemporaryDirectory() as folder:
            photo = Path(folder) / "photo.jpg"
            photo.write_bytes(b"jpeg content")
            with patch("builtins.print"):
                homework_18.upload_get_delete(photo)

        post.assert_called_once()
        self.assertEqual(post.call_args.args[0], f"{homework_18.BASE_URL}/upload")
        self.assertEqual(post.call_args.kwargs["files"]["image"][2], "image/jpeg")
        get.assert_called_once_with(
            f"{homework_18.BASE_URL}/image/photo.jpg",
            headers={"Content-Type": "text"}, timeout=10,
        )
        delete.assert_called_once_with(f"{homework_18.BASE_URL}/delete/photo.jpg", timeout=10)
        for response in (post.return_value, get.return_value, delete.return_value):
            response.raise_for_status.assert_called_once()

    def test_wrong_file_type_is_rejected_before_http(self):
        with patch("homework_18.requests.post") as post:
            with self.assertRaises(ValueError):
                homework_18.upload_get_delete("not-an-image.txt")
            post.assert_not_called()


if __name__ == "__main__":
    unittest.main()