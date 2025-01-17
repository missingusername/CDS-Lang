import os
import pandas as pd
from sklearn.model_selection import train_test_split
from joblib import dump, load
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from codecarbon import EmissionsTracker

def set_working_directory():
    """Sets the working directory to the directory of the script."""
    script_directory = os.path.dirname(os.path.realpath(__file__))
    os.chdir(script_directory)

def preprocess_data(data):
    """Prepares feature set and target variable for machine learning."""
    X = data['text']
    y = data['label']
    return train_test_split(X, y, test_size=0.2, random_state=42)

def transform_data(vectorizer, X_train, X_test):
    """Transforms the text data into features using the vectorizer."""
    X_train_feats = vectorizer.transform(X_train)
    X_test_feats = vectorizer.transform(X_test)
    return X_train_feats, X_test_feats

def train_classifier(X_train_feats, y_train):
    """Trains a logistic regression classifier."""
    return LogisticRegression(random_state=42).fit(X_train_feats, y_train)

def evaluate_classifier(classifier, X_test_feats, y_test):
    """Evaluates the classifier and returns the classification report."""
    y_pred = classifier.predict(X_test_feats)
    return metrics.classification_report(y_test, y_pred)

def save_classifier(classifier, path):
    """Saves the trained classifier to the specified path."""
    dump(classifier, os.path.join(path, 'LR_classifier.joblib'))

def save_metrics(metrics, path):
    """Saves the classifier metrics to a text file."""
    with open(os.path.join(path, 'LR_metrics.txt'), 'w') as file:
        file.write(metrics)

def main():
    set_working_directory()

    in_path = os.path.join('..', 'in')

    out_path = os.path.join('..', 'out')

    models_path = os.path.join(out_path, 'models')

    emissions_path = os.path.join(out_path, 'emissions')

    # Initialize CodeCarbon tracker
    tracker = EmissionsTracker(
        project_name="LR classification",
        experiment_id="LR_classifier",
        output_dir=emissions_path,
        output_file="Text_classification.csv"
    )

    tracker.start_task('load vectorizer')    
    vectorized_data_path = os.path.join(models_path, 'tfidf_vectorizer.joblib')
    vectorizer = load(vectorized_data_path)
    tracker.stop_task()

    tracker.start_task('load data')    
    file_name = 'fake_or_real_news.csv'
    file_path = os.path.join(in_path, file_name)
    data = pd.read_csv(file_path)
    tracker.stop_task()

    tracker.start_task('split data')    
    X_train, X_test, y_train, y_test = preprocess_data(data)
    tracker.stop_task()
    
    tracker.start_task('transform data')        
    X_train_feats, X_test_feats = transform_data(vectorizer, X_train, X_test)
    tracker.stop_task()
    
    tracker.start_task('train LR classifier')    
    classifier = train_classifier(X_train_feats, y_train)
    tracker.stop_task()
    
    tracker.start_task('evaluate LR classifier')
    classifier_metrics = evaluate_classifier(classifier, X_test_feats, y_test)
    tracker.stop_task()
    
    tracker.start_task('save LR classifier')
    save_classifier(classifier, models_path)
    tracker.stop_task()
    
    save_metrics(classifier_metrics, out_path)
    
    print(classifier_metrics)

    tracker.stop()

if __name__ == "__main__":
    main()
