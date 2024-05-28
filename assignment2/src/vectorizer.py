# system tools
import os

# data munging tools
import pandas as pd

# Machine learning stuff
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from joblib import dump

# Setting working directory
# Get the directory where the script is located
script_directory = os.path.dirname(os.path.realpath(__file__))
# Change the current working directory to the directory of the script
os.chdir(script_directory)

file_name = 'fake_or_real_news.csv'

data_path = os.path.join('..',
                         'in',
                         file_name)

data = pd.read_csv(data_path)

#setting the feature set (what we train on)
X = data['text']
#setting the target varaible (what we want to predict based on X)
y = data['label']

#splitting the data in an 80/20 split. Also using a set seed for consistency.
X_train, X_test, y_train, y_test = train_test_split(X,           # texts for the model
                                                    y,          # classification labels
                                                    test_size=0.2,   # create an 80/20 split
                                                    random_state=42) # random state for reproducibility


vectorizer = TfidfVectorizer(ngram_range = (1,2),     # unigrams and bigrams (1 word and 2 word units)
                             lowercase =  True,       # why use lowercase?
                             max_df = 0.95,           # remove very common words
                             min_df = 0.05,           # remove very rare words
                             max_features = 100)      # keep only top 100 features

# first we fit to the training data...
X_train_feats = vectorizer.fit_transform(X_train)

#... then do it for our test data
X_test_feats = vectorizer.transform(X_test)

# get feature names
feature_names = vectorizer.get_feature_names_out()

models_path = os.path.join('..',
                           'models')

def main():
    dump(vectorizer, f'{models_path}/tfidf_vectorizer.joblib')

if __name__ == "__main__":
    main()
