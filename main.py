import os
import datetime
from typing import Optional
import telebot
from git import Repo

# Configuration
BOT_TOKEN = os.getenv("WBTSRE_BOT_TOKEN")
CHANNEL_NAME = "@wannabethesre"
DAILY_NOTE_PATH = '.'

# Initialize the bot
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set")
bot = telebot.TeleBot(BOT_TOKEN)

# Clone or pull the repository


def clone_or_pull_repo(repo_url: str, repo_path: str) -> None:
    """
    Clones the repository from the given URL if the repository path doesn't exist,
    otherwise pulls the latest changes from the remote repository.

    Args:
        repo_url: The URL of the repository to clone or pull.
        repo_path: The local path where the repository should be cloned or pulled.
    """
    if os.path.exists(repo_path):
        # If the repository already exists, pull the latest changes
        repo = Repo(repo_path)
        origin = repo.remotes.origin
        origin.pull()
    else:
        # If the repository doesn't exist, clone it
        Repo.clone_from(repo_url, repo_path)


@bot.message_handler(content_types=['document'])
def get_note(message):
    """
    Gets the note from the user and sends it to the channel.
    """
    if message.document.file_name.endswith('.md'):
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        with open(message.document.file_name, 'wb') as new_file:
            new_file.write(downloaded_file)
            
        with open(message.document.file_name, 'r') as new_file:
            send_daily_note_to_channel(bot, CHANNEL_NAME, new_file.read())
        bot.send_message(message.chat.id, "Your note has been sent to the channel.")
    else:
        bot.send_message(message.chat.id, "Please send a Markdown file.")
        

# Use smart_split to send the note to the telegram channel
def send_daily_note_to_channel(bot, channel_name, note_content):
    """
    Sends the daily note to the Telegram channel.
    Uses telebot.util.smart_split to split the message into multiple
    messages if it's too long.

    Args:
        bot: TeleBot instance.
        channel_name: Channel name (without the '@').
        note_content: Daily note content as a string.
    """
    if note_content:
        messages = telebot.util.smart_split(note_content)
        for message in messages:
            bot.send_message(channel_name, message, parse_mode='Markdown')
    else:
        bot.send_message(channel_name,
                         "No daily note found for today.")  # pragma: no cover

# Polling
bot.infinity_polling()

