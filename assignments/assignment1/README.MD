# CDS Language Analytics: Assignment #1

## Setup
1. Make sure to have python and Git Bash installed!

2. Open a Git Bash terminal and use Git to download the repository:

```sh
git clone https://github.com/missingusername/cds-lang-git.git
```

3. Navigate to the project folder for this assignment:

```sh
cd assignments
cd assignment1
```

4. Before running the program make sure you have Spacy, Pandas, and TQDM installed. This can be done by simply running the ```setup.sh``` script from inside the ```assignment1``` folder, again using Git Bash:

```sh
./setup.sh
```

5. Before we can run the script, we first need to get the actual data. The data corpus can be found [here](https://ota.bodleian.ox.ac.uk/repository/xmlui/handle/20.500.12024/2457), where you can download the ```USEcorpus.zip``` file. When downloaded, unzip the folder and place "USEcorpus" in the ```in``` folder of the assignment1 directoy.

6. To finally execute the file, simply run the script in the same Git Bash terminal:

```sh
python src/assignment1.py
```

## The Code
The script utilizes the SpaCy library to tokenize and analyze the text, extracting part-of-speech tags and named entities. It iterates over each text file in each subfolder of the input directory, cleans the text by removing metadata and , and then calculates the relative frequency of nouns, verbs, adjectives, and adverbs per 10,000 words (I use spacy to not count punctuation as words, which would impact the relative frequency of the POS tags).

Additionally, it counts the total number of unique entities (persons, locations, and organizations) mentioned in each text. The extracted information is handled using pandas dataframes and is saved in CSV format, with each sub-folder corresponding to a separate CSV file containing a table with filenames and their extracted linguistic and entity information. The code is modularized for maintainability and efficiency, with functions to process individual files and entire folders, allowing for easy scalability and customization.

TQDM is used for showing the scripts progress in its processing of each folder, and is mostly included for eye candy.
