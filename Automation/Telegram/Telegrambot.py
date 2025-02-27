import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, filters

# Replace 'YOUR_BOT_TOKEN' with your actual bot token
BOT_TOKEN = "7712357378:AAFSK4Ycf_oIlpmA-72SlwaKFnnGhuuCeWs"

# Keyword responses.  Add more as needed.
KEYWORDS = {
    "سلام": "سلام علیکم  .",
    "refund": "Please contact us at [email address] for refund inquiries.",
    "support": "Our support team is available at [phone number] or [email address].",
    "hello": "Hello there! How can I help you today?",
    "goodbye": "Goodbye! Have a great day."

}

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text="Hi! I'm a customer support bot. Ask me anything!")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    response = None

    for keyword, reply in KEYWORDS.items():
        if keyword in text:
            response = reply
            break

    if response:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=response)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="I'm sorry, I didn't understand that.  Please try again.")


if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    start_handler = CommandHandler('start', start)
    message_handler = MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)

    application.add_handler(start_handler)
    application.add_handler(message_handler)

    application.run_polling()
