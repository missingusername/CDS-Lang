import os
from collections import Counter
import warnings
import re

import spacy
import pandas as pd
from tqdm import tqdm

warnings.simplefilter(action='ignore', category=FutureWarning)

nlp = spacy.load("en_core_web_md")

# Get the directory where the script is located
script_directory = os.path.dirname(os.path.realpath(__file__))
# Change the current working directory to the directory of the script
os.chdir(script_directory)

input_directory = ('../in/USEcorpus')
output_directory = os.path.join('..','out')

def process_folder(folderpath, nlp):
    #Process all text files in a folder.
    rows = []
    for file in tqdm(os.listdir(folderpath)):
        filename = file
        filepath = os.path.join(folderpath, filename)
        info = process_file(filepath, nlp)
        row = {'Filename': filename, 'RelFreq NOUN': info[0], 'RelFreq VERB': info[1],
               'RelFreq ADJ': info[2], 'RelFreq ADV': info[3], 'Unique PER': info[4],
               'Unique LOC': info[5], 'Unique ORG': info[6]}
        rows.append(row)
    df = pd.DataFrame(rows)
    return df

def process_file(filepath, nlp):
    #Process a single text file.
    #i use latin1 / ISO-8859-1 because the text is encoded with swedish characters
    with open(filepath, encoding='latin1') as f:
        text = f.read()

    #cleaning the text by removing anything between '<' and '>'
    cleaned_text = re.sub(r'<[^>]+>', '', text)

    doc = nlp(cleaned_text)
    return extract_information(doc)

def extract_information(doc):
    #Extract linguistic information and entity counts
    pos_counts = Counter(token.pos_ for token in doc)
    num_words = sum(1 for token in doc if not token.is_punct)
    
    noun_freq = calculate_frequency(pos_counts['NOUN'], num_words)
    verb_freq = calculate_frequency(pos_counts['VERB'], num_words)
    adj_freq = calculate_frequency(pos_counts['ADJ'], num_words)
    adv_freq = calculate_frequency(pos_counts['ADV'], num_words)

    ent_per = set()
    ent_loc = set()
    ent_org = set()

    for entity in doc.ents:
        if entity.label_ == 'PERSON':
            ent_per.add(str(entity))
        elif entity.label_ == 'LOC':
            ent_loc.add(str(entity))
        elif entity.label_ == 'ORG':
            ent_org.add(str(entity))

    return noun_freq, verb_freq, adj_freq, adv_freq, len(ent_per), len(ent_loc), len(ent_org)

def calculate_frequency(pos_counts, num_words, frequency_check=10000):
    #Calculate relative frequency of a part-of-speech tag per 10,000 words
    frequency = round(pos_counts / num_words * frequency_check, 2)
    return frequency

def main():
    print("Current working directory:", os.getcwd())
    for folder in os.listdir(input_directory):
        folderpath = os.path.join(input_directory, folder)
        print(f'Processing folder: {folder}')
        df = process_folder(folderpath, nlp)
        df.to_csv(os.path.join(output_directory, f'{folder} table.csv'), index=False)

if __name__ == "__main__":
    main()