import os
import random
import telebot
from flask import Flask, request

# -------------------------------------------------
# Configuration
# -------------------------------------------------

BOT_TOKEN = os.getenv("key")
if not BOT_TOKEN:
    raise RuntimeError("Environment variable 'key' is not set")

RENDER_EXTERNAL_URL = os.getenv("RENDER_EXTERNAL_URL")
PORT = int(os.getenv("PORT", 5000))

# -------------------------------------------------
# Initialize bot and Flask app
# -------------------------------------------------

bot = telebot.TeleBot(BOT_TOKEN, threaded=False)
app = Flask(__name__)

# -------------------------------------------------
# Word logic
# -------------------------------------------------

def random_line(path: str) -> str:
    """
    Return one random non-empty line from a text file.
    """
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]

    if not lines:
        raise RuntimeError(f"File '{path}' is empty")

    return random.choice(lines)

# -------------------------------------------------
# Telegram command handlers
# -------------------------------------------------

@bot.message_handler(commands=["start", "help"])
def start_handler(message):
    bot.reply_to(
        message,
        "Hello! I am the Magic Shapka bot.\n"
        "Use /ask to find out who you are today."
    )

@bot.message_handler(commands=["ask"])
def ask_handler(message):
    adjective = random_line("adjectivesV2")
    noun = random_line("nounsV2")
    bot.reply_to(message, f"{adjective} {noun}")

# -------------------------------------------------
# Telegram webhook endpoint
# -------------------------------------------------

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def telegram_webhook():
    update = telebot.types.Update.de_json(
        request.get_data().decode("utf-8")
    )
    bot.process_new_updates([update])
    return "OK", 200

# -------------------------------------------------
# Health check (optional but recommended)
# -------------------------------------------------

@app.route("/")
def health():
    return "Shapka bot is running", 200

# -------------------------------------------------
# Application startup
# -------------------------------------------------

if __name__ == "__main__":
    if RENDER_EXTERNAL_URL:
        bot.remove_webhook()
        bot.set_webhook(url=f"{RENDER_EXTERNAL_URL}/{BOT_TOKEN}")
        print("Webhook configured")

    app.run(host="0.0.0.0", port=PORT)

