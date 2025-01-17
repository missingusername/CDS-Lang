import os
import pandas as pd
from transformers import pipeline
from tqdm import tqdm
from codecarbon import EmissionsTracker

def set_working_directory():
    """Sets the working directory to the directory of the script."""
    script_directory = os.path.dirname(os.path.realpath(__file__))
    os.chdir(script_directory)

# Function to initialize the sentiment analysis pipeline
def initialize_pipeline():
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
        
        # Print information regarding current sentence being processed
        tqdm.write(f"Processing sentence {index} in {season}: {sentence[:30]}...")
        
        label = extract_label(classifier, sentence)
        
        # If the label doesn't already exist as a column, create it
        if label not in output_df.columns:
            output_df[label] = 0
        
        # Increment the count for the label in the appropriate season row
        output_df.at[season, label] += 1
        
        # Print current season label dataframe
        tqdm.write(f"Current season labels:\n{output_df.to_string()}\n")
    
    return output_df

# Function to create the initial season_labels_df DataFrame
def create_df_from_unique(script_df, target_column):
    unique_values = script_df[target_column].unique().tolist()
    new_df = pd.DataFrame({target_column: unique_values})
    return new_df

def ensure_directory_exists(path):
    """Ensures that the directory exists, creates it if it does not."""
    if not os.path.exists(path):
        os.makedirs(path)

# Main function to orchestrate the entire process
def main():
    set_working_directory()

    in_path = os.path.join('..','in')
    out_path = os.path.join('..','out')

    emissions_path = os.path.join(out_path, 'emissions')
    ensure_directory_exists(emissions_path)

    # Check if season_labels.csv already exists
    if os.path.exists(os.path.join(out_path, 'season_labels.csv')):
        print("season_labels.csv already exists. Skipping script execution.")
        return

    # Step 1: Read the CSV file into a pandas DataFrame
    script_df = pd.read_csv(os.path.join(in_path, 'Game_of_Thrones_Script.csv'))

    # Initialize CodeCarbon tracker
    tracker = EmissionsTracker(
        project_name="Emotion_classification",
        experiment_id="emotion_classifier",
        output_dir=emissions_path,
        output_file="emotion_emissions.csv"
    )

    # Track classifier initialization emissions
    tracker.start_task("initialize classifier")
    classifier = initialize_pipeline()
    tracker.stop_task()

    # Initialize season_labels_df
    season_labels_df = create_df_from_unique(script_df, 'Season')

    # Set 'Season' as the index column in season_labels_df.
    # This allows us to use 'Season' as a key to locate specific cells later on.
    # 'inplace=True' modifies the DataFrame directly, instead of returning a new DataFrame.
    season_labels_df.set_index('Season', inplace=True)
    
    # Process each row in script_df
    tracker.start_task("Emotion label classification")
    season_labels_df = process_rows(script_df, season_labels_df, classifier)
    tracker.stop_task()
    
    # Reset index for final CSV output
    season_labels_df.reset_index(inplace=True)
    
    # Save the DataFrame to a CSV file
    season_labels_df.to_csv(os.path.join(out_path, 'season_labels.csv'), index=False)

    # Stop the tracker at the end of execution
    tracker.stop()

if __name__ == "__main__":
    main()
