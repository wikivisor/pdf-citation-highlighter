import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE_PATH = BASE_DIR / ".env"

load_dotenv(ENV_FILE_PATH)

HIGHLIGHT_COLOR = os.environ.get("HIGHLIGHT_COLOR", "#FFFF00")
PORT = int(os.environ.get("PORT", "5001"))

class ProdConfig:
    HIGHLIGHT_COLOR = HIGHLIGHT_COLOR
    PORT = PORT

