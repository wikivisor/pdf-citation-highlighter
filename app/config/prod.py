import os
from pathlib import Path
from dotenv import load_dotenv

ENV_FILE_PATH = print(os.getcwd() + "/.env")

load_dotenv(ENV_FILE_PATH)

HIGHLIGHT_COLOR = os.environ.get("HIGHLIGHT_COLOR", "#FFFF00")
PORT = int(os.environ.get("PORT", "5001"))
MYSQL_USER = os.environ.get("MYSQL_USER", "wikiuser")
MYSQL_DBNAME = os.environ.get("MYSQL_DBNAME", "wikidb")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD", "password")

class ProdConfig:
    HIGHLIGHT_COLOR = HIGHLIGHT_COLOR
    PORT = PORT
    MYSQL_USER = MYSQL_USER
    MYSQL_DBNAME = MYSQL_DBNAME
    MYSQL_PASSWORD = MYSQL_PASSWORD
