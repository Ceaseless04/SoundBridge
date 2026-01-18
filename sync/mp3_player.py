"""Helpers to sync files to a portable MP3 player (stub)."""
import shutil
from pathlib import Path


class MP3Player:
    def __init__(self, mount_point: str):
        self.mount = Path(mount_point)

    def sync(self, library_path: str):
        """Simple sync where we copy files — in future support rsync-like behaviour."""
        # TODO: implement safe copy and deletion policies
        return True
