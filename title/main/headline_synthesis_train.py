import codecs
import os
import pickle
import sys

import nltk
from nltk.classify import maxent
from title.main.content_selection_classify import *
from title.main.featureFunctions.headline_model_features import get_headline_synthesis_features
from title.main.featureFunctions.BLEU_comparison import get_bleu_score
from title.main.featureFunctions.generate_language_model_features import get_feature_values

headline_feature_set = []
headline_classifier = None


def get_bleu_score_probability(file_location):
    """For the passed input file, returns the bleu score of the headline with reference to the text.

    """
    with open(file_location, 'r') as file:
        all_lines = file.readlines()
        actual_headline = all_lines[0]
        all_lines = all_lines[1:]
        bleu_score = get_bleu_score(actual_headline, all_lines)
        return bleu_score


def process_directory(input_directory):
    """Processes the entire directory passed as input to generate the feature values.

    """
    global headline_feature_set
    all_headlines = []
    dict_content_score = {}
    dict_bleu = {}
    error_file = open('Error/headline_error.txt', 'w')
    for file_name in os.listdir(input_directory):
        try:
            file_path = os.path.join(input_directory, file_name)
            headline, word_dict = classify_dev_file(file_path)

            content_score = 0
            for word in headline.split():
                # todo: recheck this, what if word is present in headline but not in text?
                content_score += word_dict.get(word, 0)

            if content_score in dict_content_score:
                dict_content_score[content_score] += 1
            else:
                dict_content_score[content_score] = 1

            # get bleu score
            bleu_score = get_bleu_score_probability(file_path)
            if bleu_score in dict_bleu:
                dict_bleu[bleu_score] += 1
            else:
                dict_bleu[bleu_score] = 1

            all_headlines.append(headline)
        except:
            error_file.write('filename : %s\n' % file_name)
            import traceback
            error_file.write(traceback.format_exc())
            error_file.write('\n')
            continue
    error_file.close()

    headline_feature_set = get_feature_values(all_headlines)

    for (score, count) in dict_content_score.items():
        output_dict = {'content_score': score}
        outcome = float(count) / len(dict_content_score)
        headline_feature_set.append((output_dict, outcome))

    for (score, count) in dict_bleu.items():
        output_dict = {'bleu_score': score}
        outcome = float(count) / len(dict_content_score)
        headline_feature_set.append((output_dict, outcome))

    import json
    file = open('temp/sequence.txt', 'w')  # this file is missing --resolved
    for entry in headline_feature_set:
        file.write(json.dumps(entry))
        file.write('\n')
    file.close()


def train():
    """Trains the model using the feature set generated above.

    """
    global headline_classifier, headline_feature_set
    headline_classifier = maxent.MaxentClassifier.train(headline_feature_set,max_iter=10)


def save():
    """Saves the model so that it can be used without re-running the training part again.

    """
    global headline_classifier
    out_file = open('model/headline_synthesis.pickle', 'wb')
    pickle.dump(headline_classifier, out_file)
    out_file.close()


if __name__ == '__main__':
    initialise()  # content_selection_classify.
    base = os.path.abspath("../../")
    path = base+'/data/out_pos_tagged/'
    process_directory(path)
    train()
    save()
