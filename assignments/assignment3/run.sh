#!/bin/bash

# Activate the virtual environment
source env/bin/activate

# Run the main.py file with command-line arguments passed to the script
python src/main.py "$@"

# Deactivate the virtual environment
deactivate
