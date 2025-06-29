"""
Бот, который отвечает на сообщения в Telegram.
Сначала определяются несколько функций-обработчиков.
Затем эти функции передаются в приложение и регистрируются в соответствующих местах.
После этого бот запускается и работает до тех пор, пока вы не нажмете Ctrl-C в командной строке.
"""

import logging

from telegram import ForceReply, Update
from telegram.ext import (
    Application,
    CommandHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

from model import LLMService
import dotenv

env = dotenv.dotenv_values(".env")

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logger = logging.getLogger(__name__)

llm_service = LLMService()


# Define a few command handlers. These usually take the two arguments update and context.
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_html(
        rf"Hi {user.mention_html()}!",
        reply_markup=ForceReply(selective=True),
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Send a message when the command /help is issued."""
    await update.message.reply_text("Help!")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Echo the user message."""
    await update.message.reply_text(update.message.text)


async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Chat the user message."""
    user_message = update.message.text
    llm_response = llm_service.chat(user_message)
    logger.info(f"User: {user_message}  LLM: {llm_response}")
    await update.message.reply_text(llm_response)


def main() -> None:
    """Start the bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(env["TELEGRAM_BOT_TOKEN"]).build()
    # echo_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, echo)
    chat_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, chat)

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # on non command i.e message - echo the message on Telegram
    application.add_handler(chat_handler)

    # Run the bot until the user presses Ctrl-C
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
