"""
Features from headline:
added in this file:
1. Pos tri-gram and probability

added in headline-synthesis_train file

3. content score and its probability of occurrence
4. bleu score and its probability of occurrence
"""
import nltk


def increment_key(dict_obj, key):
    if key in dict_obj:
        dict_obj[key] += 1
    else:
        dict_obj[key] = 1


"""
all_sentences = all headline present in training data set
"""


def get_feature_values(all_sentences):
    all_tag_sequence = []
    all_word_sequence = []
    all_feature_list = []
    dict_word = {}

    for sentence in all_sentences:
        sentence = 'start/start %s' % sentence  # append 'start/start' in each headline
        words = sentence.split()  # split each headline into word-tag format
        tag_list = []  # list of all the tag in one headline
        word_list = []  # list of all the word in one headline
        for entry in words:
            word, tag = entry.rsplit('/', 1)
            tag_list.append(tag)
            if word not in ['start']:
                word_list.append(word)
                increment_key(dict_word, word)

        all_tag_sequence.append(tag_list)  # add all the tags into tags list of all headline
        all_word_sequence.append(word_list)  # add all words into words of all the headline

    # all_tag_sequence now has a list of tags corresponding to different sentences

    bigram_pos_list = []  # bi-gram list of all the tags
    trigram_pos_list = []  # tri-gram list of all the tags
    for tag_seq in all_tag_sequence:
        bigram_pos_list.extend(list(nltk.bigrams(tag_seq)))  # generating bi-gram of tag
        trigram_pos_list.extend(list(nltk.trigrams(tag_seq)))  # generating tri-gram of all the tags
    """
    Diffrence between append and extend
    append: a.append([xyz]=  [a,[xyz]]
    extend: a.extend([xyz]) = [a,xyz]
    """
    dict_pos_bigram = {}
    dict_pos_trigram = {}

    for entry in bigram_pos_list:
        increment_key(dict_pos_bigram, entry)
        # if present then increment count else add count 1
        # counting frequency of bi-grams

    for entry in trigram_pos_list:
        increment_key(dict_pos_trigram, entry)
        # if present then increment count else add  count =1
        #  # counting frequency of tri-grams

    for (key, value) in dict_pos_trigram.items():
        prob_val = float(value) / dict_pos_bigram[(key[0], key[1])]
        key_str = '_'.join(key)   # add key(tri-gram) each time to last key_str
        dict_temp = {'pos_trigram': key_str}
        all_feature_list.append((dict_temp, prob_val))   # append a dictionary in all features list with dict_temp

    """
    # calculate word bigrams now
    bigram_word_list = []
    for word_seq in all_word_sequence:
        bigram_word_list.extend(list(nltk.bigrams(word_seq)))

    # calculate word frequency
    dict_word_bigram = {}
    for entry in bigram_word_list:
        increment_key(dict_word_bigram, entry)
    """

    return all_feature_list


def get_features(word_seq):
    word_seq = 'start/start %s' % (word_seq)
    words = word_seq.split()
    all_features = []
    tag_list = []
    word_list = []
    for entry in words:
        word, tag = entry.rsplit('/', 1)  # word-pos_tag
        tag_list.append(tag)
        word_list.append(word)

    trigram_list = list(nltk.trigrams(tag_list))
    for entry in trigram_list:
        key_str = '_'.join(entry)
        dict_temp = {'pos_trigram': key_str}
        all_features.append(dict_temp)


    return all_features
