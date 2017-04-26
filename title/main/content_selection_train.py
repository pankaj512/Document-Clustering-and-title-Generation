import math
import os
import pickle
import sys

from title.main.featureFunctions.features import get_feature_dict, get_outcome
from title.main.featureFunctions.file_level_features import get_word_range
from nltk.classify import maxent
from nltk.corpus import stopwords
from title.main.Utils import get_start_end_indices

feature_set = []
classifier = None
tfidf_dict = {}
stop_word_list = stopwords.words('english')

TFIDF_LOCATION = 'model/tfidf.pickle'    # this file is missing -- resolved



def initialise():
    """Initialises the globally declared variables.

    These variables are used throughout the file.
    """
    global tfidf_dict
    file = open(TFIDF_LOCATION, 'r')
    for line in file:
        parts = line.strip().split(' ')
        if len(parts)>=2:
            tfidf_dict[parts[0]] = parts[1]
    return

def get_tfidf_score(all_lines):
    """
    For an entire file text, returns a dictionary mapping word to range of tf-idf values it belongs to.
    This information is used as a part of feature function.
    """
    global tfidf_dict

    word_dict = {}

    for line in all_lines:
        word_list = line.strip().split()
        for word in word_list:
            word = word.rsplit('/', 1)[0]
            if word in tfidf_dict:
                word_dict[word] = tfidf_dict.get(word)
    all_values = list(word_dict.values())
    all_values.sort()

    length = len(all_values) - 1
    first_range_boundary = all_values[int(math.floor(0.9*length))]
    second_range_boundary = all_values[int(math.floor(0.1*length))]

    for (key, value) in word_dict.items():
        if value >= first_range_boundary:
            word_dict[key] = '1_10'
        elif value >= second_range_boundary:
            word_dict[key] = '10_90'
        else:
            word_dict[key] = '90_100'
    return word_dict


def get_file_level_details(file_path):
    """
    Returns file level feature functions details.
    These are used as a part of the feature functions for querying the models.
    """
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()
        all_lines = lines[1:]
        file_level_dict = get_word_range(all_lines)
        word_dict = get_tfidf_score(all_lines)
    return file_level_dict, word_dict


def process_sentence(sentence, headline, file_level_dict, word_dict):
    """
    For the sentence passed, generates the feature sets for all the words present in the sentence.
    The generated feature set is used to train the model.
    """
    global feature_set, stop_word_list
    if len(sentence)<=0:
        return
    words = sentence.strip().split()
    for index in range(0, len(words)):
        start_index, end_index = get_start_end_indices(index, len(words))
        outcome = get_outcome(words[index], headline)
        feature_dict = get_feature_dict(words[start_index: end_index], index-start_index)

        # additional fields
        word = words[index].rsplit('/', 1)[0]
        feature_dict['tfidf'] = word_dict.get(word, '90_100')

        feature_dict['lead_sentence'] = file_level_dict[word]['lead_sentence']
        feature_dict['first_occurance'] = file_level_dict[word]['first_occurance']
        feature_dict['range'] = ','.join(str(x) for x in file_level_dict[word]['range'])

        feature_dict['stop_word'] = 1 if word in stop_word_list else 0
        # add this to set of all features
        feature_set.append((feature_dict, outcome))
    return


def process_input_directory(directory):
    """
    Processes the entire directory passed as input to generate the feature values.
    """
    count = 0

    with open('Error/error_content_selection.txt', 'w') as error:
        for file_name in os.listdir(directory):
            count += 1
            try:
                file_path = os.path.join(directory, file_name)
                file_level_dict, word_dict = get_file_level_details(file_path)

                with open(file_path, 'r',) as file:
                    sentences = file.readlines()
                    headline = sentences[0]
                    sentences = sentences[1:]
                    for sentence in sentences:
                        process_sentence(sentence, headline, file_level_dict, word_dict)
            except:
                error.write('filename : %s\n' % file_name)
                import traceback
                error.write(traceback.format_exc())
                error.write('\n')
                continue
    return

def train_model():
    """Trains the model using the feature set generated above.

    """
    global classifier, feature_set
    #print(feature_set)
    classifier = maxent.MaxentClassifier.train(feature_set,max_iter=10)
    #classifier = MaxentClassifier.train(feature_set, "megam")


def save_classifier():
    """Saves the model so that it can be used without re-running the training part again.

    """
    global classifier
    out_file = open('model/content_selection.pickle', 'wb')  # this file should be created
    pickle.dump(classifier, out_file)
    out_file.close()


if __name__ == '__main__':
    initialise()
    base = os.path.abspath("../../")
    path= base +'/data/out_pos_tagged/'
    process_input_directory(path)
    train_model()
    save_classifier()
