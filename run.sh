#!/usr/bin/env bash
# ─── run.sh — Linux / macOS ───────────────────────────────────────────────────
set -e

if [ ! -d "venv" ]; then
  echo "Primero ejecutá: bash setup.sh"
  exit 1
fi

source venv/bin/activate
python main.py
