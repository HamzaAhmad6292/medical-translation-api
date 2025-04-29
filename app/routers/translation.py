from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from app.services.groq_service import GroqService
from app.services.translation_service import TranslationService
from app.services.tts_service import TTSService
from app.models.schemas import TranslationResponse
import os
from pathlib import Path

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

# Define upload directory
UPLOAD_DIR = Path("static/audio")

# Ensure upload directory exists
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/medical-translate", response_model=TranslationResponse)
async def handle_translation(
    audio_file: UploadFile = File(...),
    source_lang: str = Form(...),
    target_lang: str = Form(...)):
    
    source_lang = LANGUAGE_MAP.get(source_lang, source_lang)
    target_lang = LANGUAGE_MAP.get(target_lang, target_lang)

    if source_lang not in SUPPORTED_LANGUAGES:
        raise HTTPException(status_code=400, detail=f"Unsupported source language: {source_lang}")
    
    if target_lang not in SUPPORTED_LANGUAGES:
        raise HTTPException(status_code=400, detail=f"Unsupported target language: {target_lang}")
    
    # Generate a unique filename using timestamp and original filename
    filename = f"{"hello.webm"}"
    file_path = UPLOAD_DIR / filename
    
    # Write the uploaded file to the specified path
    with open(file_path, "wb") as f:
        f.write(await audio_file.read())
    
    try:
        # Step 1: Transcribe
        transcription = await GroqService().transcribe_audio(str(file_path), source_lang)
        
        # Step 2: Translate
        translated_text = await TranslationService().medical_translate(
            transcription, source_lang, target_lang
        )
        
        # Step 3: Generate TTS
        tts_service = TTSService()
        tts_url = await tts_service.generate_audio(translated_text)
        print(tts_url)

        
        
        return {
            "source_transcription": transcription,
            "translated_text": translated_text,
            "tts_audio_url": tts_url,
            "file_path": str(file_path)  # Optionally return the file path for reference
        }
        
    except Exception as e:
        # Delete the file if an error occurs
        if os.path.exists(file_path):
            os.unlink(file_path)
        raise HTTPException(status_code=500, detail=f"Translation process failed: {str(e)}")