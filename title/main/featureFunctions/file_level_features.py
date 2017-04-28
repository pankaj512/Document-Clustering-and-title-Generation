# -*- coding: utf-8 -*-
# define all the feature functions here
""""
This file is about the location of words in the file
1. is word in first sentence
2. in what range a word occurred in this file
"""
import math


def cal_totalwords(lines):
    word_list = []
    dict_probs = {}

    for line in lines:
        val = line.strip()
        wordtags = val.split()  # word-pos-tag
        for entry in wordtags:
            parts = entry.rsplit('/', 1)
            if len(parts) >= 2:
                word, tag = parts[0], parts[1]
                word_list.append(word)

    total_len = len(word_list)
    first_range = math.floor((0.1) * total_len)
    second_range = math.floor((0.9) * total_len)

    dict_probs['total_len'] = total_len
    dict_probs['first_range'] = first_range
    dict_probs['second_range'] = second_range
    return dict_probs

    """
    this return dictionary contain "number of total word" "first 10%" "first 90%"
    """


# calculate the word range for the file
def get_word_range(lines):
    """
    Return the dict contain the lead position of the words in the file i.e if the word is present in the first sentence or not
    """
    position_parameters = {}
    total_length = cal_totalwords(lines)
    # total_length is  a dictionary with " % of words in total 10% 90% " use it to find in which range word exist

    # if the first sentence is encountered add lead position value to one for that particular word
    firstSentence = 1
    current_count = 0

    for line in lines:
        line = line.strip()
        if firstSentence == 1:
            wordtags = line.split()  # word-pos-tag
            for entry in wordtags:
                current_count += 1
                parts = entry.rsplit('/', 1)
                if len(parts) >= 2:
                    word, tag = parts[0], parts[1]
                    if word not in position_parameters:
                        position_parameters[word] = {}
                        position_parameters[word]['range'] = []
                        position_parameters[word]['lead_sentence'] = 1  # word present in first sentence
                        position_parameters[word]['first_occurrence'] = current_count  # first position of word
                    # Added the word postion for each token and also added the word rage for given word

                    if current_count <= total_length['first_range']:     # if present in first 10%
                        position_parameters[word]['range'].append('1_10')
                    elif total_length['total_len'] >= current_count >= total_length['second_range']: # if after 90%
                        position_parameters[word]['range'].append('90_100')
                    else:
                        position_parameters[word]['range'].append('10_90')     # if between 10-90%
                        # returns the word position for each word,word index is associated with current count
            firstSentence = 0
        else:
            wordtags = line.split()
            for entry in wordtags:
                current_count += 1
                parts = entry.rsplit('/', 1)
                if len(parts) >= 2:
                    word, tag = parts[0], parts[1]
                    if word not in position_parameters:
                        position_parameters[word] = {}
                        position_parameters[word]['range'] = []
                        position_parameters[word]['lead_sentence'] = 0
                        position_parameters[word]['first_occurrence'] = current_count
                    # Added the word postion for each token and also added the word rage for given word
                    if current_count <= total_length['first_range']:
                        position_parameters[word]['range'].append('1_10')
                    elif total_length['total_len'] >= current_count >= total_length['second_range']:
                        position_parameters[word]['range'].append('90_100')
                    else:
                        position_parameters[word]['range'].append('10_90')
    return position_parameters
    """
    position_parameters is a dictionary containing information about
    1. if word is in first sentence
    2. if which range it is occurring and append every position of this word
    """