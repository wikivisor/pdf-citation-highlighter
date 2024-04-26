import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent.parent
ENV_FILE_PATH = BASE_DIR / ".env"

load_dotenv(ENV_FILE_PATH)

RED = float(os.environ.get("RED", 1))
GREEN = float(os.environ.get("GREEN", 1))
BLUE = float(os.environ.get("BLUE", 0))

class ProdConfig:
    RED = RED
    GREEN = GREEN
    BLUE = BLUE
