import os
import requests
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")


def _config_ok() -> bool:
    if not DISCORD_TOKEN or not CHANNEL_ID:
        print("Discord config missing: set DISCORD_TOKEN and CHANNEL_ID in .env")
        return False
    return True


def send_message(message: str) -> None:
    """Send a message to the Discord channel via Discord Official API."""

    if not _config_ok():
        return

    url = f"https://discord.com/api/v10/channels/{CHANNEL_ID}/messages"
    headers = {
        "Authorization": f"Bot {DISCORD_TOKEN}",
        "Content-Type": "application/json",
    }

    try:
        res = requests.post(url, json={"content": message}, headers=headers, timeout=10)
        if res.status_code >= 400:
            print(f"Discord API error {res.status_code}: {res.text}")
    except requests.RequestException as exc:
        print(f"Failed to send Discord message: {exc}")
