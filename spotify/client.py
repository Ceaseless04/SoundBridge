"""Small Spotify client wrapper (stub)."""
import os
from typing import Optional


class SpotifyClient:
    def __init__(self, client_id: Optional[str] = None, client_secret: Optional[str] = None):
        # TODO: initialize spotipy client here
        self.client_id = client_id or os.getenv("SPOTIFY_CLIENT_ID")
        self.client_secret = client_secret or os.getenv("SPOTIFY_CLIENT_SECRET")

    def authorize(self):
        """Perform OAuth flow or use cached token."""
        raise NotImplementedError

    def get_playlists(self, user_id: str):
        """Return playlists for a user (iterable)."""
        raise NotImplementedError
