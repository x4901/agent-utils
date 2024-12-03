import logging
from pathlib import Path
from tempfile import TemporaryDirectory

from pydantic import BaseModel
import requests
from openai import OpenAI
from pydub import AudioSegment



class AudioFile(BaseModel):
    url: str
    lang: str = 'en'


class Mp3Transcribe:
    """
    A class to handle downloading and transcribing MP3 audio files using OpenAI's transcription service.

    Attributes:
        url (str): The URL of the MP3 file to download.
        lang (str): The language of the audio for transcription. Default is 'en'.
        client (OpenAI): An instance of the OpenAI client.
        temp_dir (TemporaryDirectory): A temporary directory to store downloaded and processed files.
        audio (Path): The path to the downloaded MP3 file.
        transcript (Path): The path to the generated transcript file.

    Methods:
        download() -> bool:
            Downloads the MP3 file from the specified URL and saves it to a temporary directory.
            Returns True if the download is successful, otherwise False.

        transcribe() -> str:
            Transcribes the downloaded MP3 file in 10-minute segments using OpenAI's transcription service.
            Saves the transcript to a text file in the temporary directory.
            Returns the transcribed text.
    """
    def __init__(self, url, lang='en'):
        self.url = url
        self.lang = lang
        self.client = OpenAI()
        self.temp_dir = TemporaryDirectory()

    def download(self) -> bool:
        self.audio = Path(self.temp_dir.name).joinpath('audio.mp3')
        logging.debug(f'Downloading {self.url} to {self.audio}')
        response = requests.get(self.url)
        if response.status_code != 200:
            logging.error(f'Failed to download {self.url}, response {response}')
            return False
        with open(self.audio, 'wb') as f:
            f.write(response.content)
        logging.debug(f'Downloaded {self.url} to {self.audio}')
        return True

    def transcribe(self):
        audio_file = AudioSegment.from_mp3(self.audio)
        ten_minutes = 10 * 60 * 1000
        audio_10s = audio_file[::ten_minutes]
        self.transcript = Path(self.temp_dir.name).joinpath('transcript.txt')
        with open(self.transcript, 'w') as t:
            i = 0
            for audio in audio_10s:
                logging.debug(f'Transcribing segment {i}')
                seg10_name = Path(self.temp_dir.name).joinpath(f'd10-{i}.mp3')
                audio.export(seg10_name, format="mp3")
                with open(seg10_name, 'rb') as f:
                    text = self.client.audio.transcriptions.create(
                        language=self.lang,
                        file=f,
                        model="whisper-1",
                        #prompt=prompt
                        response_format="text"
                    )
                    #prompt = transcript
                    t.write(text)
                i += 1 
            logging.debug(f'Transcribed {self.audio} to {self.transcript}')
        return self.transcript.read_text()

