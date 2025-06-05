import yt_dlp
import os
import uuid

DOWNLOAD_DIR = "downloads"

def download_youtube_video(url: str) -> str:
    """
    Downloads a YouTube video with audio and saves it as an MP4 file.

    Args:
        url (str): The URL of the YouTube video.

    Returns:
        str: Path to the downloaded video file.
    """
    # Create unique filename
    filename = f"{uuid.uuid4()}.mp4"
    output_dir = os.path.join(os.path.dirname(__file__), DOWNLOAD_DIR)
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, filename)

    # yt-dlp options
    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',  # ensure video and audio are both included
        'outtmpl': output_path,
        'merge_output_format': 'mp4',          # ensure output is mp4
        'quiet': True,
    }

    # Download the video
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

    return output_path




