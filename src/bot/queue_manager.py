import asyncio
from downloaders.youtube import download_youtube_video
from downloaders.spotify import download_spotify_track

download_queue = asyncio.Queue()

async def queue_download_request(user_id: int, url: str, platform: str, context, update):
    await download_queue.put((user_id, url, platform, context, update))

async def download_worker():
    while True:
        user_id, url, platform, context, update = await download_queue.get()

        try:
            msg = await update.message.reply_animation(
                animation="https://i.gifer.com/2H0E.gif",
                caption="Downloading in progress… ⌛"
            )

            if platform == "youtube":
                path = download_youtube_video(url)
            elif platform == "spotify":
                path = download_spotify_track(url)
            else:
                await update.message.reply_text("Unsupported platform.")
                await download_queue.task_done()
                continue

            await msg.delete()

            await context.bot.send_video(
                chat_id=update.effective_chat.id,
                video=open(path, 'rb'),
                caption='👆'
            )

        except Exception as e:
            await update.message.reply_text(f"Error: {e}")
        finally:
            await download_queue.task_done()

