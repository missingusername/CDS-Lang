import os
import pandas as pd
from matplotlib import pyplot as plt
from transformers import pipeline
import codecarbon
from tqdm import tqdm

# Get the directory where the script is located
script_directory = os.path.dirname(os.path.realpath(__file__))
# Change the current working directory to the directory of the script
os.chdir(script_directory)

classifier = pipeline("text-classification", 
                      model="j-hartmann/emotion-english-distilroberta-base", 
                      return_all_scores=True)

# Step 2: Define the extract_label function
def extract_label(sentence):
    predictions = classifier(sentence)
    label = max(predictions[0], key=lambda x: x['score'])['label']
    return label

# Step 1: Read the CSV file into a pandas DataFrame
script_df = pd.read_csv('../in/Game_of_Thrones_Script.csv')

# Step 2: Get the unique values from the "seasons" column
seasons = script_df['Season'].unique().tolist()

# Step 3: Create an empty DataFrame called season_labels_df with the unique seasons
season_labels_df = pd.DataFrame({'Season': seasons})

# Set 'Season' as the index column in season_labels_df.
# This allows us to use 'Season' as a key to locate specific cells later on.
# 'inplace=True' modifies the DataFrame directly, instead of returning a new DataFrame.
season_labels_df.set_index('Season', inplace=True)

print(season_labels_df)

# Step 4: Process each row in script_df
for index, row in tqdm(script_df.iterrows(), total=len(script_df), desc="Processing Sentences"):
    season = row['Season']
    sentence = str(row['Sentence'])     #making sure that the sentence is treated as a string, to combat sentences like e.g. "None" which would get treated as a None value.
    
    # Print additional information without disrupting the progress bar
    tqdm.write(f"Processing sentence {index} in {season}: {sentence[:30]}...")
    
    label = extract_label(sentence)
    
    # If the label doesn't already exist as a column, create it
    if label not in season_labels_df.columns:
        season_labels_df[label] = 0

    # Increment the count for the label in the appropriate season row
    season_labels_df.at[season, label] += 1
    # Print additional information without disrupting the progress bar
    tqdm.write(f"Current season labels:\n{season_labels_df.to_string()}\n")

# return the normal index column
season_labels_df.reset_index(inplace=True)

season_labels_df.to_csv('../out/test.csv')