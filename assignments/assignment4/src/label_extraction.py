import os
import pandas as pd
from transformers import pipeline
from tqdm import tqdm
from codecarbon import EmissionsTracker

# Get the directory where the script is located
script_directory = os.path.dirname(os.path.realpath(__file__))
# Change the current working directory to the directory of the script
os.chdir(script_directory)

in_folder = os.path.join('..', 'in')
out_folder = os.path.join('..', 'out')

# Function to initialize the sentiment analysis pipeline
def initialize_pipeline():
    print('test')
    return pipeline("text-classification", 
                    model="j-hartmann/emotion-english-distilroberta-base", 
                    return_all_scores=True)

# Function to extract the emotion label from a sentence using the initialized pipeline
def extract_label(classifier, sentence):
    predictions = classifier(sentence)
    label = max(predictions[0], key=lambda x: x['score'])['label']
    return label

# Function to process each row in the script dataframe
def process_rows(script_df, output_df, classifier):
    for index, row in tqdm(script_df.iterrows(), total=len(script_df), desc="Processing Sentences"):
        season = row['Season']
        sentence = str(row['Sentence'])  # Ensure sentence is treated as string
        
        # Print additional information without disrupting the progress bar
        tqdm.write(f"Processing sentence {index} in Season {season}: {sentence[:30]}...")
        
        label = extract_label(classifier, sentence)
        
        # If the label doesn't already exist as a column, create it
        if label not in output_df.columns:
            output_df[label] = 0
        
        # Increment the count for the label in the appropriate season row
        output_df.at[season, label] += 1
        
        # Print current season labels without disrupting the progress bar
        tqdm.write(f"Current season labels:\n{output_df.to_string()}\n")
    
    return output_df

# Function to create the initial season_labels_df DataFrame
def create_df_from_unique(script_df, target_column):
    unique_values = script_df[target_column].unique().tolist()
    new_df = pd.DataFrame({target_column: unique_values})
    return new_df

# Main function to orchestrate the entire process
def main():
    # Check if season_labels.csv already exists
    if os.path.exists(os.path.join(out_folder, 'season_labels.csv')):
        print("season_labels.csv already exists. Skipping script execution.")
        return

    # Step 1: Read the CSV file into a pandas DataFrame
    script_df = pd.read_csv(os.path.join(in_folder, 'Game_of_Thrones_Script.csv'))

    classifier = initialize_pipeline()

    # Initialize season_labels_df
    season_labels_df = create_df_from_unique(script_df, 'Season')

    # Set 'Season' as the index column in season_labels_df.
    # This allows us to use 'Season' as a key to locate specific cells later on.
    # 'inplace=True' modifies the DataFrame directly, instead of returning a new DataFrame.
    season_labels_df.set_index('Season', inplace=True)
    
    # Process each row in script_df
    season_labels_df = process_rows(script_df, season_labels_df, classifier)
    
    # Reset index for final CSV output
    season_labels_df.reset_index(inplace=True)
    
    # Save the DataFrame to a CSV file
    season_labels_df.to_csv(os.path.join(out_folder, 'season_labels.csv'), index=False)


if __name__ == "__main__":
    main()