"""Filename / path naming helpers."""
import re


def sanitize_filename(s: str) -> str:
    s = re.sub(r"[\/:"]+", "-", s)
    return s.strip()


class Naming:
    @staticmethod
    def track_path(artist: str, album: str, title: str, fmt: str = "mp3") -> str:
        art = sanitize_filename(artist)
        alb = sanitize_filename(album)
        tit = sanitize_filename(title)
        return f"{art}/{alb}/{tit}.{fmt}"
