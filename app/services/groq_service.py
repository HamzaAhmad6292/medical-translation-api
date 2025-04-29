from groq import Groq
from app.config.settings import settings

class GroqService:
    def __init__(self):
        self.client = Groq(api_key=settings.groq_api_key)

    async def transcribe_audio(self, audio_path: str, source_lang: str) -> str:
        with open(audio_path, "rb") as audio_file:
            transcription = self.client.audio.transcriptions.create(
                file=audio_file,
                model=settings.whisper_model,
                language=source_lang,
                response_format="text"
            )
        return transcription