import os
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from joblib import dump
from codecarbon import EmissionsTracker

def set_working_directory():
    """Sets the working directory to the directory of the script."""
    script_directory = os.path.dirname(os.path.realpath(__file__))
    os.chdir(script_directory)

def load_data(file_name):
    """Loads data from a CSV file."""
    data_path = os.path.join('..', 'in', file_name)
    return pd.read_csv(data_path)

def preprocess_data(data):
    """Prepares feature set and target variable for machine learning."""
    X = data['text']
    y = data['label']
    return train_test_split(X, y, test_size=0.2, random_state=42)

def create_vectorizer():
    """Creates and configures a TfidfVectorizer."""
    return TfidfVectorizer(
        ngram_range=(1, 2),
        lowercase=True,
        max_df=0.95,
        min_df=0.05,
        max_features=100
    )

def fit_transform_vectorizer(vectorizer, X_train, X_test):
    """Fits the vectorizer to training data and transforms both training and test data."""
    X_train_feats = vectorizer.fit_transform(X_train)
    X_test_feats = vectorizer.transform(X_test)
    return X_train_feats, X_test_feats

def ensure_directory_exists(path):
    """Ensures that the directory exists, creates it if it does not."""
    if not os.path.exists(path):
        os.makedirs(path)

def save_vectorizer(vectorizer, path):
    """Saves the trained vectorizer to the specified path."""
    dump(vectorizer, os.path.join(path, 'tfidf_vectorizer.joblib'))

def main():
    set_working_directory()

    out_path = os.path.join('..', 'out')

    models_path = os.path.join(out_path, 'models')
    ensure_directory_exists(models_path)

    emissions_path = os.path.join(out_path, 'emissions')
    ensure_directory_exists(emissions_path)

    # Initialize CodeCarbon tracker
    tracker = EmissionsTracker(
        project_name="Data vectorization",
        experiment_id="Data_vectorizer",
        output_dir=emissions_path,
        output_file="Text_classification.csv"
    )
    
    tracker.start()

    file_name = 'fake_or_real_news.csv'
    data = load_data(file_name)
    
    X_train, X_test, y_train, y_test = preprocess_data(data)
    
    vectorizer = create_vectorizer()
    
    X_train_feats, X_test_feats = fit_transform_vectorizer(vectorizer, X_train, X_test)
    
    save_vectorizer(vectorizer, models_path)

    tracker.stop()

if __name__ == "__main__":
    main()
