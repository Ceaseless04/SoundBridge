"""Configuration loader."""
import yaml
import os
from pathlib import Path


def load_config(path: str = "config.yaml") -> dict:
    p = Path(path)
    if not p.exists():
        return {"log_level": os.getenv("LOG_LEVEL", "INFO")}

    with p.open() as fh:
        cfg = yaml.safe_load(fh) or {}
    cfg.setdefault("log_level", os.getenv("LOG_LEVEL", "INFO"))
    return cfg
