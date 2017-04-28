import os

from nltk.classify import maxent

from title.main.content_selection_classify import *
from title.main.featureFunctions.BLEU_comparison import get_bleu_score
from title.main.featureFunctions.generate_language_model_features import get_feature_values

title_feature_set = []
title_classifier = None


def get_bleu_score_probability(file_location):
    """For the passed input file, returns the bleu score of the title with reference to the text.

    """
    with open(file_location, 'r') as file:
        all_lines = file.readlines()
        actual_title = all_lines[0]
        all_lines = all_lines[1:]
        bleu_score = get_bleu_score(actual_title, all_lines)
        return bleu_score
        """
        return value is bleu_score that is how much readable actual title is
        """


def process_directory(input_directory):
    """Processes the entire directory passed as input to generate the feature values.

    """
    global title_feature_set
    all_titles = []
    dict_content_score = {}
    dict_bleu = {}
    error_file = open('Error/title_error.txt', 'w')
    for file_name in os.listdir(input_directory):
        try:
            file_path = os.path.join(input_directory, file_name)
            title, word_dict = classify_dev_file(file_path)
            """
            title : actual title of given file
            word_dict : words can be included in title with max probability
            """
            content_score = 0
            for word in title.split():
                # recheck this, what if word is present in actual title but not in text?
                content_score += word_dict.get(word, 0)  # if in title but not in text then 0 else probability

            if content_score in dict_content_score:
                dict_content_score[content_score] += 1
            else:
                dict_content_score[content_score] = 1

            # get bleu score
            bleu_score = get_bleu_score_probability(file_path)
            """
             bleu score of actual title with respect to given story of news
            """
            if bleu_score in dict_bleu:
                dict_bleu[bleu_score] += 1
            else:
                dict_bleu[bleu_score] = 1

            all_titles.append(title) # list of all the actual titles
        except:
            error_file.write('filename : %s\n' % file_name)
            import traceback
            error_file.write(traceback.format_exc())
            error_file.write('\n')
            continue
    error_file.close()

    title_feature_set = get_feature_values(all_titles)
    """
    title_features_set is a list of all the features extracted from all title
    """

    """
    dict_content_score = dictionary of score of words in title with their frequency of probability values
    """
    for (score, count) in dict_content_score.items():
        output_dict = {'content_score': score}   # content_score with this score
        outcome = float(count) / len(dict_content_score)  # probability of occurrance of that score
        title_feature_set.append((output_dict, outcome)) # add to title feature set

    for (score, count) in dict_bleu.items():
        output_dict = {'bleu_score': score}     # bleu score and its frequency
        outcome = float(count) / len(dict_content_score) # probability of this frequency
        title_feature_set.append((output_dict, outcome)) # add to feature set

    import json
    file = open('temp/sequence.txt', 'w')  # this file is missing --resolved
    for entry in title_feature_set:
        file.write(json.dumps(entry))
        file.write('\n')
    file.close()


def train():
    """Trains the model using the feature set generated above.

    """
    global title_classifier, title_feature_set
    title_classifier = maxent.MaxentClassifier.train(title_feature_set,max_iter=10)


def save():
    """Saves the model so that it can be used without re-running the training part again.

    """
    global title_classifier
    out_file = open('model/title_synthesis.pickle', 'wb')
    pickle.dump(title_classifier, out_file)
    out_file.close()


if __name__ == '__main__':
    initialise()  # content_selection_classify.
    base = os.path.abspath("../../")
    path = base+'/data/out_pos_tagged/'
    process_directory(path)
    train()
    save()
