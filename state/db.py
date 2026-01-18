"""State persistence layer with optional Supabase backend and local SQLite fallback.

Behavior:
- If `SUPABASE_URL` and `SUPABASE_KEY` are set in the environment, the class will use
  Supabase (Postgres) to persist `synced_tracks`.
- Otherwise it falls back to a local SQLite DB at `state/state.db`.
"""
import os
import sqlite3
from pathlib import Path
from typing import Optional


SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")


class StateDB:
    def __init__(self, db_path: str = "state/state.db"):
        """Initialize either a Supabase client or a local SQLite DB.

        Note: Supabase requires a `synced_tracks` table to exist. Create it using the
        SQL provided in the README or via the Supabase SQL editor:

        CREATE TABLE IF NOT EXISTS synced_tracks (
          spotify_id TEXT PRIMARY KEY,
          downloaded_at TIMESTAMP WITH TIME ZONE DEFAULT now()
        );
        """
        self._use_supabase = False
        if SUPABASE_URL and SUPABASE_KEY:
            try:
                # Lazy import to avoid requiring the dependency unless used
                from supabase import create_client

                self._sb = create_client(SUPABASE_URL, SUPABASE_KEY)
                # Basic check to ensure client can talk to the API
                _ = self._sb.table("synced_tracks").select("spotify_id").limit(1).execute()
                self._use_supabase = True
            except Exception:
                # Fall back to SQLite if Supabase not available or table missing
                self._use_supabase = False

        if not self._use_supabase:
            p = Path(db_path)
            p.parent.mkdir(parents=True, exist_ok=True)
            self.conn = sqlite3.connect(str(p))
            self._migrate()

    def _migrate(self):
        cur = self.conn.cursor()
        cur.execute(
            """
            CREATE TABLE IF NOT EXISTS synced_tracks (
                spotify_id TEXT PRIMARY KEY,
                downloaded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self.conn.commit()

    def is_synced(self, spotify_id: str) -> bool:
        """Return True if the given Spotify id is present in the synced table."""
        if self._use_supabase:
            try:
                res = self._sb.table("synced_tracks").select("spotify_id").eq("spotify_id", spotify_id).execute()
                data = getattr(res, "data", None) or res.get("data") if isinstance(res, dict) else None
                return bool(data)
            except Exception:
                # On failure, assume not synced (could also raise)
                return False

        cur = self.conn.cursor()
        cur.execute("SELECT 1 FROM synced_tracks WHERE spotify_id = ?", (spotify_id,))
        return cur.fetchone() is not None

    def mark_synced(self, spotify_id: str):
        """Mark a spotify id as synced in the selected backend."""
        if self._use_supabase:
            try:
                # Insert (Postgres will error on duplicate key unless using upsert)
                # Use upsert behaviour via `upsert` if available on client; fall back to insert
                try:
                    self._sb.table("synced_tracks").upsert({"spotify_id": spotify_id}).execute()
                except Exception:
                    self._sb.table("synced_tracks").insert({"spotify_id": spotify_id}).execute()
                return
            except Exception:
                # fall through to sqlite fallback
                pass

        cur = self.conn.cursor()
        cur.execute("INSERT OR REPLACE INTO synced_tracks (spotify_id) VALUES (?)", (spotify_id,))
        self.conn.commit()
