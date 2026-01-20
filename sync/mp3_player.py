"""Helpers to sync files to a portable MP3 player (stub)."""
import logging
import shutil
from pathlib import Path

logger = logging.getLogger(__name__)


class MP3Player:
    def __init__(self, mount_point: str):
        self.mount = Path(mount_point)

    def sync(self, library_path: str):
        """Simple sync where we copy files — in future support rsync-like behaviour."""
        try:
            library = Path(library_path)
            
            if not library.exists():
                logger.warning(f"Library path does not exist: {library_path}")
                return False
            
            if not self.mount.exists():
                logger.warning(f"Mount point does not exist: {self.mount}")
                return False
            
            # Create a music directory on the player if it doesn't exist
            music_dir = self.mount / "Music"
            music_dir.mkdir(parents=True, exist_ok=True)
            
            # Track files we copy
            copied_count = 0
            
            # Copy all audio files from library to player
            for src_file in library.rglob("*.mp3"):
                try:
                    # Preserve relative directory structure
                    rel_path = src_file.relative_to(library)
                    dest_file = music_dir / rel_path
                    
                    # Create destination directory
                    dest_file.parent.mkdir(parents=True, exist_ok=True)
                    
                    # Copy file (skip if destination is newer)
                    if not dest_file.exists() or src_file.stat().st_mtime > dest_file.stat().st_mtime:
                        shutil.copy2(str(src_file), str(dest_file))
                        copied_count += 1
                        logger.debug(f"Copied: {rel_path}")
                        
                except Exception as e:
                    logger.error(f"Failed to copy {src_file}: {e}")
            
            logger.info(f"Synced {copied_count} files to {self.mount}")
            return True
            
        except Exception as e:
            logger.error(f"Sync failed: {e}")
            return False
