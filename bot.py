from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import re
import os
from dotenv import load_dotenv

# بارگذاری فایل .env
load_dotenv()

TOKEN = os.getenv("TOKEN")
CHANNEL_ID = os.getenv("CHANNEL_ID")
ALLOWED_USERS = list(map(int, os.getenv("ALLOWED_USERS").split(",")))

translation_dict = {
    "Присоединяйтесь к розыгрышу!": "Join the giveaway!",
    "Призы:": "Prizes:",
    "Крайний срок:": "Deadline:",
    "Требования:": "Requirements:",
    "Только для Premium пользователей": "For Premium users only",
    "Мин. объем торгов:": "Minimum trading volume:",
    "Присоединяйтесь и удачи!": "Join in and good luck!"
}

def translate_text(text):
    for ru, en in translation_dict.items():
        text = re.sub(re.escape(ru), en, text)
    return text

async def translate_and_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    print("Message from user:", user_id, update.message.text)

    if user_id not in ALLOWED_USERS:
        await update.message.reply_text("You are not authorized.")
        return

    translated_text = translate_text(update.message.text)
    try:
        await context.bot.send_message(chat_id=CHANNEL_ID, text=translated_text)
        await update.message.reply_text("فرستادم کون خوشگله 💋")
    except Exception as e:
        await update.message.reply_text(f"Failed to send message: {e}")
        print("Error sending:", e)

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL & ~filters.COMMAND, translate_and_post))
    print("Bot started. Waiting for messages...")
    app.run_polling()

if __name__ == "__main__":
    main()
