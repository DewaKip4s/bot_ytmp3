import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = os.environ.get("8452000359:AAFzHCSaA4c9SrwCHYueDaC7ViuzW24FZCw")  # bot token kamu diset di Railway/Heroku
PORT = int(os.environ.get("PORT", 8080))

app = Flask(__name__)
application = Application.builder().token(TOKEN).build()

# --- Command handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo bosku, bot sudah jalan via webhook 🚀")

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

# --- Webhook ---
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok", 200

@app.route("/")
def index():
    return "Bot is running with webhook!", 200

if __name__ == "__main__":
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"https://{os.environ.get('RAILWAY_URL', 'your-app.up.railway.app')}/{TOKEN}"
    )
