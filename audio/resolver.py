"""Select and resolve audio sources for a track (stub)."""


class Resolver:
    def __init__(self, preference: str = "youtube"):
        self.preference = preference

    def select_source(self, track):
        """Return chosen source and identifier (e.g. youtube id)."""
        return None
