# -*- coding: utf-8 -*
import numpy as np

'''
Added a parser file which loops over all the files in a directory and generates similarity scores

'''


def evaluation_cosine(s1, s2):
    '''
    Returns cosine and tf idf evaluation for two given sentences
    '''
    words = {}
    i = 0

    # loop through each list, find distinct words and map them to a
    # unique number starting at zero

    for word in s1:
        if word not in words:
            words[word] = i
            i += 1

    for word in s2:
        if word not in words:
            words[word] = i
            i += 1

    # create a numpy array (vector) for each input list, filled with zeros
    word_list = list(words.keys())
    a = np.zeros(len(word_list))
    b = np.zeros(len(word_list))

    # loop through each list and create a corresponding vector for it
    # this vector counts occurrences of each word in the dictionary
    for word in s1:
        index = words[word]
        a[index] += 1

    for word in s2:
        index = words[word]
        b[index] += 1

    # use numpy's dot product to calculate the cosine similarity
    sim = np.dot(a, b) / np.sqrt(np.dot(a, a) * np.dot(b, b))
    # print "cosine value is "+str(sim)
    return sim  # similarity score of to title


def evaluate_headline(actual, generated):
    cosine = 0.0
    max_cosine = 0.0
    max_cosine_file = 0
    max_cosine = 0
    for i in range(len(generated)):
        current = generated[i]
        cosine = evaluation_cosine(actual, current)
        if max_cosine < cosine:
            max_cosine = cosine
            max_cosine_file = i
    return max_cosine_file, max_cosine


# main
if __name__ == '__main__':
    path = ""  # path to title directory
    evaluate_headline()
    print(cosine_list)
    # sorted_names = sorted(cosine_list.iteritems(), key=lambda (k,v): (-v, k))[:50]
    # print(sorted_names)
