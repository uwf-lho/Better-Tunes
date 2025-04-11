from pymongo.errors import DuplicateKeyError
from werkzeug.security import check_password_hash, generate_password_hash
import re

class UserService:

    def __init__(self, db):
        """
        Initializes the UserService and ensures the users collection and indexes exist.

        Args:
            db: The MongoDB database instance.
        """
        if "users" not in db.list_collection_names():
            db.create_collection("users")

        self.users_collection = db.get_collection("users")

        # Ensure unique field 'username' exists
        self.users_collection.create_index([("username", 1)], unique=True)

        # Ensure field 'password' exists
        self.users_collection.create_index([("password", 1)], unique=False)

    def get_user_by_username(self, username: str):
        """
        Fetch a user from the database by username.

        Args:
            username (str): The username to search for.

        Returns:
            dict: User document if found, else None.
        """
        return self.users_collection.find_one({"username": username})

    @staticmethod
    def verify_password(provided_password: str, stored_password: str) -> bool:
        """
        Verify if the provided password matches the stored password (with hashing).

        Args:
            provided_password (str): The plain text password to verify.
            stored_password (str): The hashed password stored in the database.

        Returns:
            bool: True if the password matches, else False.
        """
        return check_password_hash(stored_password, provided_password)

    @staticmethod
    def is_valid_username(username: str) -> bool:
        """
        Validates the username to prevent injection and ensure safe input.

        Args:
            username (str): The username to validate.

        Returns:
            bool: True if the username is valid, else False.
        """
        return bool(re.match(r'^[a-zA-Z0-9_.-]{3,20}$', username))

    def register_user(self, username: str, password: str):
        """
        Create a new user with a hashed password and enforce unique username.

        Args:
            username (str): The desired username.
            password (str): The plain text password.

        Returns:
            tuple: A response message and HTTP status code.
        """
        if not self.is_valid_username(username):
            return {"msg": "Invalid username. Use only letters, numbers, and characters like _.- with length 3-20."}, 400

        hashed_password = generate_password_hash(password)

        try:
            self.users_collection.insert_one({"username": username, "password": hashed_password})
            return {"msg": "User created successfully"}, 201
        except DuplicateKeyError:
            return {"msg": "Username already exists"}, 400
