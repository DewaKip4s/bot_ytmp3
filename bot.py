import os, glob, asyncio
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
import yt_dlp

TOKEN = "8452000359:AAFzHCSaA4c9SrwCHYueDaC7ViuzW24FZCw"  # lebih aman via env var

DOWNLOAD_FOLDER = "downloads"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "Halo! Kirim link YouTube (bukan playlist), nanti saya kirim MP3.\n"
        "Contoh: https://youtu.be/dQw4w9WgXcQ"
    )
    await update.message.reply_text(msg)

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Kirim link YouTube lalu tunggu proses konversi MP3.")

async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip()
    if ("youtube.com" not in text) and ("youtu.be" not in text):
        await update.message.reply_text("Kirim link YouTube yang valid ya.")
        return

    await update.message.reply_text("Sedang proses… mohon tunggu ⏳")

    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{DOWNLOAD_FOLDER}/%(id)s.%(ext)s",  # pakai ID agar aman
        "noplaylist": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
        ],
        "quiet": True,
        "no_warnings": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(text, download=True)
            vid_id = info.get("id")
            title = info.get("title", "Audio")

        mp3_path = os.path.join(DOWNLOAD_FOLDER, f"{vid_id}.mp3")
        if not os.path.exists(mp3_path):
            # fallback jaga-jaga
            candidates = glob.glob(os.path.join(DOWNLOAD_FOLDER, f"{vid_id}*.mp3"))
            if candidates:
                mp3_path = candidates[0]

        if not os.path.exists(mp3_path):
            await update.message.reply_text("Gagal menemukan file MP3 yang dihasilkan.")
            return

        # kirim sebagai audio
        with open(mp3_path, "rb") as f:
            await update.message.reply_audio(
                audio=f,
                title=title
            )

    except Exception as e:
        await update.message.reply_text(f"Terjadi error: {e}")

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))

    print("Bot berjalan...")
    app.run_polling()

if __name__ == "__main__":
    main()
