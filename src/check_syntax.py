#!/usr/bin/env python3
# Script para verificar sintaxis de archivos Python

import sys
import os

def check_file_syntax(file_path):
    """Verificar sintaxis de un archivo Python"""
    try:
        with open(file_path, 'r') as f:
            source = f.read()
        compile(source, file_path, 'exec')
        print(f"✓ {file_path} - Sintaxis correcta")
        return True
    except SyntaxError as e:
        print(f"✗ {file_path} - Error de sintaxis:")
        print(f"  Línea {e.lineno}: {e.msg}")
        print(f"  {e.text}")
        return False
    except Exception as e:
        print(f"✗ {file_path} - Error: {e}")
        return False

# Verificar todos los archivos Python en el directorio
python_files = [f for f in os.listdir('.') if f.endswith('.py')]

print("Verificando sintaxis de archivos Python...")
all_good = True

for file in python_files:
    if not check_file_syntax(file):
        all_good = False

if all_good:
    print("\n✓ Todos los archivos tienen sintaxis correcta")
else:
    print("\n✗ Se encontraron errores de sintaxis")
    sys.exit(1)
