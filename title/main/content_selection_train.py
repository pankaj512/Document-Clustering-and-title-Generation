import math
import os
import pickle
import sys

from title.main.featureFunctions.features import get_feature_dict, is_word_in_title
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
        a dictionary is created where key= word and value= tf-idf score
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
    first_range_boundary = all_values[int(math.floor(0.9*length))]  # lowest 90% score
    second_range_boundary = all_values[int(math.floor(0.1*length))] # lowest 10% score

    for (key, value) in word_dict.items():
        if value >= first_range_boundary:
            word_dict[key] = '1_10'  # in 10% lowest score range
        elif value >= second_range_boundary:
            word_dict[key] = '10_90' # in 10-90% score range
        else:
            word_dict[key] = '90_100' # in top 10% score range
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
        """
        file_level_dict is a dictionary containing information about the position of word in the file like
        1. is first sentence word
        2. in what range it is occurring (top 10%, 10-90%, last 10%)
        """
        word_score_dict = get_tfidf_score(all_lines)
        """
        word_dict is a dictionary containing information about  in which range score(tf-idf) of word lies
        1. lowest 10%
        2. between 10-90%
        3. top 10%
        """
    return file_level_dict, word_score_dict


def process_sentence(sentence, actual_title, file_level_dict, word_dict):
    """
    For the sentence passed, generates the feature sets for all the words present in the sentence.
    The generated feature set is used to train the model.
    """
    global feature_set, stop_word_list
    if len(sentence)<=0:
        return
    words = sentence.strip().split()
    for index in range(0, len(words)):
        """
        consider total five word 2 before the index, 1 index itself, 2 after the index (except corner cases)
        """
        start_index, end_index = get_start_end_indices(index, len(words))
        outcome = is_word_in_title(words[index], actual_title)
        """
         outcome is 1 or zero based on if word present in title or not
        """
        feature_dict = get_feature_dict(words[start_index: end_index],file_level_dict,word_dict,index-start_index)
        """
         feature_dict is dictionary with all the features to be used
        """
        # stop word feature
        word = words[index].rsplit('/', 1)[0]
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
                """
                file_level_dict contain info about the position of word in file 10% 10-90% 90-100%
                word_dict contain info about in which range each word's if-idf score lies lower 10% 10-90% top 10%
                """
                with open(file_path, 'r',) as file:
                    sentences = file.readlines()
                    actual_title = sentences[0]   # actual title
                    sentences = sentences[1:] # story of news
                    for sentence in sentences:
                        process_sentence(sentence, actual_title, file_level_dict, word_dict)
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
