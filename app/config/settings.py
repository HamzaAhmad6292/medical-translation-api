from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    groq_api_key: str
    elevenlabs_api_key: str
    whisper_model: str = "whisper-large-v3-turbo"
    llm_model: str = "llama-3.3-70b-versatile"
    tts_model: str = "eleven_multilingual_v2"
    
    class Config:
        env_file = ".env"

settings = Settings()