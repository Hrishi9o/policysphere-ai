# ==============================================================================
# PolicySphere™ AI - 1-Click Launch Script (Windows PowerShell)
# ==============================================================================

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host " 🚀 Starting PolicySphere™ AI - Campus Policy Platform" -ForegroundColor White
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Check Python installation
$pythonCmd = (Get-Command py, python -ErrorAction SilentlyContinue | Select-Object -First 1).Name
if (-not $pythonCmd) {
    Write-Host "[ERROR] Python is not installed or not in PATH." -ForegroundColor Red
    exit 1
}

Write-Host "[1/3] Using Python: $pythonCmd" -ForegroundColor Green

# 2. Check if vector index exists; if missing, build it
if (-not (Test-Path "data\vector_index.pkl")) {
    Write-Host "[2/3] Building vector index from data/handbook.md..." -ForegroundColor Yellow
    & $pythonCmd src\ingest.py
} else {
    Write-Host "[2/3] Vector index verified (data/vector_index.pkl)." -ForegroundColor Green
}

# 3. Launch FastAPI server & UI
Write-Host "[3/3] Launching PolicySphere™ AI at http://localhost:8000..." -ForegroundColor Cyan
Write-Host "      Press CTRL+C to stop the server.`n" -ForegroundColor DarkGray

& $pythonCmd api.py

