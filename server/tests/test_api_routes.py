import pytest
from flask import Flask
from flask.testing import FlaskClient
from app.routes.api import api_bp
from flask_jwt_extended import JWTManager
from unittest.mock import MagicMock


# --- Flask App + Mocks Setup ---
@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "test-secret"
    JWTManager(app)

    # Inject mock services
    app.spotify_service = MagicMock()
    app.metadata_service = MagicMock()

    app.register_blueprint(api_bp, url_prefix="/api")
    return app


@pytest.fixture
def client(app: Flask):
    return app.test_client()


# --- /api/search Tests ---
def test_search_missing_fields(client: FlaskClient):
    res = client.post("/api/search", json={})
    assert res.status_code == 400
    assert res.get_json()["error"] == "Invalid or missing JSON payload"


def test_search_success(client: FlaskClient, app: Flask):
    app.spotify_service.search.return_value = [{"title": "Mock Song"}]

    res = client.post("/api/search", json={
        "query_type": "title",
        "payload": "guitar",
        "username": "testuser"
    })

    assert res.status_code == 200
    assert res.get_json() == [{"title": "Mock Song"}]
    app.spotify_service.search.assert_called_once_with(
        query_type="title",
        query="guitar",
        username="testuser"
    )


# --- /api/update-song Tests ---
def test_update_song_missing_fields(client: FlaskClient):
    res = client.post("/api/update-song", json={})
    assert res.status_code == 400
    assert res.get_json()["error"] == "Invalid or missing JSON payload"


def test_update_song_invalid_action(client: FlaskClient):
    res = client.post("/api/update-song", json={
        "songId": "123",
        "action": "invalid_action",
        "userId": "user_abc"
    })
    assert res.status_code == 400
    assert res.get_json()["msg"] == "Invalid action."


def test_update_song_like_success(client: FlaskClient, app: Flask):
    app.metadata_service.add_like_to_song.return_value = {"msg": "Liked!"}

    res = client.post("/api/update-song", json={
        "songId": "123",
        "action": "like",
        "userId": "user_abc"
    })

    assert res.status_code == 200
    assert res.get_json() == {"msg": "Liked!"}
    app.metadata_service.add_like_to_song.assert_called_once_with(
        song_id="123",
        user_id="user_abc"
    )
