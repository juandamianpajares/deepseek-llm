#!/bin/bash

# Script para instalar dependencias desde requirements.txt

set -e

print_status() {
    echo -e "\033[0;32m[+]\033[0m $1"
}

print_error() {
    echo -e "\033[0;31m[ERROR]\033[0m $1"
}

# Verificar que estamos en el directorio correcto
if [ ! -d "venv" ]; then
    print_error "Directorio venv no encontrado. Ejecuta desde el directorio del proyecto."
    exit 1
fi

print_status "Activando entorno virtual..."
source venv/bin/activate

print_status "Actualizando pip..."
python -m pip install --upgrade pip

print_status "Instalando dependencias desde requirements.txt..."
if [ -f "requirements.txt" ]; then
    python -m pip install -r requirements.txt
else
    print_error "requirements.txt no encontrado"
    exit 1
fi

print_status "Verificando instalaciones..."
python -c "
required = ['torch', 'transformers', 'fastapi', 'uvicorn', 'langchain']
for pkg in required:
    try:
        __import__(pkg)
        print(f'✓ {pkg} instalado correctamente')
    except ImportError as e:
        print(f'✗ {pkg} no instalado: {e}')
"

print_status "Creando requirements-lock.txt..."
python -m pip freeze > requirements-lock.txt

print_status "¡Instalación completada!"
