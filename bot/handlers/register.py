from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, ConversationHandler, filters, ContextTypes

# Define the steps in our conversation
ASK_NAME, ASK_PHONE = range(2)

async def start_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📝 Please enter your full name:")
    return ASK_NAME

async def ask_phone(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Save the name the user entered
    context.user_data["name"] = update.message.text
    await update.message.reply_text("📱 Great! Now enter your phone number:")
    return ASK_PHONE

async def finish_registration(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Save the phone number
    context.user_data["phone"] = update.message.text

    name = context.user_data.get("name")
    phone = context.user_data.get("phone")

    # Print to console (so you can see it while testing)
    print(f"Registered user → Name: {name}, Phone: {phone}")

    # Send a message back to the user
    await update.message.reply_text(
        f"✅ Registration complete!\n\nName: {name}\nPhone: {phone}"
    )

    # End the conversation
    return ConversationHandler.END

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("❌ Registration cancelled.")
    return ConversationHandler.END

# The handler we’ll import in main.py
register_handler = ConversationHandler(
    entry_points=[CommandHandler("register", start_registration)],
    states={
        ASK_NAME: [MessageHandler(filters.TEXT & ~filters.COMMAND, ask_phone)],
        ASK_PHONE: [MessageHandler(filters.TEXT & ~filters.COMMAND, finish_registration)],
    },
    fallbacks=[CommandHandler("cancel", cancel)],
)
