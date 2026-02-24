import os
import random
from pathlib import Path
from typing import Optional

from flask import Flask
import telebot
from bot_logger import BotLogger

TOKEN = os.getenv("BOT_TOKEN", "8726224956:AAHW-UhV7QEax8uatZg3td7G89Ufr7Nb3LQ")

MEETING_TEXT = (
    "🌈 Yntymak Gau meeting\n\n"
    "Join us for an open and friendly LGBT+ meeting.\n"
    "Contacts:\n"
    "Phone: 996706017625 \n"
    "Telegram: t.me/yntymakAl"
)

IMAGE_PATHS = [
    "images/img1.jpg",
    "images/img2.png",
]

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)


logger = BotLogger().get()


def pick_existing_image() -> Optional[Path]:
    candidates = [Path(p) for p in IMAGE_PATHS]
    existing = [p for p in candidates if p.exists() and p.is_file()]
    if not existing:
        return None
    return random.choice(existing)


def send_meeting_post(chat_id: int):
    logger.info("Preparing meeting post for chat_id=%s", chat_id)
    image_path = pick_existing_image()
    if image_path is None:
        logger.warning("No images found. Sending text only")
        bot.send_message(chat_id, MEETING_TEXT)
    else:
        logger.info("Sending image: %s", image_path)
        with image_path.open("rb") as photo:
            bot.send_photo(chat_id, photo=photo, caption=MEETING_TEXT)


@bot.message_handler(commands=["start", "meeting"])
def handle_start(message):
    logger.info("Received command from user_id=%s", message.from_user.id)
    send_meeting_post(message.chat.id)


@app.route("/")
def index():
    logger.info("Health check requested")
    return "Bot is running!"


if __name__ == "__main__":
    logger.info("Bot started. Polling is running")
    bot.infinity_polling()