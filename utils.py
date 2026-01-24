import re

# YouTube URL patterns
YOUTUBE_PATTERNS = [
    r"(https?://)?(www\.)?(youtube\.com|youtu\.be)/.+",
]

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
