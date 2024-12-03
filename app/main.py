from typing import Union

from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

from .mp3transcribe import Mp3Transcribe, AudioFile

load_dotenv()
app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}



@app.post("/mp3transcribe/")
def transcribe_mp3(audio_file: AudioFile):
    """
    Transcribes an MP3 audio file.

    This endpoint accepts an MP3 audio file, downloads it, and transcribes the audio content to text.

    Args:
        audio_file (mp3transcribe.AudioFile): An object containing the URL and language of the MP3 audio file to be transcribed.

    Returns:
        dict: A dictionary containing the transcribed text.

    Raises:
        HTTPException: If the audio file cannot be downloaded, an HTTP 500 error is raised.
    """
    mp3 = Mp3Transcribe(audio_file.url, audio_file.lang)
    if not mp3.download():
        raise HTTPException(status_code=500, detail="Failed to download audio file")
    transcript = mp3.transcribe()
    return {"text": transcript}
