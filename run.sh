#!/usr/bin/env bash
# ==============================================================================
# Dell PolicySphere™ - 1-Click Launch Script (Linux / macOS)
# ==============================================================================

set -e

echo "=========================================================="
echo " 🚀 Starting Dell PolicySphere™ - Campus AI Platform"
echo "=========================================================="

PYTHON_BIN=$(command -v python3 || command -v python)
if [ -z "$PYTHON_BIN" ]; then
    echo "[ERROR] Python 3 is not installed or not in PATH."
    exit 1
fi

echo "[1/3] Using Python: $PYTHON_BIN"

if [ ! -f "data/vector_index.pkl" ]; then
    echo "[2/3] Building vector index from data/handbook.md..."
    $PYTHON_BIN src/ingest.py
else
    echo "[2/3] Vector index verified (data/vector_index.pkl)."
fi

echo "[3/3] Launching Dell PolicySphere™ at http://localhost:8000..."
echo "      Press CTRL+C to stop the server."

$PYTHON_BIN api.py

