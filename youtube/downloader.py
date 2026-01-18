"""Download audio using yt-dlp (stub)."""
from typing import Optional


class Downloader:
    def __init__(self, output_dir: str = "downloads"):
        self.output_dir = output_dir

    def download_audio(self, video_url: str, fmt: str = "mp3", bitrate: int = 192) -> Optional[str]:
        """Download and return path to downloaded file (or None on failure)."""
        # TODO: integrate yt-dlp and ffmpeg for conversion
        return None
