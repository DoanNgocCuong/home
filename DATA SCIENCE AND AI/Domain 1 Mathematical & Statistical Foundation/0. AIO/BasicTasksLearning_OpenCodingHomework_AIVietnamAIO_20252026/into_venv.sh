#!/bin/bash

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    python -m venv .venv
    echo "Created new virtual environment"
fi

# Activate the virtual environment
source .venv/bin/activate

# Optional: Install requirements if requirements.txt exists
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

echo "Virtual environment activated! Use 'deactivate' to exit."