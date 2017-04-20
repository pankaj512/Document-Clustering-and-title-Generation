# -*- coding: utf-8 -*-
import nltk
import os
import pickle
import sys
import re
from sklearn.feature_extraction.text import TfidfVectorizer

TFIDF_LOCATION = '../model/tfidf.pickle'    #this file is genetrated here

# TODO need fixing

def process_input_directory(input_directory):
    all_text = []
    for file_name in os.listdir(input_directory):
        file_path = os.path.join(input_directory, file_name)
        try:
            with open(file_path,'r') as file:
                lines = file.read()
                all_text.append(lines)
        except:
            print("Error in Read file")
    return all_text

def generate_tf_idf_values(all_text):
    """
        Generate the tfidf values and store it in file.
    """
    global TFIDF_LOCATION
    tfidf = TfidfVectorizer(stop_words='english', smooth_idf=True, encoding='utf-8')
    response = tfidf.fit_transform(all_text)
    feature_names = tfidf.get_feature_names()
    with open(TFIDF_LOCATION,'w') as out_file:
        for col in response.nonzero()[1]:
            out_file.write('%s %s\n' %( feature_names[col], response[0, col]))

if __name__ == '__main__':
    path= 'C:/Users/Pankaj Kumar/Desktop/Project/major/major_project/data/segmented/'
    all_text = process_input_directory(path)
    print('Got all data')
    generate_tf_idf_values(all_text)
