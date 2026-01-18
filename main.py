"""SoundBridge CLI entrypoint."""
import argparse
import logging
from utils.config import load_config

logger = logging.getLogger("soundbridge")


def main():
    parser = argparse.ArgumentParser(description="SoundBridge - sync Spotify playlists to MP3 library")
    parser.add_argument("--config", "-c", default="config.yaml", help="path to configuration file")
    parser.add_argument("--once", action="store_true", help="run one synchronization and exit")
    args = parser.parse_args()

    cfg = load_config(args.config)
    logging.basicConfig(level=cfg.get("log_level", "INFO"))
    logger.info("Starting SoundBridge")

    # TODO: Wire up Spotify client, search/match on YouTube, download and tag
    if args.once:
        logger.info("Would run a single sync here (not implemented in scaffold)")
    else:
        logger.info("Daemon mode not implemented in scaffold")


if __name__ == "__main__":
    main()
