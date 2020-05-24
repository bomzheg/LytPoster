import os
from pathlib import Path

from dotenv import load_dotenv

app_dir: Path = Path(__file__).parent

load_dotenv(str(app_dir.parent / '.env'))

BOT_TOKEN = os.getenv("BOT_TOKEN")

CAPTURE_STD_ERR = True
ERR_LOG = "err.log"
PRINT_LOG = "print.log"

LOG_CHAT_ID = os.getenv("LOG_CHAT_ID")
TARGET_CHAT_ID = os.getenv("TARGET_CHAT_ID")

PORT_LISTEN = os.getenv("PORT_LISTEN")

