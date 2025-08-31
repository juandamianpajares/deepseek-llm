import requests
import json
from typing import Dict, List, Optional
from ..utils.config import config

class DeepSeekClient:
    def __init__(self):
        self.api_key = config.DEEPSEEK_API_KEY
        self.api_url = config.DEEPSEEK_API_URL
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    async def chat_completion(self, 
                            messages: List[Dict[str, str]],
                            model: Optional[str] = None,
                            temperature: Optional[float] = None,
                            max_tokens: Optional[int] = None) -> Dict:
        """Envía una solicitud de chat a la API de DeepSeek"""
        
        payload = {
            "model": model or config.MODEL_NAME,
            "messages": messages,
            "temperature": temperature or config.TEMPERATURE,
            "max_tokens": max_tokens or config.MAX_TOKENS,
            "stream": False
        }

        try:
            response = requests.post(
                self.api_url,
                headers=self.headers,
                json=payload,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
            
        except requests.exceptions.RequestException as e:
            return {"error": f"Error en la API: {str(e)}"}

    async def stream_chat(self, 
                         messages: List[Dict[str, str]],
                         model: Optional[str] = None) -> None:
        """Streaming de respuestas (implementación básica)"""
        # Implementación para streaming
        pass
