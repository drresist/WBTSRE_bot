import os
import telebot

BOT_TOKEN = os.getenv("WBTSRE_BOT_TOKEN")
CHANNEL_NAME = "@wannabethesre"

if not BOT_TOKEN:
    raise Exception("Please set the WBTSRE_BOT_TOKEN environment variable.")

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(content_types=["document"])
def get_note(message):
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


def send_daily_note_to_channel(bot, channel_name, note_content):
    if note_content:
        messages = telebot.util.smart_split(note_content)
        for message in messages:
            bot.send_message(channel_name, message, parse_mode='Markdown')
    else:
        bot.send_message(channel_name, "No daily note found for today.")


if __name__ == "__main__":
    bot.infinity_polling()
