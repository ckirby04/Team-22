import os

# Base directory (where this file lives)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# --- Asset Paths ---
LOGO_PATH = os.path.join(BASE_DIR, "logo.jpg")
BASE_ICON_PATH = os.path.join(BASE_DIR, "baseicon.jpg")
COUNTDOWN_DIR = os.path.join(BASE_DIR, "countdown_images")
MUSIC_DIR = os.path.join(BASE_DIR, "photon_tracks")
HELMET_SOUNDS_DIR = os.path.join(BASE_DIR, "helmet-sounds")
GAME_SOUNDS_DIR = os.path.join(BASE_DIR, "game sounds")

# --- Database Config ---
DB_NAME = "photon"
DB_USER = "student"
DB_HOST = "localhost"
DB_PORT = "5432"

# --- UDP Network Config ---
UDP_TRANSMIT_PORT = 7500
UDP_RECEIVE_PORT = 7501
UDP_BROADCAST_ADDRESS = "127.0.0.1"
UDP_BUFFER_SIZE = 1024

# --- Game Timing (seconds) ---
SPLASH_DURATION_MS = 3000       # 3 seconds
COUNTDOWN_SECONDS = 30          # 30-second pre-game countdown
GAME_DURATION_SECONDS = 360     # 6 minutes

# --- Game Codes ---
GAME_START_CODE = 202
GAME_END_CODE = 221
RED_BASE_CODE = 53
GREEN_BASE_CODE = 43

# --- Scoring ---
TAG_POINTS = 10
FRIENDLY_FIRE_PENALTY = 10
BASE_HIT_POINTS = 100

# --- Team Config ---
MAX_PLAYERS_PER_TEAM = 15
TEAM_RED = "red"
TEAM_GREEN = "green"
