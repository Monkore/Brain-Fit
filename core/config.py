import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DB_PATH = BASE_DIR / "brainfit.db"
ASSETS_DIR = BASE_DIR / "assets"
MODELS_DIR = ASSETS_DIR / "models"

# App Settings
DEBUG = True
APP_NAME = "BrainFit AI"

# Voice Settings
VOSK_MODEL_PATH_EN = MODELS_DIR / "vosk-model-small-en-us"
VOSK_MODEL_PATH_HI = MODELS_DIR / "vosk-model-small-hi-0.22"
TTS_RATE = 150 # Slower rate for seniors

# Typography and Styling (Senior-first)
FONT_SIZE_HEADING = "36sp"
FONT_SIZE_BODY = "24sp"
FONT_SIZE_BUTTON = "28sp"

# We will let KivyMD handle colors, but store base sizes here
MIN_TOUCH_TARGET = "64dp"
