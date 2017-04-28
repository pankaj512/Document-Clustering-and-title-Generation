"""
this file is used for testing (generating title for new input file
"""

import copy
from heapq import heappush, heappop

from title.main.Utils import remove_tags_from_line
from title.main.content_selection_classify import *
from title.main.title_synthesis_classify import *

logger = None
LOG_FILE_LOCATION = 'temp/parse_log.log'  # this file is missing  --resolved


def initialise_all():
    """
    Initialise the content selection and title synthesis models
    """
    global logger
    initialise()  # content_selection_classify.initialise()
    title_synthesis_initialise()  # title_synthesis_classify.initialise()
    logger = open(LOG_FILE_LOCATION, 'w', encoding='utf-8')  # log file never mind


# file path is temp location where only story of file exist
def get_file_headings(file_path, title_length=8):
    """
    Creates the actual headings by parsing the passed file and generating sequences.
    """
    global logger
    top_sentence_list = []   # list of all the sentences those can be title
    with open(file_path, 'r') as file:
        text = file.read()   # read all text from file

    top_25_words = classify_new_file(file_path)
    """
    top_25_words = title for new file generated from these 25 word by re-ordering, creating sequences

    """

    heap, next_heap = [], []
    for word in top_25_words:
        heappush(heap, (0, [word]))
    """
    critical  part: Ahead
    """
    index = 0
    max_length = 25
    while index < max_length:
        if index < 1:
            max_range = 25
        elif index < 3:
            max_range = 3
        else:
            max_range = 2

        index2 = 1
        probability_list = []
        while heap and index2 < max_range:
            prob, word = heappop(heap)
            if prob not in probability_list:
                probability_list.append(prob)

            index2 += 1
            for all_word in top_25_words:
                if all_word not in word:
                    word_copy = copy.deepcopy(word)
                    existing_words = [word1.rsplit('/', 1)[0] for word1 in word_copy]
                    if all_word.rsplit('/', 1)[0] in existing_words:
                        continue
                    word_copy.append(all_word)
                    word_str = ' '.join(word_copy)
                    probab_value = get_title_synthesis_score(word_str, top_25_words, text)
                    logger.write('%s- %s\n' % (word_str, probab_value))
                    heappush(next_heap, (-1 * probab_value, word_copy))
        heap = next_heap
        next_heap = heap
        index += 1
        max_length = title_length  # change title length if needed

    count = 0
    while heap and count < 10:
        count += 1
        probab, sentence = heappop(heap)
        top_sentence_list.append(remove_tags_from_line(sentence))
    print('\t\tReturning Top 10 sentences')
    return top_sentence_list
    """
    top_sentence_list = 10 generated title
    """