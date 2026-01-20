"""SoundBridge CLI entrypoint."""
import argparse
import logging
import time

from audio.tagger import Tagger
from spotify.client import SpotifyClient
from spotify.playlists import PlaylistSync
from state.db import StateDB
from storage.library import Library
from storage.naming import get_storage_path
from sync.mp3_player import MP3Player
from utils.config import load_config
from youtube.downloader import Downloader
from youtube.matcher import Matcher
from youtube.search import YouTubeSearch

logger = logging.getLogger("soundbridge")


def main():
    parser = argparse.ArgumentParser(description="SoundBridge - sync Spotify playlists to MP3 library")
    parser.add_argument("--config", "-c", default="config.yaml", help="path to configuration file")
    parser.add_argument("--once", action="store_true", help="run one synchronization and exit")
    parser.add_argument("--player-mount", default=None, help="mount point for MP3 player")
    args = parser.parse_args()

    cfg = load_config(args.config)
    logging.basicConfig(level=cfg.get("log_level", "INFO"))
    logger.info("Starting SoundBridge")

    # Initialize components
    try:
        spotify_client = SpotifyClient()
        state_db = StateDB(cfg.get("state_db", "state/state.db"))
        playlist_sync = PlaylistSync(spotify_client, state_db)
        downloader = Downloader(cfg.get("download_dir", "downloads"))
        yt_search = YouTubeSearch(cfg.get("youtube_api_key"))
        matcher = Matcher()
        library = Library(cfg.get("library_path", "library"))
        tagger = Tagger()
        
        player = None
        if args.player_mount or cfg.get("player_mount"):
            player_mount = args.player_mount or cfg.get("player_mount")
            player = MP3Player(player_mount)
        
    except Exception as e:
        logger.error(f"Failed to initialize components: {e}")
        return 1

    def sync_once():
        """Run a single sync cycle."""
        try:
            # Get user ID from config
            user_id = cfg.get("spotify_user_id")
            if not user_id:
                logger.error("spotify_user_id not configured")
                return False
            
            # Get playlists
            playlists = spotify_client.sp.user_playlists(user_id)
            synced_count = 0
            
            for playlist_item in playlists.get("items", []):
                playlist_id = playlist_item["id"]
                playlist_name = playlist_item["name"]
                
                logger.info(f"Processing playlist: {playlist_name}")
                
                # Create playlist object for sync
                from spotify.models import Playlist
                playlist = Playlist(
                    spotify_id=playlist_id,
                    name=playlist_name,
                    owner_id=user_id,
                    tracks=[]
                )
                
                # Get new tracks
                new_tracks = playlist_sync.get_new_tracks(playlist)
                logger.info(f"Found {len(new_tracks)} new tracks in {playlist_name}")
                
                for track in new_tracks:
                    try:
                        # Search for track on YouTube
                        query = f"{track.title} {' '.join(track.artists)}"
                        candidates = yt_search.search(query, max_results=5)
                        
                        if not candidates:
                            logger.warning(f"No YouTube results for: {query}")
                            continue
                        
                        # Match best candidate
                        track_info = {
                            "title": track.title,
                            "artists": track.artists,
                            "album": track.album
                        }
                        best_match = matcher.best_match(track_info, candidates)
                        
                        if not best_match:
                            logger.warning(f"Could not match: {track.title}")
                            continue
                        
                        # Download audio
                        logger.info(f"Downloading: {track.title}")
                        audio_path = downloader.download_audio(best_match.get("url", ""))
                        
                        if not audio_path:
                            logger.error(f"Failed to download: {track.title}")
                            continue
                        
                        # Determine storage path with proper naming
                        dest_rel_path = get_storage_path(track)
                        
                        # Add to library
                        final_path = library.add(audio_path, dest_rel_path)
                        logger.info(f"Added to library: {final_path}")
                        
                        # Apply metadata tags
                        metadata = {
                            "title": track.title,
                            "artist": " ".join(track.artists),
                            "album": track.album,
                        }
                        tagger.apply_tags(final_path, metadata)
                        
                        # Mark as synced
                        state_db.mark_synced(track.spotify_id)
                        synced_count += 1
                        
                    except Exception as e:
                        logger.error(f"Error processing track {track.title}: {e}")
                        continue
            
            logger.info(f"Sync complete. Synced {synced_count} tracks.")
            
            # Sync to MP3 player if configured
            if player:
                logger.info("Syncing to MP3 player...")
                if player.sync(cfg.get("library_path", "library")):
                    logger.info("Player sync complete")
                else:
                    logger.error("Player sync failed")
            
            return True
            
        except Exception as e:
            logger.error(f"Sync error: {e}")
            return False

    if args.once:
        success = sync_once()
        return 0 if success else 1
    else:
        # Daemon mode
        interval = cfg.get("sync_interval", 3600)  # Default: 1 hour
        logger.info(f"Running in daemon mode (interval: {interval}s)")
        
        try:
            while True:
                sync_once()
                logger.info(f"Waiting {interval}s until next sync...")
                time.sleep(interval)
        except KeyboardInterrupt:
            logger.info("Shutting down...")
            return 0


if __name__ == "__main__":
    main()
