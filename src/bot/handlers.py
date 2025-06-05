import re
import logging
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ContextTypes, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from bot.queue_manager import queue_download_request

logger = logging.getLogger(__name__)

# In-memory user state
user_state = {}  # user_id: 'youtube' or 'spotify'

def setup_handlers(app):
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(platform_selection))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))


# Utility: validate that input is a URL
def is_valid_url(text):
    return re.match(r'^https?://\S+$', text) is not None


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    logger.info(f"User {user_id} started the bot.")

    # Send image with logos
    await update.message.reply_photo(
        photo="https://i.postimg.cc/mkfnb66r/Chat-GPT-Image-May-24-2025-09-08-51-PM.png",
        caption="Choose a platform below to start downloading:"
    )

    # Then send buttons
    keyboard = [
        [
            InlineKeyboardButton("🟢 \n\n Spotify", callback_data="spotify"),
            InlineKeyboardButton("🔴 \n\n YouTube", callback_data="youtube")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👇 Pick one:", reply_markup=reply_markup)


async def platform_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    platform = query.data
    user_id = query.from_user.id

    if platform not in ["spotify", "youtube"]:
        logger.warning(f"User {user_id} selected invalid platform: {platform}")
        await query.edit_message_text("Invalid platform selected.")
        return

    user_state[user_id] = platform
    logger.info(f"User {user_id} selected platform: {platform}")
    await query.edit_message_text(f"Great! Now send me the {platform.capitalize()} link.")


async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    message = update.message.text

    if user_id not in user_state:
        logger.info(f"User {user_id} sent a link without selecting platform.")
        await update.message.reply_text("Please start by typing /start.")
        return

    if not is_valid_url(message):
        logger.warning(f"User {user_id} sent invalid URL: {message}")
        await update.message.reply_text("That doesn't look like a valid link. Please send a proper URL.")
        return

    platform = user_state[user_id]
    logger.info(f"User {user_id} submitted URL for {platform}: {message}")

    try:
        await queue_download_request(user_id, message, platform, context, update)

    except Exception as e:
        logger.error(f"Error processing request for user {user_id}: {e}")
        await update.message.reply_text("Something went wrong. Please try again later.")
    
    # Optional: reset user state after processing
    user_state.pop(user_id, None)
