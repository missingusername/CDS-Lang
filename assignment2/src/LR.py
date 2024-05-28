# system tools
import os

# data munging tools
import pandas as pd

# Machine learning stuff
from sklearn.model_selection import train_test_split
from joblib import dump, load

from sklearn.linear_model import LogisticRegression
from sklearn import metrics

# Setting working directory
# Get the directory where the script is located
script_directory = os.path.dirname(os.path.realpath(__file__))
# Change the current working directory to the directory of the script
os.chdir(script_directory)

# Load the vectorized data
vectorized_data_path = os.path.join('..', 'models', 'tfidf_vectorizer.joblib')
vectorizer = load(vectorized_data_path)

# Load the dataset
data_path = os.path.join('..', 'in', 'fake_or_real_news.csv')
data = pd.read_csv(data_path)

# Setting the feature set (what we train on)
X = data['text']
# Setting the target variable (what we want to predict based on X)
y = data['label']

#splitting the data in the same way as in the vectorizer script, using same seed for consistency.
X_train, X_test, y_train, y_test = train_test_split(X,           # texts for the model
                                                    y,          # classification labels
                                                    test_size=0.2,   # create an 80/20 split
                                                    random_state=42) # random state for reproducibility

# Transforming the text data into features using the loaded vectorizer
X_train_feats = vectorizer.transform(X_train)
X_test_feats = vectorizer.transform(X_test)

# Train the logistic regression classifier
classifier = LogisticRegression(random_state=42).fit(X_train_feats, y_train)

# Predicting labels for the test set
y_pred = classifier.predict(X_test_feats)

# Evaluating the classifier
classifier_metrics = metrics.classification_report(y_test, y_pred)

models_path = os.path.join('..',
                           'models')

out_path = os.path.join('..',
                         'out')

metric_report_file = 'LR_metrics.txt'

def main():
    print(classifier_metrics)

    #Saving the classifier
    dump(classifier, f'{models_path}/LR_classifier.joblib')

    # Open the file in write mode and save the report
    with open(os.path.join(out_path, metric_report_file), 'w') as file:
        file.write(classifier_metrics)

if __name__ == "__main__":
    main()
