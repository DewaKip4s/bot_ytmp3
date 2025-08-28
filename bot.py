import os
from telegram.ext import Application, CommandHandler
from telegram import Update
from telegram.ext import ContextTypes

TOKEN = os.environ.get("8452000359:AAFzHCSaA4c9SrwCHYueDaC7ViuzW24FZCw")
PORT = int(os.environ.get("PORT", 8080))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo bosku, bot sudah jalan 🚀")

def main():
    app = Application.builder().token(TOKEN).build()

    # handler command
    app.add_handler(CommandHandler("start", start))

    # mode webhook (biar stabil di Railway)
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"https://{os.environ.get('RAILWAY_STATIC_URL')}/{TOKEN}"
    )

if __name__ == "__main__":
    main()
