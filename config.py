import json
import os
from pathlib import Path

CONFIG_PATH = Path(__file__).parent / "config.json"

with open(CONFIG_PATH) as f:
    config = json.load(f)

# Use env vars to override if provided
SPEECH_KEY = os.getenv("SPEECH_KEY")
SPEECH_REGION = os.getenv("SPEECH_REGION")
VOICE = config.get("voice", "en-US-AvaNeural")
OUTPUT_DIR = Path(config.get("output_dir", "audio"))

