#!/usr/bin/env python3
# local_llm.py - Versión optimizada para poco espacio

import os
from transformers import pipeline
from typing import List, Dict
import logging
from dotenv import load_dotenv

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Cargar variables de entorno
load_dotenv()

class LocalLLMClient:
    def __init__(self):
        # Usar el modelo más pequeño disponible
        self.model_name = "distilgpt2"  # Muy pequeño y rápido
        self.pipeline = None
        
        logger.info(f"Inicializando modelo local: {self.model_name}")
        
    def load_model(self):
        """Cargar el modelo local usando pipeline optimizado"""
        try:
            self.pipeline = pipeline(
                "text-generation",
                model=self.model_name,
                device=-1,  # Forzar uso de CPU
                max_memory={0: "1GB"},  # Limitar uso de memoria
                torch_dtype="auto"
            )
            logger.info("Modelo local cargado exitosamente")
            return True
        except Exception as e:
            logger.error(f"Error cargando modelo local: {e}")
            return False
    
    def generate_response(self, messages: List[Dict], **kwargs) -> Dict:
        """Generar respuesta usando modelo local optimizado"""
        
        if self.pipeline is None:
            if not self.load_model():
                return {"error": "No se pudo cargar el modelo local"}
        
        # Convertir mensajes a texto de forma eficiente
        conversation = "\n".join([f"{msg['role']}: {msg['content']}" for msg in messages])
        conversation += "\nassistant: "
        
        try:
            # Generar respuesta con parámetros optimizados
            result = self.pipeline(
                conversation,
                max_length=kwargs.get("max_length", 100),  # Más corto
                temperature=kwargs.get("temperature", 0.7),
                do_sample=True,
                num_return_sequences=1,
                pad_token_id=self.pipeline.tokenizer.eos_token_id,
                truncation=True  # Truncar si es muy largo
            )
            
            response = result[0]['generated_text']
            
            # Extraer solo la parte del assistant
            if "assistant:" in response:
                response = response.split("assistant:")[-1].strip()
            
            return {
                "choices": [{
                    "message": {
                        "content": response[:200],  # Limitar longitud
                        "role": "assistant"
                    }
                }],
                "model": self.model_name,
                "usage": {
                    "prompt_tokens": len(conversation.split()),
                    "completion_tokens": len(response.split()),
                    "total_tokens": len(conversation.split()) + len(response.split())
                }
            }
            
        except Exception as e:
            logger.error(f"Error generando respuesta: {e}")
            return {"error": f"Error en generación local: {str(e)}"}

# Prueba del cliente local
if __name__ == "__main__":
    client = LocalLLMClient()
    
    test_messages = [
        {"role": "user", "content": "Hola, ¿cómo estás?"}
    ]
    
    result = client.generate_response(test_messages)
    
    if "error" in result:
        print(f"Error: {result['error']}")
    else:
        print("Respuesta del modelo local:")
        print(result["choices"][0]["message"]["content"])
