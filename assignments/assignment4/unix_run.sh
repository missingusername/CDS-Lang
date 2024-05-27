#!/bin/bash

# Activate the virtual environment
source ./env/bin/activate

# Run the label_extraction.py script
python src/label_extraction.py

# Run the plot.py script with command-line arguments
python src/plot.py "$@"

# Deactivate the virtual environment
deactivate

#./unix_run.sh -a "your_artist_argument" -w "your_word_argument" -s
