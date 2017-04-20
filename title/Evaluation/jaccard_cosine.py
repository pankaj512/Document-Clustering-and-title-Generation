# -*- coding: utf-8 -*-
import re, math
from collections import Counter

WORD = re.compile(r'\w+')
generated_headline=""
actual_headline=""

#TODO
#unknown function till now
def jaccard(actual_headline,generated_headline):
    """ This where juccard fucntionality will happen"""
    x = actual_headline.split(" ")
    y= generated_headline.split(" ")
    intersection_cardinality = len(set.intersection(*[set(generated_headline), set(y)]))
    union_cardinality = len(set.union(*[set(x), set(y)]))
    return intersection_cardinality/float(union_cardinality)


def get_cosine(actual_headline, generated_headline):
    """ this is cosine functionality without a term frequency"""
    vec1 = text_to_vector(generated_headline)
    vec2 = text_to_vector(actual_headline)
    intersection = set(vec1.keys()) & set(vec2.keys())
    numerator = sum([vec1[x] * vec2[x] for x in intersection])

    sum1 = sum([vec1[x]**2 for x in vec1.keys()])
    sum2 = sum([vec2[x]**2 for x in vec2.keys()])
    denominator = math.sqrt(sum1) * math.sqrt(sum2)

    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

#counter will create dictionary of word with their frequency
# a dictionary is returned
def text_to_vector(text):
     words = WORD.findall(text)
     return Counter(words)

if __name__=="__main__":