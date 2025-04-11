import pytest
from unittest.mock import MagicMock
from app.services.metadata_service import MetadataService


@pytest.fixture
def mock_db():
    mock = MagicMock()
    mock.list_collection_names.return_value = []
    mock.get_collection.return_value = MagicMock()
    return mock


@pytest.fixture
def service(mock_db):
    return MetadataService(mock_db)


def test_get_song_from_id(service):
    service.metadata_collection.find_one.return_value = {"id": "song123"}
    song = service.get_song_from_id("song123")
    assert song["id"] == "song123"
    service.metadata_collection.find_one.assert_called_with({"id": "song123"})


def test_ensure_song_adds_if_missing(service):
    service.metadata_collection.find_one.return_value = None
    service._ensure_song_in_collection("song123")
    service.metadata_collection.insert_one.assert_called_once_with({
        "id": "song123",
        "likedBy": [],
        "dislikedBy": []
    })


def test_ensure_song_skips_if_exists(service):
    service.metadata_collection.find_one.return_value = {"id": "song123"}
    service._ensure_song_in_collection("song123")
    service.metadata_collection.insert_one.assert_not_called()


def test_add_like_to_song(service):
    service.metadata_collection.find_one.return_value = None
    result = service.add_like_to_song("song123", "user_abc")
    assert result["success"]
    service.metadata_collection.update_one.assert_called_with(
        {"id": "song123"},
        {
            "$addToSet": {"likedBy": "user_abc"},
            "$pull": {"dislikedBy": "user_abc"}
        }
    )


def test_add_dislike_to_song(service):
    service.metadata_collection.find_one.return_value = None
    result = service.add_dislike_to_song("song123", "user_abc")
    assert result["success"]
    service.metadata_collection.update_one.assert_called_with(
        {"id": "song123"},
        {
            "$addToSet": {"dislikedBy": "user_abc"},
            "$pull": {"likedBy": "user_abc"}
        }
    )


def test_unlike_song(service):
    service.metadata_collection.find_one.return_value = {"id": "song123"}
    result = service.unlike_song("song123", "user_abc")
    assert result["success"]
    service.metadata_collection.update_one.assert_called_with(
        {"id": "song123"},
        {"$pull": {"likedBy": "user_abc"}}
    )


def test_undislike_song(service):
    service.metadata_collection.find_one.return_value = {"id": "song123"}
    result = service.undislike_song("song123", "user_abc")
    assert result["success"]
    service.metadata_collection.update_one.assert_called_with(
        {"id": "song123"},
        {"$pull": {"dislikedBy": "user_abc"}}
    )


def test_require_song_id_raises_error():
    with pytest.raises(ValueError, match="song_id is required"):
        MetadataService._require_song_id("")
