Write-Host "Starting FastAPI Backend Server..." -ForegroundColor Green
Write-Host ""

Set-Location $PSScriptRoot
& .\venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
