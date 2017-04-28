"""
List of features used:
1. Current Story Word
2. Word Bi-gram Context - both sides -1 and +1
3. POS of Current Story Word
4. POS Bi-gram of Current Word - both sides -1 and +1
5. POS Tri-gram of Current Word - both sides -1, -2 and +1, +2
6. Word Position in Lead sentence
7. Word Position
8. First Word Occurrence Position
9. Word TF-IDF Range

"""


def is_word_in_headline(word, heading):
    """
    Returns if the word is present in heading or not.
    """
    word = word.rsplit('/', 1)[0]
    if word in heading:
        return 1
    return 0


def get_feature_dict(word_tag_list, word_position_dict, word_score_dict, index=2):
    """
    Returns the feature dictionary of POS tagged list of words(5 words are passed in the list).
    """
    dict_feature = {}
    word_list = []  # list of all the words from word_tag_list
    tag_list = []  # list of the tags from word_tag_list
    for entry in word_tag_list:
        word, tag = entry.rsplit('/', 1)
        word_list.append(word)
        tag_list.append(tag)

    # 1. Current Story Word
    # 3. POS of Current Story Word
    # key format for feature dictionary = feature number + '_' + type of feature (word/tag)
    dict_feature['1_w'] = word_list[index]
    dict_feature['3_t'] = tag_list[index]

    # 2. Word Bi-gram Context - both sides -1 and +1
    # 4. POS Bi-gram of Current Word - both sides -1 and +1
    if index - 1 >= 0:
        dict_feature['2_w_w-1'] = '%s,%s' % (word_list[index], word_list[index - 1])  # bi-gram of word
        dict_feature['4_t_t-1'] = '%s,%s' % (tag_list[index], tag_list[index - 1])  # bi-gram of tag
    if index + 1 < len(word_list) - 1:
        dict_feature['2_w_w+1'] = '%s,%s' % (word_list[index], word_list[index + 1])
        dict_feature['4_t_t+1'] = '%s,%s' % (tag_list[index], tag_list[index + 1])

    # 5. POS Tri-gram of Current Word - both sides -1, -2 and +1, +2
    if index - 2 >= 0:
        dict_feature['5_t_t-1_t-2'] = '%s,%s,%s' % (tag_list[index], tag_list[index - 1], tag_list[index - 2])
    if index + 2 < len(word_list) - 1:
        dict_feature['5_t_t+1_t+2'] = '%s,%s,%s' % (tag_list[index], tag_list[index + 1], tag_list[index + 2])

    # 6. Word Position in Lead sentence
    dict_feature['6_w'] = word_position_dict[word_list[index]]['lead_sentence']

    # 7. Word Position range
    dict_feature['7_w'] = ','.join(str(x) for x in word_position_dict[word]['range'])

    # 8. First Word Occurrence Position
    dict_feature['8_w'] = word_position_dict[word_list[index]]['first_occurrence']

    # 9. word if-idf range 1 if in top 10% else 0
    dict_feature['9_w'] = word_score_dict.get(word, '90_100')

    return dict_feature
