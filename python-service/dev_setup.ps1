# Creates a Python venv and installs requirements
param()
$ErrorActionPreference = 'Stop'

Push-Location $PSScriptRoot
if (-not (Test-Path .venv)) {
  python -m venv .venv
}
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
Pop-Location
Write-Host "Setup complete. Activate with: .\\.venv\\Scripts\\Activate.ps1"