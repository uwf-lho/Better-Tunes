import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from flask import Flask
from flask.testing import FlaskClient
from unittest.mock import MagicMock
from app.routes.auth import auth_bp
from app.services.user_service import UserService
from flask_jwt_extended import JWTManager


@pytest.fixture
def app():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "test-secret"
    JWTManager(app)

    # Fake DB/service injection
    fake_user_service = MagicMock(spec=UserService)
    app.user_service = fake_user_service

    app.register_blueprint(auth_bp, url_prefix="/auth")
    return app


@pytest.fixture
def client(app: Flask):
    return app.test_client()


def test_login_missing_fields(client: FlaskClient):
    res = client.post("/auth/login", json={})
    assert res.status_code == 400
    assert res.get_json()["error"] == "Invalid or missing JSON payload"


def test_login_user_not_found(client: FlaskClient, app: Flask):
    app.user_service.get_user_by_username.return_value = None
    res = client.post("/auth/login", json={"username": "notfound", "password": "test"})
    assert res.status_code == 401
    assert b"Invalid credentials" in res.data


def test_login_wrong_password(client: FlaskClient, app: Flask):
    app.user_service.get_user_by_username.return_value = {"username": "user", "password": "hashed"}
    app.user_service.verify_password.return_value = False
    res = client.post("/auth/login", json={"username": "user", "password": "wrong"})
    assert res.status_code == 401
    assert b"Invalid credentials" in res.data


def test_login_success(client: FlaskClient, app: Flask):
    app.user_service.get_user_by_username.return_value = {"username": "user", "password": "hashed"}
    app.user_service.verify_password.return_value = True
    res = client.post("/auth/login", json={"username": "user", "password": "correct"})
    assert res.status_code == 200
    assert b"access_token" in res.data


def test_register_missing_fields(client: FlaskClient):
    res = client.post("/auth/register", json={})
    assert res.status_code == 400


def test_register_duplicate_user(client: FlaskClient, app: Flask):
    app.user_service.register_user.return_value = ({"msg": "Username already exists"}, 400)
    res = client.post("/auth/register", json={"username": "existing", "password": "pass"})
    assert res.status_code == 400
    assert b"Username already exists" in res.data


def test_register_success(client: FlaskClient, app: Flask):
    app.user_service.register_user.return_value = ({"msg": "Registered!"}, 201)
    res = client.post("/auth/register", json={"username": "new", "password": "pass"})
    assert res.status_code == 201
    assert b"access_token" in res.data
