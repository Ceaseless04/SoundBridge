"""Playlist synchronization helpers."""
from typing import List
from .models import Playlist, Track


class PlaylistSync:
    def __init__(self, spotify_client):
        self.client = spotify_client

    def get_new_tracks(self, playlist: Playlist) -> List[Track]:
        """Return tracks added since last sync."""
        # TODO: compare with local state DB and return new items
        return []
