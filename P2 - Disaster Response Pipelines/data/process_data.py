import sys
import numpy as np
import pandas as pd
from sqlalchemy import create_engine

def load_data(messages_filepath, categories_filepath):
    """Loads messages and categories datasets, merge into on `id`.

    Args:
        messages_filepath (str): Path to the messages csv.
        categories_filepath (str): Path to the categories csv.

    Returns:
        df (pandas dataframe): Merged dataset.
    """

    messages = pd.read_csv(messages_filepath)
    categories = pd.read_csv(categories_filepath)
    df = messages.merge(categories, on='id')
    return df


def clean_data(df):
    """Cleans dataset.

    Args:
        df (pandas dataframe): Merged dataset.

    Returns:
        df (pandas dataframe): Preprocessed dataset.
    """

    # create a dataframe of the 36 individual category columns
    categories = df['categories'].str.split(pat=';', expand=True)

    # rename category columns
    row = categories.iloc[0]
    category_colnames = row.apply(lambda x: x.split('-')[0])
    categories.columns = category_colnames

    # set each value to be the last character of the string and convert to numeric
    for column in categories:
        categories[column] = categories[column].apply(lambda x: x.split('-')[1])
        categories[column] = pd.to_numeric(categories[column], errors='coerce') 

    # drop the original categories column from `df`
    df.drop(['categories'], axis=1, inplace=True)

    # concat the original dataframe with the new `categories` dataframe
    df = pd.concat([df, categories], axis=1)

    # drop duplicate messages
    df = df.drop_duplicates(subset=['message'])

    # drop `child_alone` category (all messages have the same value)
    df.drop(['child_alone'], axis=1, inplace=True)

    return df


def save_data(df, database_filepath):
    """Saves dataset to a SQLite database.

    Args:
        df (pandas dataframe): Cleaned dataset.
        database_filepath (str): File path to save to.

    Returns:
        None
    """

    engine = create_engine(f'sqlite:///{database_filepath}')
    df.to_sql('messages', engine, index=False)
    pass


def main():
    if len(sys.argv) == 4:

        messages_filepath, categories_filepath, database_filepath = sys.argv[1:]

        print('Loading data...\n    MESSAGES: {}\n    CATEGORIES: {}'
              .format(messages_filepath, categories_filepath))
        df = load_data(messages_filepath, categories_filepath)

        print('Cleaning data...')
        df = clean_data(df)

        print('Saving data...\n    DATABASE: {}'.format(database_filepath))
        save_data(df, database_filepath)

        print('Cleaned data saved to database!')

    else:
        print('Please provide the filepaths of the messages and categories '\
              'datasets as the first and second argument respectively, as '\
              'well as the filepath of the database to save the cleaned data '\
              'to as the third argument. \n\nExample: python process_data.py '\
              'disaster_messages.csv disaster_categories.csv '\
              'DisasterResponse.db')


if __name__ == '__main__':
    main()