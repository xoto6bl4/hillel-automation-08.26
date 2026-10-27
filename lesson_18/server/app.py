"""A small Flask server for uploading and deleting images."""

from pathlib import Path

from flask import Flask, abort, jsonify, request, send_from_directory, url_for
from werkzeug.utils import secure_filename


app = Flask(__name__)
UPLOAD_DIR = Path(__file__).resolve().parent / "uploads"


def image_url(filename):
    return url_for("uploaded_image", filename=filename, _external=True)


def saved_image(filename):
    if filename != secure_filename(filename) or not (UPLOAD_DIR / filename).is_file():
        abort(404)
    return UPLOAD_DIR / filename


@app.post("/upload")
def upload_image():
    image = request.files.get("image")
    if image is None or not image.mimetype.startswith("image/"):
        return jsonify(error="Send an image in the 'image' field"), 400

    filename = secure_filename(image.filename or "")
    if not filename:
        return jsonify(error="Image filename is missing"), 400

    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    image.save(UPLOAD_DIR / filename)
    return jsonify(image_url=image_url(filename)), 201


@app.get("/uploads/<filename>")
def uploaded_image(filename):
    saved_image(filename)
    return send_from_directory(UPLOAD_DIR, filename)


@app.get("/image/<filename>")
def get_image(filename):
    saved_image(filename)
    if request.headers.get("Content-Type", "").lower().startswith("image"):
        return send_from_directory(UPLOAD_DIR, filename)
    return jsonify(image_url=image_url(filename))


@app.delete("/delete/<filename>")
def delete_image(filename):
    saved_image(filename).unlink()
    return jsonify(image_url=image_url(filename))


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080)