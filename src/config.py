from os import environ

SPOTIPY_CLIENT_ID = environ.get("SPOTIPY_CLIENT_ID")
SPOTIFYL_CLIENT_SECRET = environ.get("SPOTIFYL_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = environ.get("SPOTIPY_REDIRECT_URI")

MONGODB_URI = environ.get("MONGODB_URI", "mongodb://127.0.0.1")
MONGODB_DATABASE = environ.get("MONGODB_DATABASE", "spotishuffle_dev")
