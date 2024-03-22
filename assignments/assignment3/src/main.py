import gensim.downloader as api
import os
import argparse
import pandas as pd
import string

# Get the directory where the script is located
script_directory = os.path.dirname(os.path.realpath(__file__))
# Change the current working directory to the directory of the script
os.chdir(script_directory)

model = api.load("glove-wiki-gigaword-50")

parser = argparse.ArgumentParser(
                    prog='Query expansion with word embeddings',
                    description='Finds songs about ',
                    epilog='Text at the bottom of help')

#   what artist to search for
parser.add_argument('-a', '--artist', required=True, help='What artist to search for. Requiered.')
#   what word to search for
parser.add_argument('-w', '--word', required=True, help='What word to search for similar words to. Required.')
#   adding a boolean argument for whether to save a csv of the songs
parser.add_argument('-s', '--save', required=False, action='store_true', help='Include this flag to save a csv of the results. Optional.')

args = parser.parse_args()

data_file = 'Spotify Million Song Dataset_exported.csv'

data_path = os.path.join('..',
                         'in',
                         data_file)

df = pd.read_csv(data_path)

out_path = os.path.join('..',
                        'out')

filtered_df = df[df['artist'].str.lower() == args.artist.lower()]   # Filter the DataFrame to keep only rows where 'artist' column contains the given artist

similar_words_tuples = model.most_similar(args.word, topn=10)   #using gensim "most_similar" to get a list of tuples of the most similar words, and how similar they are

similar_words = [tuple[0] for tuple in similar_words_tuples]    #making a new list of just the words from the tuples.

def preprocess_text(text):
    # Convert text to lowercase
    text_lower = text.lower()
    
    # Remove punctuation
    text_no_punctuation = text_lower.translate(str.maketrans('', '', string.punctuation))
    
    # Split text into tokens
    tokens = text_no_punctuation.split()
    
    return tokens

def scan_songs(input_df):
    scanned_songs_list = []    # Create an empty list to store scanned songs

    for index, row in input_df.iterrows():
        text = row['text']
        similar_word_count = {word: 0 for word in similar_words}
        contains_similar = False
        
        tokens = preprocess_text(text)
        
        # Count occurrences of similar words in the text
        for word in tokens:
            if word in similar_word_count:
                similar_word_count[word] += 1
                contains_similar = True
        
        # Add the scanned song to the list of scanned songs
        scanned_songs_list.append({
            'song': row['song'],
            'contains_similar': contains_similar,
            'similar_word_counts': similar_word_count
        })
    return scanned_songs_list

def calculate_similar_stats(df):
    true_count = df['contains_similar'].sum()    # Count the number of True values in the 'contains_similar' column, to get the amount of "similar" songs.
    false_count = len(df) - true_count    # get the amount of "non-similar" songs by subtracting the amount of similar songs from teh total songs.
    total_count = len(df)    #get the total amount of songs by simply getting the length of the dataframe
    true_percentage = round((true_count / total_count) * 100, 2)    #calculate percentage of similar songs
    return true_count, false_count, total_count, true_percentage

def main():
    scanned_songs_df = pd.DataFrame(scan_songs(filtered_df))

    true_count, false_count, total_count, true_percentage = calculate_similar_stats(scanned_songs_df)
    
    #printing stats about the song
    print(f"""
You searched for songs by: {args.artist}
Which contained words similar to: {args.word}
Of the {total_count} total songs by {args.artist}:
    {true_count} songs contained words similar to {args.word}
    {false_count} songs did not contain words similar to {args.word}
    This means {true_percentage}% of {args.artist} songs contains words similar to {args.word}""")
    
    #Saving the scanned songs dataframe to a csv, if the user specified that they want that
    if args.save:
        out_filename = f'{args.artist} songs about {args.word}.csv'
        print(f'results saved in "/out" folder, as: "{out_filename}"')
        scanned_songs_df.to_csv(os.path.join(out_path, out_filename))

if __name__ == '__main__':
    main()
