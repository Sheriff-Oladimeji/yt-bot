# YouTube Transcript Telegram Bot

A Telegram bot that fetches YouTube video transcripts instantly. Send a YouTube URL, get the transcript!

## Features

- 🎥 Extract transcripts from any YouTube video with captions
- ⚡ Fast and reliable
- 🐳 Docker support for easy deployment
- 🔄 Auto-restart on failure
- 📱 Simple Telegram interface

## Demo

```
You: https://www.youtube.com/watch?v=dQw4w9WgXcQ
Bot: ⏳ Fetching transcript...
Bot: ✅ Transcript:

     [Full video transcript here...]
```

## Quick Start (Local)

### Prerequisites

- Python 3.9+
- Telegram Bot Token (from [@BotFather](https://t.me/botfather))

### Setup

1. **Clone the repository**
```bash
git clone https://github.com/Sheriff-Oladimeji/yt-bot.git
cd yt-bot
```

2. **Create virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate  # On Mac/Linux
# OR
.\venv\Scripts\activate  # On Windows
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Create .env file**
```bash
cp .env.example .env
# Edit .env and add your token:
# TELEGRAM_BOT_TOKEN=your_token_here
```

5. **Run the bot**
```bash
python telegram_bot.py
```

## Docker Deployment (Recommended)

### Local Testing

```bash
docker-compose up --build
```

### Production Deployment

See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) for complete VPS deployment instructions.

**Quick version:**
```bash
# On your VPS
git clone https://github.com/Sheriff-Oladimeji/yt-bot.git
cd yt-bot
nano .env  # Add your token
docker-compose up -d --build
```

## Usage

### Commands

- `/start` - Welcome message
- `/help` - Show help

### How to Use

1. Start a chat with your bot on Telegram
2. Send any YouTube URL
3. Receive the transcript instantly

### Supported URL Formats

- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`

## Project Structure

```
yt-bot/
├── telegram_bot.py          # Main bot script
├── test_transcript.py       # Local testing script
├── requirements.txt         # Python dependencies
├── Dockerfile              # Docker image configuration
├── docker-compose.yml      # Docker orchestration
├── .env.example           # Environment template
├── .gitignore            # Git ignore rules
├── DEPLOYMENT_GUIDE.md   # Deployment instructions
└── README.md            # This file
```

## Technology Stack

- **Python 3.11** - Core language
- **python-telegram-bot** - Telegram Bot API wrapper
- **youtube-transcript-api** - Transcript fetching
- **python-dotenv** - Environment variable management
- **Docker** - Containerization

## Configuration

Environment variables in `.env`:

```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

## Updating

```bash
# Local
git pull origin main
docker-compose up -d --build

# VPS (same commands)
git pull origin main
docker-compose up -d --build
```

## Troubleshooting

### "No transcript available"
- Video doesn't have captions/subtitles enabled
- Try another video

### Bot not responding
- Check if bot is running: `docker-compose ps`
- View logs: `docker-compose logs -f`
- Restart: `docker-compose restart`

### Docker issues
See [DEPLOYMENT_GUIDE.md](./DEPLOYMENT_GUIDE.md) for detailed troubleshooting.

## Development

### Local Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run without Docker
python telegram_bot.py

# Test transcript fetching
python test_transcript.py
```

### Testing

The `test_transcript.py` script lets you test transcript fetching without Telegram:

```bash
python test_transcript.py
# Paste a YouTube URL when prompted
```

## Limitations

- Only works for videos with available captions (auto-generated or manual)
- Cannot transcribe videos without captions
- Telegram message limit: 4096 characters (bot splits longer transcripts)

## Future Improvements

- [ ] Add fallback transcript methods (yt-dlp, Whisper)
- [ ] Support for multiple languages
- [ ] Download transcripts as files for very long videos
- [ ] Add timestamp information
- [ ] Support for playlist processing

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

MIT License - feel free to use for personal or commercial projects.

## Author

**Sheriff Oladimeji** ([@Sheriff-Oladimeji](https://github.com/Sheriff-Oladimeji))
- Founder of [Brikta](https://brikta.dev)

## Acknowledgments

- Built with [python-telegram-bot](https://github.com/python-telegram-bot/python-telegram-bot)
- Uses [youtube-transcript-api](https://github.com/jdepoix/youtube-transcript-api)
- Inspired by the need for quick YouTube transcript access

## Support

- 🐛 Report bugs via [GitHub Issues](https://github.com/Sheriff-Oladimeji/yt-bot/issues)
- 💬 Questions? Open a discussion
- ⭐ Star the repo if you find it useful!

---

Made with ❤️ by Sheriff Oladimeji