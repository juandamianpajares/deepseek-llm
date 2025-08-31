import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict
import requests
from dotenv import load_dotenv
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

app = FastAPI(title="DeepSeek LLM API", version="1.0.0")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Modelos Pydantic
class Message(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    messages: List[Message]
    model: Optional[str] = None
    temperature: Optional[float] = None
    max_tokens: Optional[int] = None

class ChatResponse(BaseModel):
    response: str
    model: str
    usage: Optional[Dict] = None

class DeepSeekClient:
    def __init__(self):
        self.api_key = os.getenv("DEEPSEEK_API_KEY")
        self.api_url = os.getenv("DEEPSEEK_API_URL", "https://api.deepseek.com/v1/chat/completions")
        self.model_name = os.getenv("MODEL_NAME", "deepseek-chat")
        
        if not self.api_key:
            logger.warning("API key no configurada. Usa el archivo .env para configurarla.")

    async def chat_completion(self, messages: List[Dict], **kwargs) -> Dict:
        """Enviar mensaje a la API de DeepSeek"""
        
        if not self.api_key:
            return {"error": "API key no configurada. Configura DEEPSEEK_API_KEY en el archivo .env"}
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": kwargs.get("model", self.model_name),
            "messages": messages,
            "temperature": kwargs.get("temperature", 0.7),
            "max_tokens": kwargs.get("max_tokens", 2048),
            "stream": False
        }
        
        try:
            response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logger.error(f"Error en la API de DeepSeek: {e}")
            return {"error": f"Error en la API: {str(e)}"}

client = DeepSeekClient()

@app.get("/")
async def root():
    return {"message": "DeepSeek LLM API funcionando", "status": "ok"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "deepseek-llm"}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    try:
        # Convertir a formato para la API
        messages = [{"role": msg.role, "content": msg.content} for msg in request.messages]
        
        response = await client.chat_completion(
            messages=messages,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens
        )
        
        if "error" in response:
            raise HTTPException(status_code=500, detail=response["error"])
        
        return ChatResponse(
            response=response["choices"][0]["message"]["content"],
            model=response["model"],
            usage=response.get("usage")
        )
        
    except Exception as e:
        logger.error(f"Error en el endpoint /chat: {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    
    logger.info(f"Iniciando servidor en {host}:{port}")
    uvicorn.run(app, host=host, port=port)
