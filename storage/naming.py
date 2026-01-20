"""Filename / path naming helpers."""
import re


def sanitize_filename(s: str) -> str:
    s = re.sub(r"[\/:"]+", "-", s)
    return s.strip()


def get_storage_path(track, fmt: str = "mp3") -> str:
    """Get the relative storage path for a track in Artist/Album/Title format."""
    artist = " ".join(track.artists) if track.artists else "Unknown Artist"
    album = track.album or "Unknown Album"
    title = track.title or "Unknown Track"
    
    art = sanitize_filename(artist)
    alb = sanitize_filename(album)
    tit = sanitize_filename(title)
    return f"{art}/{alb}/{tit}.{fmt}"


class Naming:
    @staticmethod
    def track_path(artist: str, album: str, title: str, fmt: str = "mp3") -> str:
        art = sanitize_filename(artist)
        alb = sanitize_filename(album)
        tit = sanitize_filename(title)
        return f"{art}/{alb}/{tit}.{fmt}"
