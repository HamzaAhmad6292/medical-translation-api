from elevenlabs import ElevenLabs
import hashlib
import time
from pathlib import Path
from app.config.settings import settings

class TTSService:
    def __init__(self):
        # Initialize client 
        self.client = ElevenLabs(api_key=settings.elevenlabs_api_key)

    async def generate_audio(self, text: str) -> str:
        """Generate audio from text using ElevenLabs' API"""
        try:
            # Create unique filename from user id to ensure data security
            user_hash = hashlib.md5(text.encode()).hexdigest()[:8]
            timestamp = int(time.time())
            filename = f"translation_{user_hash}_{timestamp}.mp3"
            filepath = Path("/tmp/audio") / filename
            
            # Generate audio
            response = self.client.text_to_speech.convert(
                voice_id="JBFqnCBsd6RMkjVDRZzb",
                output_format="mp3_44100_128",
                text=text,
                model_id="eleven_multilingual_v2"
            )
            
            # Save audio file
            filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(filepath, "wb") as f:
                for chunk in response:
                    f.write(chunk)
            
            # In services/tts_service.py
            return f"https://medical-translation-api.onrender.com/tmp/audio/{filename}" 
            
        except Exception as e:
            raise RuntimeError(f"TTS generation failed: {str(e)}")