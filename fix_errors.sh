#!/bin/bash

# Script para corregir errores en el proyecto DeepSeek LLM

set -e

print_status() {
    echo -e "\033[0;32m[+]\033[0m $1"
}

print_error() {
    echo -e "\033[0;31m[ERROR]\033[0m $1"
}

print_status "Corrigiendo errores en el proyecto..."

# Verificar y crear directorio models si no existe
if [ ! -d "src/models" ]; then
    print_status "Creando directorio src/models..."
    mkdir -p src/models
fi

# Crear/Corregir archivo schemas.py
print_status "Creando/actualizando src/models/schemas.py..."
cat > src/models/schemas.py << 'SCHEMAS'
from pydantic import BaseModel
from typing import List, Optional, Dict

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
SCHEMAS

# Verificar y crear directorio services si no existe
if [ ! -d "src/services" ]; then
    print_status "Creando directorio src/services..."
    mkdir -p src/services
fi

# Verificar y crear directorio utils si no existe
if [ ! -d "src/utils" ]; then
    print_status "Creando directorio src/utils..."
    mkdir -p src/utils
fi

# Crear archivo __init__.py en cada directorio
print_status "Creando archivos __init__.py..."
touch src/__init__.py
touch src/models/__init__.py
touch src/services/__init__.py
touch src/utils/__init__.py

# Actualizar requirements.txt si es necesario
if grep -q "pydantic" requirements.txt; then
    print_status "Requirements.txt ya contiene pydantic"
else
    print_status "Agregando pydantic a requirements.txt..."
    echo "pydantic==2.6.1" >> requirements.txt
fi

print_status "Correcciones aplicadas. Probando la aplicación..."

# Activar entorno virtual y probar
source venv/bin/activate

# Probar importaciones
if python -c "
from models.schemas import ChatRequest, ChatResponse, Message
print('✓ Schemas importados correctamente')
from typing import Dict, List, Optional
print('✓ Typing imports correctos')
import pydantic
print(f'✓ Pydantic {pydantic.VERSION} instalado')
"; then
    print_status "¡Todas las correcciones se aplicaron exitosamente!"
else
    print_error "Hubo errores en las importaciones. Revisa las dependencias."
    print_status "Instalando dependencias faltantes..."
    python -m pip install pydantic typing-extensions
fi

print_status "Ejecuta ./run.sh para iniciar la aplicación"
