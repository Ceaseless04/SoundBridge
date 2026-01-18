#!/usr/bin/env bash
set -euo pipefail

CONFIG=${1:-config.yaml}
python3 main.py --config "$CONFIG" --once
