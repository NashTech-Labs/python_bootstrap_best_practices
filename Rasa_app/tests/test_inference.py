"""Test cases for inference"""
import json
import pytest
from flask import Flask, jsonify

def ping():
    """health check"""
    ping_response = jsonify({"status": "OK"}), 200
    return ping_response



@pytest.fixture
def app():
    """mock for flask app"""
    app = Flask(__name__)
    app.route("/ping", methods=["GET"])(ping)
    return app


@pytest.fixture
def client(app):
    """mocking  flask app"""
    client = app.test_client()
    yield client


def test_ping(client):
    """test the function ping"""
    response = client.get("/ping")
    assert response.status_code == 200
    assert json.loads(response.data) == {"status": "OK"}


ALLOWED_EXTENSIONS = {"txt", "pdf", "png", "jpg", "jpeg", "gif"}


def allowed_file(filename):
    """checks for allowed file"""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def test_allowed_file():
    """test the function allowed file"""
    # Test file with allowed extension
    assert allowed_file("document.txt") == True
    assert allowed_file("image.png") == True

    # Test file with not allowed extension
    assert allowed_file("unknown.doc") == False
    assert allowed_file("unknown") == False

    # Test file with allowed extension in uppercase
    assert allowed_file("document.TXT") == True
    assert allowed_file("image.PNG") == True
