import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt
from codecarbon import EmissionsTracker

def set_working_directory():
    """Sets the working directory to the directory of the script."""
    script_directory = os.path.dirname(os.path.realpath(__file__))
    os.chdir(script_directory)

# Function to plot the distribution of emotions for each season, optioanlly exclusing labels
def plot_emotion_distribution(season_labels_df, out_path, exclude_labels=None):
    if exclude_labels is None:
        exclude_labels = []

    num_seasons = len(season_labels_df)
    num_cols = 4  # 4 subplots per row
    num_rows = (num_seasons + num_cols - 1) // num_cols

    fig, axes = plt.subplots(num_rows, num_cols, figsize=(25, 10))
    axes = axes.flatten()

    for i, (season, row) in enumerate(season_labels_df.iterrows()):
        ax = axes[i]
        filtered_row = row.drop(['Season'] + exclude_labels)
        filtered_row.plot(kind='bar', ax=ax)
        ax.set_title(f'Emotion Distribution - Season #{season+1}')
        ax.set_xlabel('Emotion')
        ax.set_ylabel('Frequency')

    plt.tight_layout()

    # Construct the filename based on potentially excluded labels
    exclude_str = "_excluding_" + "_".join(exclude_labels) if exclude_labels else ""
    filename = f'emotion_distribution_per_season{exclude_str}.png'
    plt.savefig(os.path.join(out_path, filename))
    plt.close()
    
# Function to plot the relative frequency of each emotion across all seasons
def plot_emotion_relative_frequency(season_labels_df, out_path, exclude_labels=None):
    if exclude_labels is None:
        exclude_labels = []

    # Drop 'Season' and any columns specified in exclude_labels before calculating relative frequencies
    columns_to_drop = ['Season'] + exclude_labels
    relative_frequencies_df = calculate_relative_frequencies(season_labels_df.drop(columns=columns_to_drop))

    included_emotions = [col for col in relative_frequencies_df.columns if col not in exclude_labels]
    num_emotions = len(included_emotions)
    num_cols = 4  # 4 subplots per row
    num_rows = (num_emotions + num_cols - 1) // num_cols

    fig, axes = plt.subplots(num_rows, num_cols, figsize=(30, 10))
    axes = axes.flatten()

    seasons = season_labels_df['Season']
    for i, emotion in enumerate(included_emotions):
        ax = axes[i]
        ax.plot(seasons, relative_frequencies_df[emotion], marker='o')
        ax.set_title(f'Relative Frequency - {emotion}')
        ax.set_xlabel('Season')
        ax.set_ylabel('Relative Frequency')

    # Delete empty subplots
    for j in range(i + 1, len(axes)):
        fig.delaxes(axes[j])

    plt.tight_layout()

    # Construct the filename based on potentially excluded labels
    exclude_str = "_excluding_" + "_".join(exclude_labels) if exclude_labels else ""
    filename = f'relative_frequency_per_emotion{exclude_str}.png'
    plt.savefig(os.path.join(out_path, filename))
    plt.close()
    
# Function to calculate relative frequencies of emotion labels
def calculate_relative_frequencies(season_labels_df):
    relative_frequencies = season_labels_df.astype(float).copy()  # Ensure the DataFrame is float type
    for season in season_labels_df.index:
        total_count = season_labels_df.loc[season].sum() # calculate the sum of all emotion labels per season
        for label in season_labels_df.columns:
            #calculate the relative frequency of each emotion relative to the emotional sum of each season.
            relative_frequencies.at[season, label] = season_labels_df.at[season, label] / total_count 
    return relative_frequencies

def ensure_directory_exists(path):
    """Ensures that the directory exists, creates it if it does not."""
    if not os.path.exists(path):
        os.makedirs(path)

def main():
    set_working_directory()
    
    out_path = os.path.join('..','out')

    emissions_path = os.path.join(out_path, 'emissions')
    ensure_directory_exists(emissions_path)

    # Initialize CodeCarbon tracker
    tracker = EmissionsTracker(
        project_name="Emotion_plotting",
        experiment_id="emotion_plotter",
        output_dir=emissions_path,
        output_file="emotion_emissions.csv"
    )
    tracker.start()

    # Parse command-line arguments
    tracker.start_task('Argparse')
    parser = argparse.ArgumentParser(description='Plot emotion distribution and their relative frequency across seasons.')
    parser.add_argument('-e', '--exclude', nargs='+', default=[], help='List of emotion labels to exclude')
    args = parser.parse_args()
    tracker.stop_task()

    # Ensure exclude_labels are in lowercase
    exclude_labels = [label.lower() for label in args.exclude]

    # Read season labels data
    tracker.start_task('read emotion data')
    season_labels_df = pd.read_csv(os.path.join(out_path, 'season_labels.csv'))
    tracker.stop_task()
    
    tracker.start_task('plot emotion distribution')
    plot_emotion_distribution(season_labels_df, out_path, exclude_labels)
    tracker.stop_task()

    tracker.start_task('plot relative frequency')
    plot_emotion_relative_frequency(season_labels_df, out_path, exclude_labels)
    tracker.stop_task()

    tracker.stop()

if __name__ == "__main__":
    main()
