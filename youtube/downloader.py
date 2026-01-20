"""Download audio using yt-dlp (stub)."""
import os
from pathlib import Path
from typing import Optional

import yt_dlp


class Downloader:
    def __init__(self, output_dir: str = "downloads"):
        self.output_dir = output_dir
        Path(output_dir).mkdir(parents=True, exist_ok=True)

    def download_audio(self, video_url: str, fmt: str = "mp3", bitrate: int = 192) -> Optional[str]:
        """Download and return path to downloaded file (or None on failure)."""
        
        try:
            # Configure yt-dlp options for audio extraction
            audio_format = "bestaudio/best"
            
            ydl_opts = {
                "format": audio_format,
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": fmt,
                        "preferredquality": str(bitrate),
                    }
                ],
                "outtmpl": os.path.join(self.output_dir, "%(title)s.%(ext)s"),
                "quiet": True,
                "no_warnings": True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=True)
                filename = ydl.prepare_filename(info)
                
                # Get the converted audio file path
                base_path = os.path.splitext(filename)[0]
                audio_path = f"{base_path}.{fmt}"
                
                if os.path.exists(audio_path):
                    return audio_path
                
                return None
                
        except Exception:
            return None
