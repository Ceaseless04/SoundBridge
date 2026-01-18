"""Apply ID3 tags to audio files (stub)."""
from mutagen.easyid3 import EasyID3


class Tagger:
    @staticmethod
    def apply_tags(file_path: str, metadata: dict) -> bool:
        try:
            audio = EasyID3(file_path)
            for k, v in metadata.items():
                audio[k] = v
            audio.save()
            return True
        except Exception:
            return False
