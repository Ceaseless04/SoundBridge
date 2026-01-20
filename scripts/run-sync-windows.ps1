#!/usr/bin/env pwsh
$ErrorActionPreference = "Stop"

# Get first argument or default to config.yaml
$CONFIG = if ($args.Count -ge 1) { $args[0] } else { "config.yaml" }

python main.py --config $CONFIG --once