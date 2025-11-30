# bot/handlers/check.py

from telegram import Update
from telegram.ext import (
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    ContextTypes,
    filters
)

from bot.utils.db import find_user_by_phone

# Conversation state
CHECK_PHONE = 1


async def check_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Starts the /check flow and asks for phone."""
    await update.message.reply_text("📱 Please enter your phone number to check your registration:")
    return CHECK_PHONE


async def check_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Receives phone number and returns saved user info."""
    phone = update.message.text.strip()
    user = find_user_by_phone(phone)

    if user:
        await update.message.reply_text(
            f"✅ Registration found!\n\n"
            f"ID: {user['id']}\n"
            f"Name: {user['name']}\n"
            f"Phone: {user['phone']}"
        )
    else:
        await update.message.reply_text(
            "❌ No registration found with this phone number.\n"
            "If you're new, use /register to sign up."
        )

    return ConversationHandler.END


# This is what main.py will import
check_handler = ConversationHandler(
    entry_points=[CommandHandler("check", check_command)],
    states={
        CHECK_PHONE: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, check_phone)
        ]
    },
    fallbacks=[],
)
