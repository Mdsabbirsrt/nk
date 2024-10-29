import logging
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
import requests

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Define a command handler function
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hello! Use /bin <bin> to check a BIN.')

def check_bin(update: Update, context: CallbackContext) -> None:
    if len(context.args) != 1:
        update.message.reply_text('Please provide a BIN to check.')
        return

    bin_number = context.args[0]
    api_url = f'https://bins.antipublic.cc/bin/{bin_number}'

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        update.message.reply_text(f"BIN Info: {data}")
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
        update.message.reply_text('Failed to retrieve BIN information.')

def main() -> None:
    # Replace 'YOUR_TOKEN' with your bot's API token
    updater = Updater("7819656172:AAFo9XjkRk6LXfVHArkeMn_4uLIzyqzHp10")

    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("bin", check_bin))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
