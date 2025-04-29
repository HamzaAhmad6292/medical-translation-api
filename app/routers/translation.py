from fastapi import APIRouter, UploadFile, File, Form
from fastapi.responses import JSONResponse
from app.services.groq_service import GroqService
from app.services.translation_service import TranslationService
from app.services.tts_service import TTSService
from app.models.schemas import TranslationResponse
import tempfile
import os

router = APIRouter(prefix="/api/v1", tags=["translation"])

# Add near top of translation.py
SUPPORTED_LANGUAGES = {
    "oc", "tg", "am", "nn", "haw", "yue", "et", "be", "su", "id",
    "da", "th", "bg", "mi", "eu", "sq", "gl", "it", "sw", "si",
    "km", "fo", "tk", "ro", "az", "br", "mn", "mr", "ps", "tr",
    "bn", "is", "ne", "sa", "lb", "ba", "zh", "de", "pt", "pl",
    "he", "uk", "kk", "ar", "hi", "hr", "te", "yo", "sd", "tt",
    "jv", "sv", "fi", "la", "sk", "sr", "lo", "ln", "en", "ca",
    "sn", "mt", "my", "bo", "tl", "es", "el", "hu", "ta", "so",
    "af", "ht", "ko", "fr", "no", "lv", "pa", "cs", "fa", "sl",
    "ka", "gu", "yi", "uz", "ha", "ru", "vi", "ur", "cy", "mk",
    "bs", "ja", "nl", "ms", "ml", "kn", "hy", "mg", "as", "lt"
}

LANGUAGE_MAP = {
    "en-US": "en",
    "es-ES": "es",
    "fr-FR": "fr",
    "de-DE": "de",
    "hi-IN": "hi",
    "zh-CN": "zh",
    "ar-SA": "ar"
}

@router.post("/medical-translate", response_model=TranslationResponse)
async def handle_translation(
    audio_file: UploadFile = File(...),
    source_lang: str = Form(...),
    target_lang: str = Form(...)):
     
    
     source_lang = LANGUAGE_MAP.get(source_lang, source_lang)
     target_lang = LANGUAGE_MAP.get(target_lang, target_lang)

     if source_lang not in SUPPORTED_LANGUAGES:
        raise HTTPException(400, f"Unsupported source language: {source_lang}")
    
    # Validate supported languages

    # Handle audio file
     with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as tmp_file:
        tmp_file.write(await audio_file.read())
        audio_path = tmp_file.name
    
     try:
        # Step 1: Transcribe
        transcription = await GroqService().transcribe_audio(audio_path, source_lang)
        
        # Step 2: Translate
        translated_text = await TranslationService().medical_translate(
            transcription, source_lang, target_lang
        )
        
        # Step 3: Generate TTS
        tts_service = TTSService()
        tts_url = await tts_service.generate_audio(translated_text)
        
        return {
            "source_transcription": transcription,
            "translated_text": translated_text,
            "tts_audio_url": tts_url
        }
        
     finally:
        os.unlink(audio_path)