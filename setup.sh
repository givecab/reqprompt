#!/usr/bin/env bash
# ─── setup.sh — Linux / macOS ─────────────────────────────────────────────────
# Crea el entorno virtual e instala dependencias.

set -e

echo "=== ReqPrompt — Setup ==="

# Check Python
if ! command -v python3 &>/dev/null; then
  echo "ERROR: Python 3 no encontrado. Instalalo desde https://python.org"
  exit 1
fi

echo "→ Creando entorno virtual..."
python3 -m venv venv

echo "→ Instalando dependencias..."
source venv/bin/activate
pip install --upgrade pip -q
pip install -r requirements.txt -q

echo ""
echo "✓ Setup completo."
echo ""
echo "Para iniciar la app:"
echo "  Linux/macOS:  ./run.sh"
echo "  Windows:      run.bat"
