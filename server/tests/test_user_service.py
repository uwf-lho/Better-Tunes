import pytest
from unittest.mock import MagicMock
from werkzeug.security import generate_password_hash
from pymongo.errors import DuplicateKeyError
from app.services.user_service import UserService


@pytest.fixture
def mock_db():
    mock = MagicMock()
    mock.list_collection_names.return_value = []
    mock.get_collection.return_value = MagicMock()
    return mock


@pytest.fixture
def service(mock_db):
    return UserService(mock_db)


def test_get_user_by_username_found(service):
    service.users_collection.find_one.return_value = {"username": "testuser"}
    user = service.get_user_by_username("testuser")
    assert user["username"] == "testuser"
    service.users_collection.find_one.assert_called_with({"username": "testuser"})


def test_get_user_by_username_not_found(service):
    service.users_collection.find_one.return_value = None
    user = service.get_user_by_username("unknown")
    assert user is None


def test_verify_password_matches():
    hashed = generate_password_hash("secret")
    assert UserService.verify_password("secret", hashed) is True


def test_verify_password_mismatch():
    hashed = generate_password_hash("secret")
    assert UserService.verify_password("wrong", hashed) is False


@pytest.mark.parametrize("username,expected", [
    ("validUser123", True),
    ("u", False),
    ("toolongusername_that_fails", False),
    ("bad!!name", False),
    ("user.name", True),
])
def test_is_valid_username(username, expected):
    assert UserService.is_valid_username(username) == expected


def test_register_user_success(service):
    service.users_collection.insert_one.return_value = None
    message, status = service.register_user("validUser", "password123")
    assert status == 201
    assert message["msg"] == "User created successfully"
    service.users_collection.insert_one.assert_called_once()


def test_register_user_duplicate(service):
    service.users_collection.insert_one.side_effect = DuplicateKeyError("duplicate key")
    message, status = service.register_user("existingUser", "password123")
    assert status == 400
    assert message["msg"] == "Username already exists"


def test_register_user_invalid_username(service):
    message, status = service.register_user("!!bad", "password123")
    assert status == 400
    assert "Invalid username" in message["msg"]
