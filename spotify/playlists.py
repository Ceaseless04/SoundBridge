"""Playlist synchronization helpers."""
from typing import List

from .models import Playlist, Track


class PlaylistSync:
    def __init__(self, spotify_client, state_db):
        self.client = spotify_client
        self.state_db = state_db

    def get_new_tracks(self, playlist: Playlist) -> List[Track]:
        """Return tracks added since last sync."""
        new_tracks = []
        results = self.client.sp.playlist_tracks(playlist.spotify_id)
        
        while results:
            for item in results.get("items", []):
                track_data = item.get("track", {})
                spotify_id = track_data.get("id")
                
                # Only include tracks that haven't been synced yet
                if spotify_id and not self.state_db.is_synced(spotify_id):
                    track = Track(
                        spotify_id=spotify_id,
                        title=track_data.get("name", ""),
                        artists=[artist.get("name", "") for artist in track_data.get("artists", [])],
                        album=track_data.get("album", {}).get("name", ""),
                        duration_ms=track_data.get("duration_ms", 0)
                    )
                    new_tracks.append(track)
            
            # Handle pagination
            results = self.client.sp.next(results) if results.get("next") else None
        
        return new_tracks
