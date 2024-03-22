
# CDS Language Analytics: Assignment #3 - Query expansion with word embeddings

## Description
This script utilizes word embeddings to find out how many songs by a given artist contain words similar to a given search word.

## Setup

1. Make sure to have python and Git Bash installed!

2. Open a Git Bash terminal and use Git to download the repository:
```sh
git  clone  https://github.com/missingusername/cds-lang-git.git
```
3. Navigate to the project folder for this assignment:
```sh
cd  cds-lang-git/assignments/assignment3
```
4. Before running the program, you first have to set up a virtual environment with the required dependencies. This can be done by simply running either  `bash win_setup.sh`  or  `bash unix_setup.sh`  depending on your system.

5. Before we can run the script, we first need the song data. The data can be found [here](https://www.kaggle.com/datasets/joebeachcapital/57651-spotify-songs?resource=download), where you can download an `archive.zip` file. When downloaded, unzip the folder and place `Spotify Million Song Dataset_exported.csv` in the `/in` folder of the `assignment3` directory.

6. The script uses Argparse to parse commands to the script from the command line.

| name | flag | description | required |
|--|--|--|--|
| artist | -a | What artist to search for | *REQUIRED |
| word | -w | What word to search for similar words for | *REQUIRED |
| save | -s | whether to save a .csv file of the gathered data | OPTIONAL |

To run the program, you can run the appropriate run script, again depending on your system. Here's an example of how to run the script with arguments:
```sh
./win_run.sh -a metallica -w god -s
```
or
```sh
./unix_run.sh -a abba -w love -s
```
If the script is denied permission, you can try running `chmod +x *`, which will grant execution privileges to the scripts in the current directory. Then try running the script again.

## The Code
The code works by first turning the data into a pandas dataframe, and filters it such that only songs by the specified artist remains.
We use gensim to load the model `glove-wiki-gigaword-50`, which is trained on 2B tweets (27B tokens, 1.2M vocabulary)
Then we generate a list of the 10 most simliar words to the search word, using gensim "most_similar", as well as the search word itself.
Then, we simply go through every song by that artist, checking if any of the similar words appear in the songs text. We keep track of this in a dictionary, w´counting how many times each of the similar words occurs.
This all gets converted to its own dataframe, where we keep track of the song, if it it contained any of the similar words, and how many times each similar word appeared in the text.
This is the dataframe that you can optionally have saved to the `/out` folder *(some output examples can also be found there)*.
Lastly, you get some stats about the data printed to the terminal, telling you how many of the songs featured similar words.
