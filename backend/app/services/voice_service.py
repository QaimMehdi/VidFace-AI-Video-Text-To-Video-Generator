import os
import requests
import json
from typing import Optional, Dict, List
from app.core.config import settings

class VoiceService:
    """Service for text-to-speech functionality"""
    
    def __init__(self):
        self.elevenlabs_api_key = settings.ELEVENLABS_API_KEY
        self.openai_api_key = settings.OPENAI_API_KEY
        self.output_dir = "static/audio"
        self.ensure_output_dir()
    
    def ensure_output_dir(self):
        """Ensure output directory exists"""
        os.makedirs(self.output_dir, exist_ok=True)
    
    async def generate_speech(
        self,
        text: str,
        voice_id: str = "default",
        language: str = "en",
        speed: float = 1.0,
        output_filename: Optional[str] = None
    ) -> str:
        """Generate speech from text"""
        try:
            if self.elevenlabs_api_key:
                return await self.generate_with_elevenlabs(text, voice_id, speed, output_filename)
            elif self.openai_api_key:
                return await self.generate_with_openai(text, voice_id, language, output_filename)
            else:
                # Fallback to basic TTS or placeholder
                return await self.generate_placeholder_audio(text, output_filename)
                
        except Exception as e:
            raise Exception(f"Speech generation failed: {str(e)}")
    
    async def generate_with_elevenlabs(
        self, 
        text: str, 
        voice_id: str, 
        speed: float,
        output_filename: Optional[str] = None
    ) -> str:
        """Generate speech using ElevenLabs API"""
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        
        headers = {
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": self.elevenlabs_api_key
        }
        
        data = {
            "text": text,
            "model_id": "eleven_monolingual_v1",
            "voice_settings": {
                "stability": 0.5,
                "similarity_boost": 0.5,
                "speed": speed
            }
        }
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            if not output_filename:
                output_filename = f"elevenlabs_{hash(text)}.mp3"
            
            output_path = os.path.join(self.output_dir, output_filename)
            
            with open(output_path, "wb") as f:
                f.write(response.content)
            
            return output_path
        else:
            raise Exception(f"ElevenLabs API error: {response.status_code} - {response.text}")
    
    async def generate_with_openai(
        self, 
        text: str, 
        voice: str, 
        language: str,
        output_filename: Optional[str] = None
    ) -> str:
        """Generate speech using OpenAI TTS API"""
        url = "https://api.openai.com/v1/audio/speech"
        
        headers = {
            "Authorization": f"Bearer {self.openai_api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "tts-1",
            "input": text,
            "voice": voice,  # alloy, echo, fable, onyx, nova, shimmer
            "response_format": "mp3"
        }
        
        response = requests.post(url, json=data, headers=headers)
        
        if response.status_code == 200:
            if not output_filename:
                output_filename = f"openai_{hash(text)}.mp3"
            
            output_path = os.path.join(self.output_dir, output_filename)
            
            with open(output_path, "wb") as f:
                f.write(response.content)
            
            return output_path
        else:
            raise Exception(f"OpenAI API error: {response.status_code} - {response.text}")
    
    async def generate_placeholder_audio(
        self, 
        text: str, 
        output_filename: Optional[str] = None
    ) -> str:
        """Generate placeholder audio (for development/testing)"""
        if not output_filename:
            output_filename = f"placeholder_{hash(text)}.wav"
        
        output_path = os.path.join(self.output_dir, output_filename)
        
        # Create a simple sine wave as placeholder
        import numpy as np
        import soundfile as sf
        
        # Generate a simple tone
        sample_rate = 22050
        duration = len(text.split()) * 0.5  # Rough estimate
        t = np.linspace(0, duration, int(sample_rate * duration))
        audio = np.sin(2 * np.pi * 440 * t) * 0.3  # 440 Hz tone
        
        sf.write(output_path, audio, sample_rate)
        
        return output_path
    
    async def get_available_voices(self) -> List[Dict]:
        """Get available voices from ElevenLabs"""
        if not self.elevenlabs_api_key:
            return self.get_default_voices()
        
        try:
            url = "https://api.elevenlabs.io/v1/voices"
            headers = {"xi-api-key": self.elevenlabs_api_key}
            
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                voices_data = response.json()
                return [
                    {
                        "id": voice["voice_id"],
                        "name": voice["name"],
                        "category": voice.get("category", "general"),
                        "description": voice.get("description", ""),
                        "language": voice.get("labels", {}).get("language", "en")
                    }
                    for voice in voices_data["voices"]
                ]
            else:
                return self.get_default_voices()
                
        except Exception:
            return self.get_default_voices()
    
    def get_default_voices(self) -> List[Dict]:
        """Get default voice options"""
        return [
            {
                "id": "default",
                "name": "Default Voice",
                "category": "general",
                "description": "Default text-to-speech voice",
                "language": "en"
            },
            {
                "id": "professional",
                "name": "Professional",
                "category": "business",
                "description": "Professional business voice",
                "language": "en"
            },
            {
                "id": "friendly",
                "name": "Friendly",
                "category": "casual",
                "description": "Warm and friendly voice",
                "language": "en"
            },
            {
                "id": "narrator",
                "name": "Narrator",
                "category": "storytelling",
                "description": "Deep narrator voice",
                "language": "en"
            }
        ]
    
    async def get_voice_by_id(self, voice_id: str) -> Optional[Dict]:
        """Get specific voice details"""
        voices = await self.get_available_voices()
        return next((voice for voice in voices if voice["id"] == voice_id), None) 