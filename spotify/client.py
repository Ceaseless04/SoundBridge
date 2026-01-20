"""Small Spotify client wrapper (stub)."""
import os
from typing import Optional

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials


class SpotifyClient:
    def __init__(self, client_id: Optional[str] = None, client_secret: Optional[str] = None):
        self.client_id = client_id or os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("SPOTIFY_CLIENT_SECRET")

        
        auth_manager = SpotifyClientCredentials(
            client_id=self.client_id,
            client_secret=self.client_secret
        )
        self.sp = spotipy.Spotify(auth_manager=auth_manager)

    def authorize(self):
        """Perform OAuth flow or use cached token."""
        raise NotImplementedError

    def get_playlists(self, user_id: str):
        """Return playlists for a user (iterable)."""
        raise NotImplementedError
