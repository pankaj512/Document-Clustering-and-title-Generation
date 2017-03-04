# This file access each document in each category and
# make a preprocessed text file which contain all the term each document have.
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer

def make_vector(needStopword):

    labels = []
    stories = []

    if needStopword==True:
        file_name = '../data/input_withStop.xlsx'
    else:
        file_name = '../data/input_withoutStop.xlsx'

    news_data_frame = pd.read_excel(io=file_name, sheetname='Sheet 1')
    labels = news_data_frame['Label'].tolist()
    stories = news_data_frame['News'].tolist()

    output_data_path = '../data/'
    """
        Creates a document corpus list (by stripping out the
        class labels), then applies the TF-IDF transform to this
        list.

        The function returns both the class label vector (y) and
        the corpus token/feature matrix (X).
        """
    # Create the TF-IDF vectoriser and transform the corpus
    vectorizer = TfidfVectorizer(min_df=1)
    stories = vectorizer.fit_transform(stories)
    labels = vectorizer.fit_transform(labels)
    return stories, labels

if __name__=='__main__':