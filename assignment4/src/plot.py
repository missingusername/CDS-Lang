import os
import argparse
import pandas as pd
import matplotlib.pyplot as plt

# Get the directory where the script is located
script_directory = os.path.dirname(os.path.realpath(__file__))
# Change the current working directory to the directory of the script
os.chdir(script_directory)

out_folder = os.path.join('..', 'out')

# Function to plot the distribution of emotions for each season, optioanlly exclusing labels
def plot_emotion_distribution(season_labels_df, exclude_labels=None):
    if exclude_labels is None:
        exclude_labels = []

    num_seasons = len(season_labels_df)
    num_cols = 4  # 4 subplots per row
    num_rows = (num_seasons + num_cols - 1) // num_cols

    fig, axes = plt.subplots(num_rows, num_cols, figsize=(25, 5 * num_rows))
    axes = axes.flatten()

    for i, (season, row) in enumerate(season_labels_df.iterrows()):
        ax = axes[i]
        filtered_row = row.drop(['Season'] + exclude_labels)
        filtered_row.plot(kind='bar', ax=ax)
        ax.set_title(f'Emotion Distribution - Season #{season}')
        ax.set_xlabel('Emotion')
        ax.set_ylabel('Frequency')

    plt.tight_layout()

    # Construct the filename based on potentially excluded labels
    exclude_str = "_excluding_" + "_".join(exclude_labels) if exclude_labels else ""
    filename = f'emotion_distribution_per_season{exclude_str}.png'
    plt.savefig(os.path.join(out_folder, filename))
    plt.close()
    
# Function to plot the relative frequency of each emotion across all seasons
def plot_emotion_relative_frequency(season_labels_df, exclude_labels=None):
    if exclude_labels is None:
        exclude_labels = []

    # Calculate relative frequencies
    relative_frequencies_df = calculate_relative_frequencies(season_labels_df.drop(columns=['Season']))

    included_emotions = [col for col in relative_frequencies_df.columns if col not in exclude_labels]
    num_emotions = len(included_emotions)
    num_cols = 2  # 4 subplots per row
    num_rows = (num_emotions + num_cols - 1) // num_cols

    fig, axes = plt.subplots(num_rows, num_cols, figsize=(20, 5 * num_rows))
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
    plt.savefig(os.path.join(out_folder, filename))
    plt.close()

# Function to calculate relative frequencies of emotion labels
def calculate_relative_frequencies(season_labels_df):
    relative_frequencies = season_labels_df.astype(float).copy()  # Ensure the DataFrame is float type
    for season in season_labels_df.index:
        total_count = season_labels_df.loc[season].sum()
        for label in season_labels_df.columns:
            relative_frequencies.at[season, label] = season_labels_df.at[season, label] / total_count
    return relative_frequencies

def main():
        # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Plot emotion distribution and their relative frequency across seasons.')
    parser.add_argument('-e', '--exclude', nargs='+', default=[], help='List of emotion labels to exclude')
    args = parser.parse_args()

    # Ensure exclude_labels are in lowercase
    exclude_labels = [label.lower() for label in args.exclude]
    
    print(exclude_labels)

    # Read season labels data
    season_labels_df = pd.read_csv(os.path.join(out_folder, 'season_labels.csv'))
    
    plot_emotion_distribution(season_labels_df, exclude_labels)
    plot_emotion_relative_frequency(season_labels_df, exclude_labels)

if __name__ == "__main__":
    main()
