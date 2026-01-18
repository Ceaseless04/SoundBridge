"""Domain models for Spotify objects."""
from dataclasses import dataclass


@dataclass
class Track:
    spotify_id: str
    title: str
    artists: list
    album: str
    duration_ms: int


@dataclass
class Playlist:
    spotify_id: str
    name: str
    owner_id: str
    tracks: list
