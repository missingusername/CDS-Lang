import os
import argparse
import pandas as pd
import string
from tqdm import tqdm
from gensim.downloader import load as gensim_load
from codecarbon import EmissionsTracker

parser = argparse.ArgumentParser(
    prog='Query expansion with word embeddings',
    description='Finds songs about ',
    epilog='Text at the bottom of help'
)
parser.add_argument('-a', '--artist', required=True, help='What artist to search for. Required.')
parser.add_argument('-w', '--word', required=True, help='What word to search for similar words to. Required.')
parser.add_argument('-s', '--save', required=False, action='store_true', help='Include this flag to save a csv of the results. Optional.')
args = parser.parse_args()

def set_working_directory():
    """Sets the working directory to the directory of the script."""
    script_directory = os.path.dirname(os.path.realpath(__file__))
    os.chdir(script_directory)

def load_model(model_name="glove-wiki-gigaword-50"):
    """Loads the specified word embedding model."""
    return gensim_load(model_name)

def load_data(file_name):
    """Loads data from a CSV file."""
    data_path = os.path.join('..', 'in', file_name)
    return pd.read_csv(data_path)

def filter_data(df, artist):
    """Filters the DataFrame to keep only rows where 'artist' column contains the given artist."""
    return df[df['artist'].str.lower() == artist.lower()]

def get_similar_words(model, word, topn=10):
    """Finds similar words using the word embedding model."""
    similar_words_tuples = model.most_similar(word, topn=topn)
    similar_words = [t[0] for t in similar_words_tuples]
    similar_words.append(word)
    return similar_words

def preprocess_text(text):
    """Preprocesses text by converting to lowercase and removing punctuation."""
    text_lower = text.lower()
    text_no_punctuation = text_lower.translate(str.maketrans('', '', string.punctuation))
    tokens = text_no_punctuation.split()
    return tokens

def scan_songs(input_df, similar_words):
    """Scans songs and counts occurrences of similar words."""
    scanned_songs_list = []
    for _, row in tqdm(input_df.iterrows()):
        text = row['text']
        similar_word_count = {word: 0 for word in similar_words}
        contains_similar = False
        tokens = preprocess_text(text)
        for word in tokens:
            if word in similar_word_count:
                similar_word_count[word] += 1
                contains_similar = True
        scanned_songs_list.append({
            'song': row['song'],
            'contains_similar': contains_similar,
            'similar_word_counts': similar_word_count
        })
    return pd.DataFrame(scanned_songs_list)

def calculate_similar_stats(df):
    """Calculates statistics about songs containing similar words."""
    true_count = df['contains_similar'].sum()
    false_count = len(df) - true_count
    total_count = len(df)
    true_percentage = round((true_count / total_count) * 100, 2)
    return true_count, false_count, total_count, true_percentage

def ensure_directory_exists(path):
    """Ensures that the directory exists, creates it if it does not."""
    if not os.path.exists(path):
        os.makedirs(path)

def save_results(df, artist, word, out_path):
    """Saves the results to a CSV file."""
    out_filename = f'{artist} songs about {word}.csv'
    df.to_csv(os.path.join(out_path, out_filename))
    print(f'Results saved in "/out" folder, as: "{out_filename}"')

def main():
    set_working_directory()

    out_path = os.path.join('..', 'out')

    emissions_path = os.path.join(out_path, 'emissions')

    ensure_directory_exists(emissions_path)

    tracker = EmissionsTracker(
        project_name="Query expansion",
        experiment_id="Query_expander",
        output_dir=emissions_path,
        output_file="Query_expansion_emissions.csv"
    )

    tracker.start_task('load model')
    model = load_model()
    tracker.stop_task()

    df = load_data('Spotify Million Song Dataset_exported.csv')

    filtered_df = filter_data(df, args.artist)

    tracker.start_task('find similar words')
    similar_words = get_similar_words(model, args.word)
    tracker.stop_task()
    
    tracker.start_task('scan songs for similar words')
    scanned_songs_df = scan_songs(filtered_df, similar_words)
    tracker.stop_task()

    true_count, false_count, total_count, true_percentage = calculate_similar_stats(scanned_songs_df)
    
    tracker.stop()

    print(f"""
You searched for songs by: {args.artist}
Which contained words similar to: {args.word}
Of the {total_count} total songs by {args.artist}:
    {true_count} songs contained words similar to {args.word}
    {false_count} songs did not contain words similar to {args.word}
    This means {true_percentage}% of {args.artist} songs contains words similar to {args.word}
""")
    
    if args.save:
        save_results(scanned_songs_df, args.artist, args.word, out_path)

if __name__ == '__main__':
    main()
