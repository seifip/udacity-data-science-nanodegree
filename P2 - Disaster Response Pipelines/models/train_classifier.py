import sys
import numpy as mp
import pandas as pd
from sqlalchemy import create_engine
import re
import joblib

import nltk
nltk.download(['punkt', 'stopwords', 'wordnet'])

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import WordNetLemmatizer

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
from sklearn.model_selection import train_test_split, RandomizedSearchCV
from sklearn.pipeline import Pipeline
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

def load_data(database_filepath):
    """Loads dataset, returns X, y, and category names.

    Args:
        database_filepath (str): Path to the sqlite database.

    Returns:
        X (pandas dataframe): Feature data (disaster messages).
        y (pandas dataframe): Classification labels (category).
        category_names (list): Category names for classification.
    """

    engine = create_engine(f'sqlite:///{database_filepath}')
    df = pd.read_sql_query('SELECT * FROM messages', engine)
    X = df.loc[:, 'message']
    y = df.loc[:, 'related':'direct_report']
    category_names = [*y]
    return X, y, category_names

def tokenize(text):
    """Cleans, normalizes and tokenizes text.

    Args:
        text (str): Text.

    Returns:
        tokens (list): String tokens.
    """

    # replace URLs with placeholders
    url_regex = 'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
    detected_urls = re.findall(url_regex, text)
    for url in detected_urls:
        text = text.replace(url, "urlplaceholder")

    # normalize case and remove punctuation
    text = re.sub(r"[^a-zA-Z0-9]", " ", text.lower())

    # tokenize text
    tokens = word_tokenize(text)

    # lemmatize and remove stop words
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    tokens = [lemmatizer.lemmatize(word).strip() for word in tokens if word not in stop_words]

    return tokens


def build_model():
    """Builds a GridSearchCV model.

    Args:
        None

    Returns:
        cv (scikit-learn GridSearchCV): Grid Search model.
    """

    pipeline = Pipeline([
        ('vect', CountVectorizer(tokenizer=tokenize)),
        ('tfidf', TfidfTransformer()),
        ('clf', MultiOutputClassifier(RandomForestClassifier())),
    ])

    # randomized search parameters
    parameters_dist = {
        'clf__estimator__n_estimators': [50, 75, 100],
        #'clf__estimator__learning_rate': [0.5, 1.0, 1.5],
    }

    cv = RandomizedSearchCV(pipeline, param_distributions=parameters_dist, n_iter=20, verbose=10)

    return cv


def evaluate_model(model, X_test, y_test, category_names):
    """Prints multi-output classification results.

    Args:
        model (pandas dataframe): Fitted model.
        X_test (pandas dataframe): Test feature data (disaster messages).
        y_test (pandas dataframe): Test labels (categories).
        category_names (list): Category names.

    Returns:
        None
    """

    # generate predictions
    y_pred = model.predict(X_test)

    # print average accuracy
    accuracy_avg = (y_pred == y_test).mean().mean()
    print('\n\nAverage accuracy {0:.2f}%'.format(accuracy_avg*100))

    # print classification reports and accuracy scores
    y_pred_df = pd.DataFrame(y_pred, columns=category_names)
    for column in category_names:
        print('\n\n{} '.format(column).ljust(55, '-').upper())
        print('{0:.2f}% ACC.'.format(accuracy_score(y_test[column], y_pred_df[column])*100).ljust(53, '-'))
        print(classification_report(y_test[column], y_pred_df[column]))


def save_model(model, model_filepath):
    """Saves model pickle.

    Args:
        model (scikit-learn model): Fitted model.
        model_filepath (str): File path to save to.

    Returns:
        None
    """

    joblib.dump(model.best_estimator_, model_filepath)


def main():
    if len(sys.argv) == 3:
        database_filepath, model_filepath = sys.argv[1:]
        print('Loading data...\n    DATABASE: {}'.format(database_filepath))
        X, y, category_names = load_data(database_filepath)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

        print('Building model...')
        model = build_model()

        print('Training model...')
        model.fit(X_train, y_train)

        print('Evaluating model...')
        evaluate_model(model, X_test, y_test, category_names)

        print('Saving model...\n    MODEL: {}'.format(model_filepath))
        save_model(model, model_filepath)

        print('Trained model saved!')

    else:
        print('Please provide the filepath of the disaster messages database '\
              'as the first argument and the filepath of the pickle file to '\
              'save the model to as the second argument. \n\nExample: python '\
              'train_classifier.py ../data/DisasterResponse.db classifier.pkl')


if __name__ == '__main__':
    main()