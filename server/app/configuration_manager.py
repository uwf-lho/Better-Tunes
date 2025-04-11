import yaml

class ConfigurationManager:
    def __init__(self, config_path):
        self.PORT = None
        self.SPOTIFY_CLIENT_SECRET = None
        self.JWT_SECRET_KEY = None
        self.SPOTIFY_CLIENT_ID = None
        self.MONGO_URI = None

        with open(config_path, 'r') as config_file:
            configuration = yaml.safe_load(config_file) or {}

        self.initialize_variables(configuration)

    def initialize_variables(self, configuration: dict):
        self.PORT = configuration.get('PORT')
        self.MONGO_URI = configuration.get('MONGO_URI')
        self.JWT_SECRET_KEY = configuration.get('JWT_SECRET_KEY')
        self.SPOTIFY_CLIENT_ID = configuration.get('SPOTIFY_CLIENT_ID')
        self.SPOTIFY_CLIENT_SECRET = configuration.get('SPOTIFY_CLIENT_SECRET')
