from flask_jwt_extended import JWTManager
from flask import Flask
from pymongo import MongoClient
from app.routes.api import api_bp
from app.services.spotify_service import SpotifyService
from app.services.user_service import UserService
from app.routes.auth import auth_bp
from app.configuration_manager import ConfigurationManager
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from app.services.metadata_service import MetadataService


def create_app() -> (Flask, str):
    """
    Creates and configures the Flask application.

    Returns:
        Flask: The configured Flask application instance.
    """
    # Load configuration from YAML file
    configuration_manager = ConfigurationManager("app/configurations/config.yaml")

    # Create and configure Flask app
    app = Flask(__name__)
    app.config["MONGO_URI"] = configuration_manager.MONGO_URI
    app.config["JWT_SECRET_KEY"] = configuration_manager.JWT_SECRET_KEY

    # Initialize MongoDB connection
    client = MongoClient(app.config["MONGO_URI"])
    database = client.get_default_database("Better-Tunes-DB")
    app.db = database

    # Set up Spotify API Client
    spotify_client = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
        client_id=configuration_manager.SPOTIFY_CLIENT_ID,
        client_secret=configuration_manager.SPOTIFY_CLIENT_SECRET
    ))

    # Initialize service components
    app.user_service = UserService(database)
    app.spotify_service = SpotifyService(spotify_client, database)
    app.metadata_service = MetadataService(database)

    # Initialize JWT for authentication
    jwt = JWTManager(app)

    # Register Blueprints for routing
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(api_bp, url_prefix='/api')

    return app, configuration_manager.PORT

if __name__ == "__main__":
    # Run the application in debug mode
    app, port = create_app()
    app.run(debug=True, host='0.0.0.0', port=port)
