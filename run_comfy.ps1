# Ensures the local .venv is active, then runs main.py using the venv's Python.
# Usage: ./run_comfy.ps1 [--port 8188] [additional args forwarded to main.py]

$scriptRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$venvPath = Join-Path $scriptRoot '.venv'
$pythonPath = Join-Path $venvPath 'Scripts\python.exe'
$activatePath = Join-Path $venvPath 'Scripts\Activate.ps1'
$mainPath = Join-Path $scriptRoot 'main.py'

if (-not (Test-Path $pythonPath)) {
    Write-Error "Virtual environment not found at $venvPath. Create it before running this script."
    exit 1
}

# Dot-source activation so the current session picks up the venv, but only if not already using it.
$venvActive = $env:VIRTUAL_ENV -and ($env:VIRTUAL_ENV -replace '/','\\') -ieq ($venvPath -replace '/','\\')
if (-not $venvActive) {
    if (-not (Test-Path $activatePath)) {
        Write-Error "Activation script missing at $activatePath"
        exit 1
    }
    . $activatePath
}

if (-not (Test-Path $mainPath)) {
    Write-Error "main.py not found at $mainPath"
    exit 1
}

# Run main.py, forwarding any additional arguments.
& $pythonPath $mainPath @args
exit $LASTEXITCODE
