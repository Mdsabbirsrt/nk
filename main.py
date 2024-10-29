import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Define a command handler function
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! Use /bin <bin> to check a BIN.')

async def check_bin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if len(context.args) != 1:
        await update.message.reply_text('Please provide a BIN to check.')
        return

    bin_number = context.args[0]
    api_url = f'https://bins.antipublic.cc/bin/{bin_number}'

    try:
        response = requests.get(api_url)
        response.raise_for_status()
        data = response.json()
        await update.message.reply_text(f"BIN Info: {data}")
    except requests.exceptions.RequestException as e:
        logger.error(f"API request failed: {e}")
        await update.message.reply_text('Failed to retrieve BIN information.')

async def main() -> None:
    # Replace 'YOUR_TOKEN' with your bot's API token
    application = ApplicationBuilder().token("7819656172:AAFo9XjkRk6LXfVHArkeMn_4uLIzyqzHp10").build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("bin", bin))

    # Start the bot
    await application.run_polling()

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
