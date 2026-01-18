"""Audio processing: ffmpeg helpers, resolver and tagging."""
from .ffmpeg import FFmpeg
from .resolver import Resolver
from .tagger import Tagger

__all__ = ["FFmpeg", "Resolver", "Tagger"]
