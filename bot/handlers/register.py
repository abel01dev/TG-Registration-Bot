from os import name
import re
from turtle import update #to validate regular expressions
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup #for the share contact button

from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, filters, ContextTypes
from bot.utils.db import add_user

from bot.utils.db import add_user

ASK_NAME, ASK_PHONE = range(2)

# Validate name — only letters and spaces allowed
def is_valid_name(name: str) -> bool:
    return bool(re.match(r"^[A-Za-z\s]{2,30}$", name))

# Validate phone number — numbers with optional "+"
def is_valid_phone(phone: str) -> bool:
    return bool(re.match(r"^\+?\d{7,15}$", phone))

async def start_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📝 Please enter your full name:")
    return ASK_NAME
# a separate function for getting and validating name
async def get_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_name = update.message.text.strip()

    if not is_valid_name(user_name):
        await update.message.reply_text("❌ Please enter a valid name (letters only, no numbers).")
        return ASK_NAME

    context.user_data["name"] = user_name

    contact_button = KeyboardButton("Share phone number", request_contact=True)
    reply_markup = ReplyKeyboardMarkup([[contact_button]], one_time_keyboard=True)
    await update.message.reply_text("✅ Great! Now share or enter your phone number:", reply_markup=reply_markup)
    return ASK_PHONE
# a separate function for getting and validating phone number
async def get_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # If shared via button
    if update.message.contact:
        phone = update.message.contact.phone_number
    else:
        phone = update.message.text.strip()

    if not is_valid_phone(phone):
        await update.message.reply_text("❌ Invalid phone number. Use format +123456789 or 0123456789.")
        return ASK_PHONE

    context.user_data["phone"] = phone
    name = context.user_data["name"]

    user_id = add_user(name, phone)
    print(f"✅ Registration complete!\n\nID: {user_id}\nName: {name}\nPhone: {phone}")

    await update.message.reply_text(
    f"✅ Registration complete!\n\n🆔 ID: {user_id}\n👤 Name: {name}\n📞 Phone: {phone}"
)

    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Registration cancelled.")
    return ConversationHandler.END

# Register handler for main.py
register_handler = ConversationHandler(
    entry_points=[CommandHandler("register", start_registration)],
    states={
        ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, get_name)],
        ASK_PHONE: [
            MessageHandler(filters.CONTACT, get_phone),
            MessageHandler(filters.TEXT & ~filters.COMMAND, get_phone),
        ],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
