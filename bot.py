import yt_dlp
import os

def download_audio(url: str, filename: str = "audio.mp3"):
    """Download audio (MP3) dari YouTube"""
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": filename,
        "postprocessors": [
            {"key": "FFmpegExtractAudio", "preferredcodec": "mp3", "preferredquality": "192"}
        ]
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return filename

def download_video(url: str, filename: str = "video.mp4"):
    """Download video (MP4) dari YouTube"""
    ydl_opts = {
        "format": "best[ext=mp4]",
        "outtmpl": filename
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return filename
