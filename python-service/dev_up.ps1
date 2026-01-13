# Activates venv and starts the Flask app
param()
$ErrorActionPreference = 'Stop'

Push-Location $PSScriptRoot
if (-not (Test-Path .venv)) {
  Write-Host "Venv not found. Run dev_setup.ps1 first." -ForegroundColor Yellow
  Pop-Location
  exit 1
}
$python = Join-Path $PSScriptRoot ".venv/Scripts/python.exe"
Start-Process -FilePath $python -ArgumentList "app.py" -WorkingDirectory $PSScriptRoot
Write-Host "Flask app starting... Check http://127.0.0.1:5000/health"
Pop-Location