from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from youtube_transcript_api import YouTubeTranscriptApi
from utils import extract_video_id, is_youtube_url
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("YouTube Transcript API starting up")
    yield
    logger.info("YouTube Transcript API shutting down")


app = FastAPI(
    title="YouTube Transcript API",
    description="API for fetching YouTube video transcripts",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class TranscriptRequest(BaseModel):
    url: str


class TranscriptSegment(BaseModel):
    text: str
    start: float
    duration: float


class TranscriptResponse(BaseModel):
    video_id: str
    transcript: str
    segments: list[TranscriptSegment]


@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "yt-transcript-api"}


@app.get("/")
def root():
    return {"status": "ok", "service": "yt-transcript-api"}


@app.post("/transcript", response_model=TranscriptResponse)
def get_transcript(request: TranscriptRequest):
    url = request.url

    if not is_youtube_url(url):
        raise HTTPException(status_code=400, detail="Invalid YouTube URL")

    video_id = extract_video_id(url)
    if not video_id:
        raise HTTPException(status_code=400, detail="Could not extract video ID")

    try:
        logger.info(f"Fetching transcript for video ID: {video_id}")
        ytt_api = YouTubeTranscriptApi()
        transcript_data = ytt_api.fetch(video_id)

        full_text = "\n".join([snippet.text for snippet in transcript_data])

        segments = [
            TranscriptSegment(
                text=snippet.text,
                start=getattr(snippet, "start", 0.0),
                duration=getattr(snippet, "duration", 0.0),
            )
            for snippet in transcript_data
        ]

        return TranscriptResponse(
            video_id=video_id,
            transcript=full_text,
            segments=segments,
        )

    except Exception as e:
        logger.error(f"Error fetching transcript: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Failed to fetch transcript: {str(e)}",
        )
