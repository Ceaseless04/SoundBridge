"""Simple ffmpeg wrapper utilities."""
import subprocess
from typing import Optional


class FFmpeg:
    @staticmethod
    def convert(input_path: str, output_path: str, bitrate: int = 192) -> bool:
        cmd = [
            "ffmpeg",
            "-y",
            "-i",
            input_path,
            "-b:a",
            f"{bitrate}k",
            output_path,
        ]
        try:
            subprocess.run(cmd, check=True)
            return True
        except subprocess.CalledProcessError:
            return False
