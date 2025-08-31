from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from .services.deepseek_client import DeepSeekClient
from .models.schemas import ChatRequest, ChatResponse, Message
import uvicorn

app = FastAPI(title="DeepSeek LLM API", version="1.0.0")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

client = DeepSeekClient()

@app.get("/")
async def root():
    return {"message": "DeepSeek LLM API funcionando"}

@app.post("/chat", response_model=ChatResponse)
async def chat_completion(request: ChatRequest):
    try:
        # Convertir Pydantic models a dict para la API
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
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "deepseek-llm"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
