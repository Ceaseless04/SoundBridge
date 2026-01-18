"""Library management (add files, dedupe, organize)."""
from pathlib import Path
from typing import Optional


class Library:
    def __init__(self, path: str):
        self.path = Path(path).expanduser()
        self.path.mkdir(parents=True, exist_ok=True)

    def add(self, src_path: str, dest_rel_path: Optional[str] = None) -> str:
        """Copy/rename file into the library and return final path."""
        # TODO: implement dedupe, hashing, etc.
        dest = self.path / (dest_rel_path or Path(src_path).name)
        return str(dest)
