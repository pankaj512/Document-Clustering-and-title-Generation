# This file access each document in each category and
# make a preprocessed text file which contain all the term each document have.
import pandas as pd


def make_vector(needStopword):

    labels = []
    stories = []

    if needStopword=='Yes':
        file_name = 'data/input_withStop.xlsx'
    else:
        file_name = 'data/input_withoutStop.xlsx'

    news_data_frame = pd.read_excel(io=file_name, sheetname='sheet 1')
    labels = news_data_frame['Label'].tolist()
    stories = news_data_frame['News'].tolist()

    return stories, labels
