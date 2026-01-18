"""Search YouTube for tracks (stub).

This should abstract different search backends (YouTube Data API, direct scraping, etc.).
"""

from typing import List


class YouTubeSearch:
    def __init__(self, api_key: str = None):
        self.api_key = api_key

    def search(self, query: str, max_results: int = 5) -> List[dict]:
        """Return a list of candidate videos (id/title/url)."""
        return []
