# SoundBridge

SoundBridge automatically syncs Spotify playlists to an offline MP3 music library.

## Why
I wanted to reduce reliance on streaming services, avoid phone distractions,
and enjoy intentional offline listening on a dedicated MP3 player.

## Features
- Detect new tracks added to Spotify playlists
- Normalize track metadata
- Search and match tracks on YouTube
- Fetch audio from configurable sources
- Apply ID3 tags and organize a local music library
- Sync music to a portable MP3 player

## Status
🚧 Under active development

---

## Getting started ✅

These steps get the project running locally. For production or CI, follow the same steps but set secrets via your environment/secret store.

### Prerequisites
- Python 3.10+
- ffmpeg installed and available on PATH
- A Supabase project (optional but recommended for shared state)

### Install

1. Create a virtualenv and activate it:

   python3 -m venv .venv
   source .venv/bin/activate

2. Install dependencies:

   pip install -r requirements.txt

3. Copy environment variables example and fill in secrets:

   cp .env.example .env
   # Edit .env and provide your keys

### Supabase (optional but recommended)

If you want to use Supabase to persist sync state across machines, create a Supabase project and add a table named `synced_tracks` with the following SQL (use the Supabase SQL Editor):

```sql
CREATE TABLE IF NOT EXISTS synced_tracks (
  spotify_id TEXT PRIMARY KEY,
  downloaded_at TIMESTAMP WITH TIME ZONE DEFAULT now()
);
```

Then set the following environment variables in your `.env` (or in your environment):

- SUPABASE_URL: https://your-project-ref.supabase.co
- SUPABASE_KEY: your-service-or-anon-key

> Tip: For server-side usage prefer a service role key, but keep it secret.

If Supabase is not configured, SoundBridge will fall back to a local SQLite DB for simple single-machine use.

### Quick run

Run a single sync (scaffold currently prints actions):

   python3 main.py --config config.yaml --once

You can create a small script invocation as well:

   ./scripts/run_sync.sh config.yaml

### Development

- Tests: (not implemented in scaffold yet) — add unit tests and consider mocking Supabase.
- Linting: Use your preferred linter (e.g., flake8, ruff)

