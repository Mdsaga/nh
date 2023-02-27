import urllib.parse
import requests
import json
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# Define your API endpoint and token here
API_ENDPOINT = "https://short2url.in/api"
API_TOKEN = "2aa259aceab846d81abe727474e483314aa3e77f"

# Define the command handlers for the bot
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Welcome to the URL shortener bot! Send me a URL and I'll shorten it for you.")

def shorten_url(update, context):
    url = update.message.text.strip()
    if not url.startswith("http"):
        url = "http://" + url
    encoded_url = urllib.parse.quote(url, safe='')
    custom_alias = None
    if len(context.args) > 0:
        custom_alias = context.args[0]
    if custom_alias:
        alias_param = f"&alias={custom_alias}"
    else:
        alias_param = ""
    api_url = f"{API_ENDPOINT}?api={API_TOKEN}&url={encoded_url}{alias_param}"
    response = requests.get(api_url)
    json_data = json.loads(response.text)
    if json_data["status"] == "error" and "Alias already exists" in json_data["message"]:
        api_url = f"{API_ENDPOINT}?api={API_TOKEN}&url={encoded_url}"
        response = requests.get(api_url)
        json_data = json.loads(response.text)
        if json_data["status"] == "error":
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"An error occurred while shortening the URL: {json_data['message']}")
        else:
            shortened_url = json_data["shortenedUrl"]
            context.bot.send_message(chat_id=update.effective_chat.id, text=f"Here's your shortened URL: {shortened_url}")
    else:
        shortened_url = json_data["shortenedUrl"]
        context.bot.send_message(chat_id=update.effective_chat.id, text=f"Here's your shortened URL: {shortened_url}")

def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="To shorten a URL, send me the URL and an optional custom alias separated by a space.\n\nExample usage: /shorten https://www.google.com google")

def error(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="An error occurred. Please try again later.")

def main():
    # Initialize the Telegram bot
    updater = Updater(token="5879811488:AAGg1SjFIpAwifBvVsRXu_rq5ZkmAZ6TxFI", use_context=True)

    # Define the command handlers
    updater.dispatcher.add_handler(CommandHandler("start", start))
    updater.dispatcher.add_handler(CommandHandler("shorten", shorten_url))
    updater.dispatcher.add_handler(CommandHandler("help", help))

    # Define the error handler
    updater.dispatcher.add_error_handler(error)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
    
