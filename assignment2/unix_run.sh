#!/bin/bash

# Activate the virtual environment
source ./env/bin/activate

# Run the vectorizer.py script first.
python src/vectorizer.py

# Run the LR.py script afterwards
python src/LR.py

# Run the MLP.py script
python src/MLP.py

# Deactivate the virtual environment
deactivate

#./unix_run.sh -a "your_artist_argument" -w "your_word_argument" -s
