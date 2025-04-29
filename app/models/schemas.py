from pydantic import BaseModel

class TranslationRequest(BaseModel):
    source_lang: str
    target_lang: str

class TranslationResponse(BaseModel):
    source_transcription: str
    translated_text: str
    tts_audio_url: str