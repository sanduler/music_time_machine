import spotipy
import os
from spotipy.oauth2 import SpotifyOAuth

spotify_id = os.environ["SPOTIPY_CLIENT_ID"]
spotify_secret = os.environ["SPOTIPY_CLIENT_SECRET"]
redirect_uri = os.environ["SPOTIPY_REDIRECT_URI"]

sp = spotipy.Spotify()

sp.auth_manager=SpotifyOAuth(scope="playlist-modify-private",
                             redirect_uri=redirect_uri,
                             client_id=spotify_id,
                             client_secret=spotify_secret,
                             show_dialog=True,
                             cache_path="token.txt")

user_id = sp.current_user()["id"]
print(user_id)