import pathlib
import os
from dotenv import load_dotenv

BASE_DIR = pathlib.Path(__file__).parent.parent
load_dotenv(dotenv_path=BASE_DIR / ".env")

USERS_SHOULD_INVITE_COUNT = 7

BASE_URL = os.getenv("BASE_URL", "http://localhost:8000")
USERS_API = f"{BASE_URL}/api/users/users/"
STATS_API = f"{BASE_URL}/api/users/stats/"
INVITATIONS_API = f"{BASE_URL}/api/users/invitations/"

CHANNELS_IDs = {
    -1001414632886: ("Ibrat Farzandlari", "https://t.me/ibratfarzandlari"),
}
