#!/usr/bin/env python3
# test_local.py - Prueba simple del modelo local

import sys
import os

# Agregar el directorio actual al path para importar local_llm
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    from local_llm import LocalLLMClient
except ImportError as e:
    print(f"Error de importación: {e}")
    print("Asegúrate de que local_llm.py esté en el mismo directorio")
    sys.exit(1)

def main():
    client = LocalLLMClient()
    
    # Mensajes de prueba
    test_cases = [
        [{"role": "user", "content": "Hola, ¿cómo estás?"}],
        [{"role": "user", "content": "¿Qué es la inteligencia artificial?"}],
        [{"role": "user", "content": "Cuéntame un chiste corto"}]
    ]
    
    for i, messages in enumerate(test_cases, 1):
        print(f"\n--- Prueba {i} ---")
        print(f"Pregunta: {messages[0]['content']}")
        
        response = client.generate_response(
            messages, 
            max_length=100, 
            temperature=0.8
        )
        
        if "error" in response:
            print(f"Error: {response['error']}")
        else:
            print("Respuesta:")
            print(response["choices"][0]["message"]["content"])
            print(f"Modelo: {response['model']}")
            print(f"Tokens: {response['usage']['total_tokens']}")

if __name__ == "__main__":
    main()
