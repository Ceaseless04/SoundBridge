"""Library management (add files, dedupe, organize)."""
import hashlib
import shutil
from pathlib import Path
from typing import Optional


class Library:
    def __init__(self, path: str):
        self.path = Path(path).expanduser()
        self.path.mkdir(parents=True, exist_ok=True)

    def _hash_file(self, file_path: str) -> str:
        """Compute SHA256 hash of a file."""
        sha256_hash = hashlib.sha256()
        with open(file_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()

    def add(self, src_path: str, dest_rel_path: Optional[str] = None) -> str:
        """Copy/rename file into the library and return final path."""
        src = Path(src_path)
        
        # Compute source file hash for deduplication
        src_hash = self._hash_file(str(src))
        
        # Determine destination path
        if dest_rel_path:
            dest = self.path / dest_rel_path
        else:
            dest = self.path / src.name
        
        # Check if file with same hash already exists in library
        for existing_file in self.path.rglob("*"):
            if existing_file.is_file():
                try:
                    existing_hash = self._hash_file(str(existing_file))
                    if existing_hash == src_hash:
                        # File already in library, return existing path
                        return str(existing_file)
                except Exception:
                    pass
        
        # Create destination directory if needed
        dest.parent.mkdir(parents=True, exist_ok=True)
        
        # Copy file to library
        shutil.copy2(str(src), str(dest))
        return str(dest)
