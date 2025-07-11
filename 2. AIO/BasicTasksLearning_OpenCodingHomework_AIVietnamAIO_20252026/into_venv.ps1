# Create virtual environment if it doesn't exist
if (-not (Test-Path ".venv")) {
    python -m venv .venv
    Write-Host "Created new virtual environment"
}

# Activate the virtual environment
.\.venv\Scripts\Activate.ps1

# Optional: Install requirements if requirements.txt exists
if (Test-Path "requirements.txt") {
    pip install -r requirements.txt
}

Write-Host "Virtual environment activated! Use 'deactivate' to exit."