from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    CallbackQueryHandler,
    ConversationHandler
)
import logging
import sqlite3
from datetime import datetime, timedelta

# --- Configuration --- Give it From BOTfather in telegram
BOT_TOKEN = "7712357378:AAFSK4Ycf_oIlpmA-72SlwaKFnnGhuuCeWs"

DB_NAME = "bot_users.db"
KEYWORD_RESPONSES = {
    "hello": "👋 Hello! How can I assist you today?",
    "price": "💰 Our products start at $10. Check our website!",
    "support": "🆘 Contact support@example.com for immediate help!",
    "order": "📦 Track your order here: https://example.com/orders",
    "refund": "🔄 Please share your order ID to process refund",
}
COMMON_QUESTIONS = ["Price List", "Order Status", "Contact Support"]

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (user_id INTEGER PRIMARY KEY, 
                  username TEXT, 
                  first_name TEXT,
                  last_interaction TIMESTAMP)''')
    conn.commit()
    conn.close()

# --- Rate Limiting ---
class CooldownManager:
    def init(self, cooldown=5):
        self.user_last_message = {}
        self.cooldown = timedelta(seconds=cooldown)

    def is_on_cooldown(self, user_id):
        return datetime.now() - self.user_last_message.get(user_id, datetime.min) < self.cooldown

cooldown_manager = CooldownManager()

# --- Enhanced Handlers ---
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    keyboard = ReplyKeyboardMarkup([[q] for q in COMMON_QUESTIONS], resize_keyboard=True)
    
    await update.message.reply_html(
        f"🌟 Welcome {user.mention_html()}!\n"
        "How can I help you today?",
        reply_markup=keyboard
    )
    
    # Save user to database
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''INSERT OR IGNORE INTO users 
                 VALUES (?, ?, ?, ?)''', 
              (user.id, user.username, user.first_name, datetime.now()))
    conn.commit()
    conn.close()

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # Rate limiting check
    if cooldown_manager.is_on_cooldown(user_id):
        await update.message.reply_text("⏳ Please wait a moment before sending another message.")
        return

    text = update.message.text.lower()
    response = None

    # Enhanced keyword matching with priority
    for keyword in sorted(KEYWORD_RESPONSES.keys(), key=len, reverse=True):
        if keyword in text.split():  # Check for whole words only
            response = KEYWORD_RESPONSES[keyword]
            break

    # Fallback response
    if not response:
        response = "❓ I'm still learning! Your question has been forwarded to our team."
        # Create support ticket (example)
        context.user_data['pending_ticket'] = text

    # Update cooldown
    cooldown_manager.user_last_message[user_id] = datetime.now()
    
    # Add quick actions
    keyboard = InlineKeyboardMarkup([[
        InlineKeyboardButton("Open Ticket", callback_data="open_ticket"),
        InlineKeyboardButton("Main Menu", callback_data="main_menu")
    ]])
    
    await update.message.reply_text(response, reply_markup=keyboard)

# --- Advanced Features ---
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "open_ticket":
        await query.edit_message_text("🎫 Creating support ticket...")
    elif query.data == "main_menu":
        await start_command(update, context)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logging.error(f"Update {update} caused error: {context.error}")
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="⚠️ An error occurred. Our engineers have been notified!"
    )
if __name__ == "__main__":
    # Initialize components
    init_db()
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    app = Application.builder().token(BOT_TOKEN).build()

    # Register handlers
    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Error handling
    app.add_error_handler(error_handler)

    print("🤖 Bot is running in enhanced mode...")
    app.run_polling()