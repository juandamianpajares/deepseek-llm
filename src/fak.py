#!/usr/bin/env python3
# fak.py corregido con fallback local

import os
import sys
from dotenv import load_dotenv

# Agregar el directorio padre al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from local_llm import HybridLLMClient
import asyncio

# Cargar variables de entorno
load_dotenv()

async def main():
    client = HybridLLMClient()
    
    messages = [
        {"role": "user", "content": "Hola, ¿puedes explicarme qué es la inteligencia artificial?"}
    ]
    
    print("Enviando mensaje...")
    
    try:
        response = await client.chat_completion(
            messages=messages,
            model="deepseek-chat",
            temperature=0.7,
            max_tokens=500
        )
        
        if "error" in response:
            print(f"Error: {response['error']}")
        else:
            print("Respuesta recibida:")
            print("-" * 50)
            print(response["choices"][0]["message"]["content"])
            print("-" * 50)
            print(f"Modelo: {response['model']}")
            print(f"Tokens usados: {response['usage']['total_tokens']}")
            
    except Exception as e:
        print(f"Error general: {e}")

if __name__ == "__main__":
    asyncio.run(main())
