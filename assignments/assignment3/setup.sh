#!/bin/bash

# Create a Python virtual environment named "env"
python3 -m venv env

# Activate the virtual environment
source env/bin/activate

# Install required libraries from requirements.txt
pip install -r requirements.txt

# Deactivate the virtual environment
deactivate
