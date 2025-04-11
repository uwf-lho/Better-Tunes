from pymongo.synchronous.database import Database


class MetadataService:
    def __init__(self, db: Database):
        # Setup collection
        if "song-metadata" not in db.list_collection_names():
            db.create_collection("song-metadata")

        self.metadata_collection = db.get_collection("song-metadata")

        # Ensure unique index on custom ID field
        self.metadata_collection.create_index(
            [("id", 1)], unique=True
        )

    def _ensure_song_in_collection(self, song_id: str) -> None:
        self._require_song_id(song_id)

        song = self.metadata_collection.find_one({"id": song_id})
        if song is None:
            self.metadata_collection.insert_one({
                "id": song_id,
                "likedBy": [],
                "dislikedBy": [],
            })

    def get_song_from_id(self, song_id: str):
        self._require_song_id(song_id)
        return self.metadata_collection.find_one({"id": song_id})

    def add_like_to_song(self, song_id: str, user_id: str):
        self._require_song_id(song_id)
        self._ensure_song_in_collection(song_id)
        self.metadata_collection.update_one(
            {"id": song_id},
            {
                "$addToSet": {"likedBy": user_id},
                "$pull": {"dislikedBy": user_id}
            },
        )
        return {'msg': 'successfully added a like to song.','success': True}

    def add_dislike_to_song(self, song_id: str, user_id: str):
        self._require_song_id(song_id)
        self._ensure_song_in_collection(song_id)
        self.metadata_collection.update_one(
            {"id": song_id},
            {
                "$addToSet": {"dislikedBy": user_id},
                "$pull": {"likedBy": user_id}
            },
        )
        return {'msg': 'successfully added a dislike to song.','success': True}

    def unlike_song(self, song_id: str, user_id: str):
        self._require_song_id(song_id)
        self._ensure_song_in_collection(song_id)
        self.metadata_collection.update_one(
            {"id": song_id},
            {"$pull": {"likedBy": user_id}}
        )
        return {'msg': 'successfully unliked a song.', 'success': True}

    def undislike_song(self, song_id: str, user_id: str):
        self._require_song_id(song_id)
        self._ensure_song_in_collection(song_id)
        self.metadata_collection.update_one(
            {"id": song_id},
            {"$pull": {"dislikedBy": user_id}}
        )
        return {'msg': 'successfully un-disliked a song.', 'success': True}

    @staticmethod
    def _require_song_id(song_id: str):
        # todo: ensure this function when song_id is none will be handled gracefully.
        if not song_id:
            raise ValueError("song_id is required")
