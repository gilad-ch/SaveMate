import os
import uuid
import subprocess

DOWNLOAD_DIR = "downloads"

def download_spotify_track(url: str) -> str:
    filename = f"{uuid.uuid4()}.mp3"
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(current_dir, DOWNLOAD_DIR, filename)

    cmd = [
        "spotdl", url,
        "--output", output_path,
        "--format", "mp3",
    ]

    subprocess.run(cmd, check=True)
    return output_path

