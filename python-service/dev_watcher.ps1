# Activates venv and starts the Outlook watcher (Windows only)
param()
$ErrorActionPreference = 'Stop'

Push-Location $PSScriptRoot
if (-not (Test-Path .venv)) {
  Write-Host "Venv not found. Run dev_setup.ps1 first." -ForegroundColor Yellow
  Pop-Location
  exit 1
}
$python = Join-Path $PSScriptRoot ".venv/Scripts/python.exe"
Start-Process -FilePath $python -ArgumentList "watcher.py" -WorkingDirectory $PSScriptRoot
Write-Host "Watcher starting..."
Pop-Location