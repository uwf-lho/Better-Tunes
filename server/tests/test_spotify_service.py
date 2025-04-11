import pytest
from unittest.mock import MagicMock
from app.services.spotify_service import SpotifyService


@pytest.fixture
def mock_spotify():
    return MagicMock()


@pytest.fixture
def mock_db():
    collection = MagicMock()
    db = MagicMock()
    db.list_collection_names.return_value = []
    db.get_collection.return_value = collection
    return db


@pytest.fixture
def service(mock_spotify, mock_db):
    return SpotifyService(mock_spotify, mock_db)


def test_search_artist_ids(service, mock_spotify):
    mock_spotify.search.return_value = {
        "artists": {
            "items": [
                {"id": "artist1"},
                {"id": "artist2"}
            ]
        }
    }

    ids = service.search_artist_ids("beatles")
    assert ids == ["artist1", "artist2"]
    mock_spotify.search.assert_called_once()


def test_search_artist(service, mock_spotify):
    mock_spotify.search.return_value = {
        "artists": {
            "items": [
                {
                    "name": "Artist A",
                    "id": "1",
                    "external_urls": {"spotify": "http://spotify.com/a"},
                    "genres": ["pop"],
                    "images": [{"url": "large"}, {"url": "medium"}, {"url": "small"}]
                }
            ]
        }
    }

    result = service._search_artist("test")
    assert result[0]["artist_name"] == "Artist A"
    assert "artist_image" in result[0]


def test_search_albums(service, mock_spotify):
    mock_spotify.artist_albums.return_value = {
        "items": [
            {
                "artists": [{"name": "Album Artist"}],
                "name": "Cool Album",
                "total_tracks": 10,
                "release_date": "2022-01-01",
                "images": [{"url": "big"}, {"url": "medium"}, {"url": "small"}]
            }
        ]
    }

    result = service._search_albums(query="test", artist_ids=["id123"])
    assert len(result) == 1
    assert result[0]["album_name"] == "Cool Album"


def test_search_tracks(service, mock_spotify):
    service.metadata_collection.find_one.return_value = None

    mock_spotify.search.return_value = {
        "tracks": {
            "items": [
                {
                    "id": "track123",
                    "name": "Test Track",
                    "album": {
                        "name": "Album Name",
                        "album_type": "album",
                        "images": [{"url": "large"}, {"url": "medium"}, {"url": "small"}]
                    },
                    "artists": [{"name": "Artist A"}],
                    "external_urls": {"spotify": "http://spotify.com/track"}
                }
            ]
        }
    }

    result = service._search_tracks(query="track", username="logan")
    assert len(result) == 1
    assert result[0]["name"] == "Test Track"
    assert result[0]["likedByUser"] is False
    assert result[0]["dislikedByUser"] is False


def test_search_router(service):
    # Mock internal calls
    service._search_artist = MagicMock(return_value="ARTIST_RESULT")
    service._search_albums = MagicMock(return_value="ALBUM_RESULT")
    service._search_tracks = MagicMock(return_value="TRACK_RESULT")
    service.search_artist_ids = MagicMock(return_value=["id1"])

    assert service.search("artist", "q", "user") == "ARTIST_RESULT"
    assert service.search("album", "q", "user") == "ALBUM_RESULT"
    assert service.search("track", "q", "user") == "TRACK_RESULT"
    assert "msg" in service.search("badtype", "q", "user")


def test_get_image_artist():
    mock_artist = {
        "images": [{"url": "big"}, {"url": "medium"}, {"url": "small"}]
    }
    from app.services.spotify_service import SpotifyService as S
    assert S._get_image(mock_artist, source="artist") == "medium"


def test_get_image_no_images():
    from app.services.spotify_service import SpotifyService as S
    assert S._get_image({}, source="artist") is False
