#!/bin/bash

# Activate the virtual environment
source ./env/bin/activate

# Run the plot.py script
python src/plot.py

# Deactivate the virtual environment
deactivate

#./unix_run.sh -a "your_artist_argument" -w "your_word_argument" -s
