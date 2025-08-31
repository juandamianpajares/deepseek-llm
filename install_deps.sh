#!/bin/bash

# Script para instalar dependencias del proyecto

set -e

echo "Instalando dependencias para DeepSeek LLM..."

# Verificar que el entorno virtual está activado
if [ -z "$VIRTUAL_ENV" ]; then
    echo "Activando entorno virtual..."
    source venv/bin/activate
fi

# Instalar dependencias básicas
echo "Instalando dependencias básicas..."
pip install --upgrade pip
pip install python-dotenv requests

# Instalar PyTorch para CPU
echo "Instalando PyTorch..."
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu

# Instalar transformers y dependencias
echo "Instalando transformers..."
pip install transformers accelerate sentencepiece protobuf

# Instalar FastAPI y dependencias
echo "Instalando FastAPI..."
pip install fastapi uvicorn aiohttp websockets python-multipart

# Verificar instalaciones
echo "Verificando instalaciones..."
python -c "
import dotenv, requests, transformers, fastapi
print('Todas las dependencias instaladas correctamente')
print('dotenv version:', dotenv.__version__)
print('requests version:', requests.__version__)
print('transformers version:', transformers.__version__)
print('fastapi version:', fastapi.__version__)
"

echo "¡Instalación completada!"
