#!/usr/bin/env python3
"""
YouTube Transcript Telegram Bot
With health check endpoint for monitoring
"""

import re
import logging
import asyncio
from aiohttp import web
from telegram import Update
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from youtube_transcript_api import YouTubeTranscriptApi

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# YouTube URL patterns
YOUTUBE_PATTERNS = [
    r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+",
]

# Global variable to track bot health
bot_healthy = False


def extract_video_id(url):
    """Extract video ID from various YouTube URL formats"""
    patterns = [
        r"(?:youtube\.com/watch\?v=|youtu\.be/)([^&\n?#]+)",
        r"youtube\.com/embed/([^&\n?#]+)",
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def is_youtube_url(text):
    """Check if text contains a YouTube URL"""
    for pattern in YOUTUBE_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return True
    return False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    user = update.effective_user
    await update.message.reply_text(
        f"Hi {user.first_name}! 👋\n\n"
        "Send me any YouTube video URL and I'll send you the transcript.\n\n"
        "Just paste the link and I'll handle the rest!"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    await update.message.reply_text(
        "📝 How to use:\n\n"
        "1. Send me a YouTube video URL\n"
        "2. Wait a moment while I fetch the transcript\n"
        "3. Receive the full transcript!\n\n"
        "Supported formats:\n"
        "• https://www.youtube.com/watch?v=VIDEO_ID\n"
        "• https://youtu.be/VIDEO_ID\n"
        "• https://www.youtube.com/embed/VIDEO_ID"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle messages containing YouTube URLs"""
    text = update.message.text

    # Check if message contains a YouTube URL
    if not is_youtube_url(text):
        await update.message.reply_text(
            "❌ Please send a valid YouTube URL.\n\n"
            "Use /help to see supported formats."
        )
        return

    # Send processing message
    processing_msg = await update.message.reply_text("⏳ Fetching transcript...")

    try:
        # Extract video ID
        video_id = extract_video_id(text)
        if not video_id:
            await processing_msg.edit_text("❌ Could not extract video ID from URL.")
            return

        logger.info(f"Fetching transcript for video ID: {video_id}")

        # Get the transcript
        ytt_api = YouTubeTranscriptApi()
        fetched_transcript = ytt_api.fetch(video_id)

        # Convert to text
        transcript = "\n".join([snippet.text for snippet in fetched_transcript])

        if not transcript or transcript.strip() == "":
            await processing_msg.edit_text(
                "❌ No transcript available for this video.\n\n"
                "The video might not have captions enabled."
            )
            return

        # Telegram message limit is 4096 characters
        MAX_LENGTH = 4000

        if len(transcript) <= MAX_LENGTH:
            # Send entire transcript if it fits
            await processing_msg.edit_text(f"✅ Transcript:\n\n{transcript}")
        else:
            # Split into multiple messages if too long
            await processing_msg.edit_text(
                "✅ Transcript (sending in parts due to length):"
            )

            # Split transcript into chunks
            chunks = []
            current_chunk = ""

            for line in transcript.split("\n"):
                if len(current_chunk) + len(line) + 1 <= MAX_LENGTH:
                    current_chunk += line + "\n"
                else:
                    chunks.append(current_chunk)
                    current_chunk = line + "\n"

            if current_chunk:
                chunks.append(current_chunk)

            # Send each chunk
            for i, chunk in enumerate(chunks, 1):
                await update.message.reply_text(
                    f"📄 Part {i}/{len(chunks)}:\n\n{chunk}"
                )

        logger.info(f"Successfully sent transcript for video ID: {video_id}")

    except Exception as e:
        logger.error(f"Error fetching transcript: {e}")
        await processing_msg.edit_text(
            f"❌ Error fetching transcript:\n\n{str(e)}\n\n"
            "This could be due to:\n"
            "• Video has no captions/subtitles\n"
            "• Video is private or restricted\n"
            "• Invalid video URL"
        )


async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Log errors caused by updates"""
    logger.error(f"Update {update} caused error {context.error}")


# Health check endpoint for monitoring
async def health_check(request):
    """Health check endpoint for Uptime Kuma"""
    if bot_healthy:
        return web.Response(
            text='{"status": "healthy", "service": "yt-transcript-bot"}',
            status=200,
            content_type="application/json",
        )
    else:
        return web.Response(
            text='{"status": "unhealthy", "service": "yt-transcript-bot"}',
            status=503,
            content_type="application/json",
        )


async def start_health_server():
    """Start health check HTTP server"""
    app = web.Application()
    app.router.add_get("/health", health_check)
    app.router.add_get("/", health_check)  # Root also works

    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", 8080)
    await site.start()
    logger.info("Health check server started on port 8080")


def main():
    """Start the bot"""
    import os
    from dotenv import load_dotenv

    global bot_healthy

    # Load environment variables from .env file
    load_dotenv()

    print("\n" + "=" * 60)
    print("🤖 YouTube Transcript Telegram Bot")
    print("=" * 60)

    # Get token from environment
    TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

    if not TOKEN:
        print("\n⚠️  TELEGRAM BOT TOKEN NOT FOUND")
        print("=" * 60)
        print("\nPlease provide your Telegram Bot Token:")
        print("(You can get one from @BotFather on Telegram)\n")
        TOKEN = input("Enter token: ").strip()

    if not TOKEN:
        print("❌ No token provided. Exiting.")
        return

    print("\n" + "=" * 60)
    print("✅ Bot Starting...")
    print("=" * 60)
    print(f"Token: {TOKEN[:10]}...{TOKEN[-5:]}")
    print("\n📱 Bot is now running!")
    print("💡 Open Telegram and send a YouTube URL to your bot")
    print("🏥 Health check available at http://localhost:8080/health")
    print("⚠️  Keep this terminal window open")
    print("🛑 Press Ctrl+C to stop\n")
    print("=" * 60 + "\n")

    # Create the Application
    application = Application.builder().token(TOKEN).build()

    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(
        MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message)
    )

    # Add error handler
    application.add_error_handler(error_handler)

    # Start health check server
    loop = asyncio.get_event_loop()
    loop.create_task(start_health_server())

    # Mark bot as healthy once it starts
    bot_healthy = True

    # Run the bot
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
