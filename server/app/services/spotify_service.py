from pymongo.synchronous.database import Database
from spotipy import Spotify

def get_artists(artists_dict: list[dict]) -> str:
    """
    Converts a list of artist dictionaries into a comma-separated string of artist names.

    Args:
        artists_dict (list[dict]): List of artist dictionaries.

    Returns:
        str: Comma-separated artist names or a fallback message.
    """
    return ", ".join(
        artist.get('name', 'Unknown') for artist in artists_dict
    ) if artists_dict else "No artists found."

def get_album(album: dict) -> str:
    """
    Retrieves the album name if the item is an album.

    Args:
        album (dict): Dictionary containing album data.

    Returns:
        str: Album name or 'N/A' if it's not an album.
    """
    return album.get('name', 'N/A') if album.get('album_type') == 'album' else 'N/A'

class SpotifyService:
    def __init__(self, spotify_client: Spotify, db: Database):
        """
        Initializes the SpotifyService with a Spotify client.

        Args:
            spotify_client (Spotify): An authenticated Spotify client.
        """
        if "song-metadata" not in db.list_collection_names():
            db.create_collection("song-metadata")

        self.metadata_collection = db.get_collection("song-metadata")
        self.spotify_client = spotify_client
        self.RESULT_LIMIT = 12

    def search(self, query_type: str, query: str, username: str) -> list[dict] | dict[str, str]:
        """
        Searches Spotify for artists, albums, or tracks based on the query type.

        Args:
            query_type (str): Type of search ('artist', 'album', 'track').
            query (str): The search query string.
            username (str): The username of the user.

        Returns:
            list[dict] | dict[str, str]: Search results or an error message.
        """
        match query_type:
            case 'artist':
                return self._search_artist(query)
            case 'album':
                artist_ids = self.search_artist_ids(query=query)
                return self._search_albums(artist_ids=artist_ids, query=query)
            case 'track':
                return self._search_tracks(query=query, username=username)
            case _:
                return {'msg': 'could not find any hits for this query'}

    def _is_liked_by_user(self, track_id:str, username: str) -> bool:
        return self.metadata_collection.find_one({'id': track_id, 'likedBy': username}) is not None

    def _is_disliked_by_user(self, track_id:str, username: str) -> bool:
        return self.metadata_collection.find_one({'id': track_id, 'dislikedBy': username}) is not None

    @staticmethod
    def _get_image(item: dict, source: str) -> str | bool:
        """Retrieves the smallest album image URL or returns False if none exist."""

        IMAGE_SIZE = 1  # Spotify provides three image sizes in the response: largest to smallest.
                        # We will use the middle-sized image from the list (index 1).

        match source:
            case 'album':
                return item['images'][IMAGE_SIZE]['url']
            case 'artist':
                artist_images = item.get('images', [])
                return artist_images[IMAGE_SIZE]['url'] if artist_images else False
            case 'track':
                album_images = item.get('album', {}).get('images', [])
                return album_images[IMAGE_SIZE]['url'] if album_images else False
            case _:
                return False



    def search_artist_ids(self, query: str) -> list[str]:
        """
        Searches for artist IDs matching the query.

        Args:
            query (str): The search query string.

        Returns:
            list[str]: List of matching artist IDs.
        """
        artist_ids = []
        results = self.spotify_client.search(q=query, type='artist', limit=self.RESULT_LIMIT)
        items = results.get('artists', {}).get('items', [])

        for item in items:
            artist_ids.append(item.get('id'))

        return artist_ids

    def _search_artist(self, query: str) -> list[dict]:
        """
        Searches for artists and formats the results into a list of dictionaries.

        Args:
            query (str): The search query string.

        Returns:
            list[dict]: Formatted artist data.
        """
        cards = []
        artists_results = self.spotify_client.search(q=query, type='artist', limit=self.RESULT_LIMIT)
        artists = artists_results.get('artists', {}).get('items', [])

        for artist in artists:
            cards.append({
                'artist_name': artist.get('name'),
                'artist_id': artist.get('id'),
                'spotify_link': artist.get('external_urls', {}).get('spotify'),
                'genres': artist.get('genres', []),
                'artist_image': self._get_image(item=artist, source='artist'),
            })

        return cards

    def _search_albums(self, query: str, artist_ids: list) -> list[dict]:
        """
        Searches for albums by artist IDs and formats the results.

        Args:
            query (str): The search query string.
            artist_ids (list): List of artist IDs.

        Returns:
            list[dict]: Formatted album data.
        """
        cards = []
        for artist_id in artist_ids:
            artist_albums = self.spotify_client.artist_albums(artist_id=artist_id, album_type='album')
            artist_albums = artist_albums.get('items', [])

            for album in artist_albums:
                cards.append({
                    'artist_name': album.get('artists', [])[0].get('name'),
                    'artist_id': artist_id,
                    'album_name': album.get('name'),
                    'total_tracks': album.get('total_tracks'),
                    'album_release_date': album.get('release_date'),
                    'album_image': self._get_image(item=album, source='album'),
                })

        return cards

    def _search_tracks(self, query: str, username: str) -> list[dict]:
        """
        Searches for tracks and formats the results into a list of dictionaries.

        Args:
            query (str): The search query string.
            username (str): The username to check likes/dislikes.

        Returns:
            list[dict]: Formatted track data.
        """

        results = self.spotify_client.search(q=query, type='track', limit=self.RESULT_LIMIT)
        tracks_dict = results.get('tracks', {}).get('items', [])

        cards = []
        for track in tracks_dict:
            track_id = track.get('id', 'N/A')
            album = track.get('album', {})
            artists = track.get('artists', [])

            cards.append({
                'name': track.get('name', 'N/A'),
                'album': get_album(album),
                'artists': get_artists(artists),
                'likedByUser': self._is_liked_by_user(track_id=track_id, username=username),
                'dislikedByUser': self._is_disliked_by_user(track_id=track_id, username=username),
                'songId': track_id,
                'album_image': self._get_image(item=track, source='track'),
                'spotify_link': track.get('external_urls', {}).get('spotify', False),
            })

        return cards
