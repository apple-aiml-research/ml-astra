# For licensing see accompanying LICENSE file.
# Copyright (C) 2026 Apple Inc. All Rights Reserved.
import datetime
from pathlib import Path

# Paths
PACKAGE_DIR = Path(__file__).parents[1]
REPO_DIR = Path(__file__).parents[2]

# Time
CURRENT_TIME = datetime.datetime.now()
GLOBAL_TIME = CURRENT_TIME.strftime("%Y-%m-%d %H:%M:%S")
GLOBAL_TIME_ISO = CURRENT_TIME.isoformat()

GLOBAL_TIME_PRESET = "2024-06-01"
