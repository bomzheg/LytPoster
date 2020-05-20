import os
from pathlib import Path

from dotenv import load_dotenv

app_dir: Path = Path(__file__).parent

load_dotenv(str(app_dir / '.env'))

BOT_TOKEN = os.getenv("BOT_TOKEN")

CAPTURE_STD_ERR = False
ERR_LOG = "err.log"
PRINT_LOG = "print.log"

LOG_CHAT_ID = os.getenv("LOG_CHAT_ID")
TARGET_CHAT_ID = os.getenv("TARGET_CHAT_ID")

SOURCE_URL = os.getenv("SOURCE_URL")

