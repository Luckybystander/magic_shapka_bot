import telebot
import random
import os
from flask import Flask
import threading


# --- IMPORTANT ---
# Replace 'YOUR_BOT_TOKEN_HERE' with the token you get from BotFather on Telegram.
# KEEP YOUR BOT TOKEN SECRET!
BOT_TOKEN = os.getenv("key")


# Initialize the bot with your token
bot = telebot.TeleBot(BOT_TOKEN)

# --- Word Combining Logic ---
# This is the same logic from the previous script, adapted to be used here.
def get_random_word(file_path):
    """
    Reads a text file and returns a single random word.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # .strip() removes whitespace, and we filter out empty lines
            words = [word.strip() for word in file.readlines() if word.strip()]
            return random.choice(words) if words else None
    except FileNotFoundError:
        print(f"Error: The file at '{file_path}' was not found.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def combine_words(file1_path, file2_path):
    """
    Combines a random word from the first file with a random word from the second file.
    """
    word1 = get_random_word(file1_path)
    word2 = get_random_word(file2_path)

    if word1 and word2:
        return f"{word1} {word2}"
    else:
        return "Sorry, I couldn't generate a combination. Please check that both word files exist and are not empty."

# --- Telegram Bot Commands ---
@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    """
    Handles the /start and /help commands.
    """
    bot.reply_to(message, "Hello! I am a Magic shapka bot. I can tell who are you today. Use the /ask command to find out who are you.")

@bot.message_handler(commands=['ask'])
def send_combination(message):
    """
    Handles the /combine command by generating and sending a new phrase.
    """
    # Define the paths to your word files
    # Make sure these files are in the same directory as this script.
    file_one = 'adjectives.txt' # Example file name
    file_two = 'nouns.txt'      # Example file name

    # Generate the combined phrase
    combined_phrase = combine_words(file_one, file_two)

    # Reply to the user with the result
    bot.reply_to(message, combined_phrase)

# --- Flask Server Setup ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Shapka Bot is running!"

def run_flask():
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)



# --- Main Bot Loop ---
if __name__ == '__main__':
    def start_bot():
        print("Bot is starting... Press Ctrl+C to stop.")
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            print(f"An error occurred while polling the bot: {e}")

    # Start bot polling in a separate thread
    threading.Thread(target=start_bot).start()

    # Start Flask app
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


