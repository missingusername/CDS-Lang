import os
from collections import Counter
import warnings
import re

import spacy
import pandas as pd
from tqdm import tqdm

from codecarbon import EmissionsTracker

warnings.simplefilter(action='ignore', category=FutureWarning)

def set_working_directory():
    """Sets the working directory to the directory of the script."""
    script_directory = os.path.dirname(os.path.realpath(__file__))
    os.chdir(script_directory)

def process_folder(folder_path, nlp):
    '''Process all text files in a folder.'''
    rows = []
    for file in tqdm(sorted(os.listdir(folder_path))):
        filename = file
        filepath = os.path.join(folder_path, filename)
        info = process_file(filepath, nlp)
        row = {'Filename': filename, 'RelFreq NOUN': info[0], 'RelFreq VERB': info[1],
               'RelFreq ADJ': info[2], 'RelFreq ADV': info[3], 'Unique PER': info[4],
               'Unique LOC': info[5], 'Unique ORG': info[6]}
        rows.append(row)
    df = pd.DataFrame(rows)
    return df

def process_file(filepath, nlp):
    '''
    Process a single text file.
    using latin1 / ISO-8859-1 because the text is encoded with swedish characters
    '''
    with open(filepath, encoding='latin1') as f:
        text = f.read()

    #cleaning the text by removing anything between '<' and '>'
    cleaned_text = re.sub(r'<[^>]+>', '', text)

    doc = nlp(cleaned_text)
    return extract_information(doc)

def extract_information(doc):
    '''Extract linguistic information and entity counts'''
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
    '''Calculate relative frequency of a part-of-speech tag per 10,000 words'''
    frequency = round(pos_counts / num_words * frequency_check, 2)
    return frequency

def ensure_directory_exists(path):
    """Ensures that the directory exists, creates it if it does not."""
    if not os.path.exists(path):
        os.makedirs(path)

def main():
    set_working_directory()

    in_path = os.path.join('..','in')
    data_folder = os.path.join(in_path,'USEcorpus')
    out_path = os.path.join('..','out')

    emissions_path = os.path.join(out_path, 'emissions')
    ensure_directory_exists(emissions_path)

    # Initialize CodeCarbon tracker
    tracker = EmissionsTracker(
        project_name="Feature extraction",
        experiment_id="Feature_extractor",
        output_dir=emissions_path,
        output_file="Feature_extraction_emissions.csv"
    )
    tracker.start()

    nlp = spacy.load("en_core_web_md")

    print("Current working directory:", os.getcwd())
    for folder in sorted(os.listdir(data_folder)):
        current_folder_path = os.path.join(data_folder, folder)
        print(f'Processing folder: {folder}')
        df = process_folder(current_folder_path, nlp)
        df.to_csv(os.path.join(out_path, f'{folder} table.csv'), index=False)
        
    tracker.stop()

if __name__ == "__main__":
    main()