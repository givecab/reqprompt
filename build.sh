#!/usr/bin/env bash
set -euo pipefail

APP_NAME="ReqPrompt"
ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VENV_DIR="$ROOT_DIR/venv"
ICON_PNG="$ROOT_DIR/assets/icono.png"
MACOS_ICONSET_DIR="$ROOT_DIR/build/${APP_NAME}.iconset"
MACOS_ICNS="$ROOT_DIR/build/${APP_NAME}.icns"

cd "$ROOT_DIR"

echo "=== ${APP_NAME} - Build ==="

if ! command -v python3 >/dev/null 2>&1; then
  echo "ERROR: Python 3 no encontrado. Instalalo desde https://python.org"
  exit 1
fi

if [ ! -d "$VENV_DIR" ]; then
  echo "→ Entorno virtual no encontrado. Ejecutando setup inicial..."
  bash "$ROOT_DIR/setup.sh"
fi

echo "→ Activando entorno virtual..."
source "$VENV_DIR/bin/activate"

echo "→ Instalando dependencias de compilacion..."
python -m pip install --upgrade pip -q
python -m pip install pyinstaller -q

echo "→ Limpiando artefactos previos..."
rm -rf "$ROOT_DIR/build" "$ROOT_DIR/dist"

generate_macos_icon() {
  if [ ! -f "$ICON_PNG" ]; then
    echo "ERROR: No se encontro el icono base en $ICON_PNG"
    exit 1
  fi

  mkdir -p "$MACOS_ICONSET_DIR"

  local size
  for size in 16 32 128 256 512; do
    sips -z "$size" "$size" "$ICON_PNG" --out "$MACOS_ICONSET_DIR/icon_${size}x${size}.png" >/dev/null
    sips -z $((size * 2)) $((size * 2)) "$ICON_PNG" --out "$MACOS_ICONSET_DIR/icon_${size}x${size}@2x.png" >/dev/null
  done

  iconutil -c icns "$MACOS_ICONSET_DIR" -o "$MACOS_ICNS"
}

if [ "$(uname -s)" = "Darwin" ]; then
  echo "→ Generando icono macOS (.icns)..."
  generate_macos_icon
fi

echo "→ Compilando aplicacion..."
python -m PyInstaller --noconfirm --clean "$ROOT_DIR/ReqPrompt.spec"

echo ""
echo "✓ Compilacion completada."
echo ""
if [ -d "$ROOT_DIR/dist/${APP_NAME}.app" ]; then
  echo "Salida: $ROOT_DIR/dist/${APP_NAME}.app"
else
  echo "Salida: $ROOT_DIR/dist/${APP_NAME}"
fi
