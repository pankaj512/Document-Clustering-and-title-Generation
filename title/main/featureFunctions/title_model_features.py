# define all the feature functions here
"""
List of features used:
1. Language model features
2. title Length feature
3. Part of Speech Language Model Feature
4. N-Gram Match feature
5. Content selection feature
"""

import math

# model feature tuple
feature_values = []

# structures for title length feature
Unique_length_count = 0  # range considered is 3 to 15(13 values )
title_length_count = {}
title_length_probability = {}
# structures for language model feature
unique_bigram_count = 0
language_model_count = {}
language_model_probability = {}
word_count = {}
# structure for pos title bigram feature
unique_bigram_pos_count = 0
bigram_model_count = {}

# structure for pos title trigram feature
unique_trigram_pos_count = 0
trigram_model_count = {}
trigram_model_probability = {}


def compute_title_length_counts(title_word_tag_list):
    """
    Input: A list with each entry having title from input corpus
    operation: computes the title length for each article title  and stores the probability 
    for each title length in a length dictionary
    """
    global title_length_count, Unique_length_count  # range considered is 3 to 15(13)

    for title in title_word_tag_list:
        count = 0
        tokens = title.split(" ")
        for entry in tokens:
            word, tag = entry.rsplit('/', 1)
            count += 1

        if count in title_length_count:
            title_length_count[count] += 1
        else:
            title_length_count[count] = 1
            Unique_length_count += 1


def compute_title_length_probability(title_word_tag_list):
    """
    Input: A list with each entry having title from input corpus
    operation: computes the title length for each article title  and stores the probability
     for each title length in a length dictionary
    """
    global title_length_count, Unique_length_count, title_length_probability  # range considered is 3 to 15(13)

    title_length_probability = title_length_count.copy()
    # computing total title count
    total_no_of_titles = len(title_word_tag_list)
    compute_title_length_counts(title_word_tag_list)

    for i in title_length_count:
        # print "key:"+str(i)+" val:"+str(title_length_count[i])
        temp = (title_length_count[i]) / float(total_no_of_titles)
        # print "temp:"+str(temp)
        title_length_probability[i] = temp


def compute_word_count(title_word_tag_list):
    """
    Input: A list with each entry having title from input corpus
    operation: computes the word count of each word in dataset
    """

    global word_count
    for title in title_word_tag_list:
        tokens = title.split(" ")
        for entry in tokens:
            word, tag = entry.rsplit('/', 1)
            if word in word_count:
                word_count[word] += 1
            else:
                word_count[word] = 1


def compute_language_model_counts(title_word_tag_list):
    """
    Input: A list with each entry having title from input corpus
    operation: computes the language model counts for each article bigram  and stores the probability for each bigram in dictionary
    """
    global language_model_count, unique_bigram_count

    for title in title_word_tag_list:
        tokens = title.split(" ")
        prev = "start"
        cur = "start"
        for entry in tokens:
            word, tag = entry.rsplit('/', 1)
            prev = cur
            cur = word

            if prev in language_model_count:
                if cur in language_model_count[prev]:
                    language_model_count[prev][cur] += 1
                else:
                    language_model_count[prev][cur] = 1
            else:
                language_model_count[prev] = {}
                if cur in language_model_count[prev]:
                    language_model_count[prev][cur] += 1
                else:
                    language_model_count[prev][cur] = 1


def compute_language_model_probability(title_word_tag_list):
    """
    Input: A list with each entry having title from input corpus
    operation: computes the language model probability for each article bigram  and stores the probability for each bigram in  dictionary
    """
    global language_model_count, unique_bigram_count, language_model_probability, word_count

    compute_word_count(title_word_tag_list)
    compute_language_model_counts(title_word_tag_list)
    language_model_probability = dict(language_model_count)

    for title in title_word_tag_list:

        tokens = title.split(" ")
        prev = "start"
        cur = "start"
        mycount = 0
        for entry in tokens:
            mycount = mycount + 1
            word, tag = entry.rsplit('/', 1)
            prev = cur
            cur = word

            if mycount >= 2:
                if prev in language_model_probability:
                    if cur in language_model_probability[prev]:
                        language_model_probability[prev][cur] = (language_model_count[prev][cur]) / float(
                            word_count[prev])
                    else:
                        language_model_probability[prev][cur] = (language_model_count[prev][cur]) / float(
                            word_count[prev])
                else:

                    language_model_probability[prev] = {}
                    language_model_probability[prev][cur] = (1) / float(word_count[prev])


def compute_bigram_counts(title_word_tag_list):
    """
    Input: A list with each entry having title from input corpus
    operation: computes the language model counts for each article bigram  and stores the probability for each bigram POSin  dictionary
    """

    global bigram_model_count, unique_bigram_pos_count

    for title in title_word_tag_list:
        tokens = title.split(" ")
        prev = "start"
        cur = "start"
        for entry in tokens:
            word, tag = entry.rsplit('/', 1)
            prev = cur
            cur = tag

            if prev in bigram_model_count:
                if cur in bigram_model_count[prev]:
                    bigram_model_count[prev][cur] += 1
                else:
                    bigram_model_count[prev][cur] = 1
            else:
                bigram_model_count[prev] = {}
                if cur in bigram_model_count[prev]:
                    bigram_model_count[prev][cur] += 1
                else:
                    bigram_model_count[prev][cur] = 1


def compute_trigram_counts(title_word_tag_list):
    """
    Input: A list with each entry having title from input corpus
    operation: computes the language model counts for each article trigram  and stores the probability for each trigram POS in  dictionary
    """

    global trigram_model_count, unique_trigram_pos_count
    local_trigram_count = 0
    lc = 0
    # print title_word_tag_list
    for title in title_word_tag_list:
        local_trigram_count += 1
        # print str(local_trigram_count)+")current line:"+title

        tokens = title.split(" ")
        prev = "start"
        cur = "start"
        next = "start"
        # print "line:"+title
        for entry in tokens:
            word, tag = entry.rsplit('/', 1)
            prev = cur
            cur = next
            next = tag

            # print "LC:"+str(lc)
            if prev in trigram_model_count:
                # print "in if"
                if cur in trigram_model_count[prev]:
                    # print "in if if"
                    if next in trigram_model_count[prev][cur]:
                        # print "in if if if"
                        trigram_model_count[prev][cur][next] += 1
                        # print "dict:"+str(trigram_model_count)
                    else:
                        # unique_trigram_pos_count = unique_trigram_pos_count+1
                        # print "in if if else"
                        trigram_model_count[prev][cur] = {}
                        trigram_model_count[prev][cur][next] = 1
                        # print "dict:"+str(trigram_model_count)

                else:
                    # print "in if else"

                    trigram_model_count[prev][cur] = {}
                    trigram_model_count[prev][cur][next] = 1
                    # print "dict:"+str(trigram_model_count)
            else:
                # print "in else"
                trigram_model_count[prev] = {}
                trigram_model_count[prev][cur] = {}
                trigram_model_count[prev][cur][next] = 1
                # print "dict:"+str(trigram_model_count)

            lc += 1
            # print "########################################################################"


# P( wi | wi-1 wi-2 ) = count ( wi, wi-1, wi-2 ) / count ( wi-1, wi-2 )



def compute_pos_language_model(title_word_tag_list):
    """ Input: A list with each entry having title from input corpus
    operation: computes the language model probability for each trigrams of POS  and stores the probability for each trigram POS in  dictionary

    """
    global trigram_model_probability, trigram_model_count, trigram_model_probability, bigram_model_count
    compute_trigram_counts(title_word_tag_list)
    compute_bigram_counts(title_word_tag_list)

    trigram_model_probability = dict(trigram_model_count)
    # computes POS language model probability
    for title in title_word_tag_list:
        prev = "start"
        cur = "start"
        next = "start"
        tokens = title.split(" ")
        mycount = 0
        for entry in tokens:
            word, tag = entry.rsplit('/', 1)
            prev = cur
            cur = next
            next = tag
            # print "&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&"
            # print "prev:"+prev+" cur:"+cur+" next:"+next+"my count:"+str(mycount)

            if mycount > 1:

                if prev in trigram_model_probability:

                    if cur in trigram_model_probability[prev]:

                        if next in trigram_model_probability[prev][cur]:
                            temp = (trigram_model_count[prev][cur][next]) / float(bigram_model_count[prev][cur])
                            trigram_model_probability[prev][cur][next] = temp
            mycount += 1


def compute_POS_language_feature(title_word_tag_list):
    """ Returns POS language model feature value for the title
    """
    global trigram_model_probability
    POSLM_feature = 0
    prev = "start"
    cur = "start"
    next = "start"
    count = 1

    # initialization of dictionary
    tokens = title_word_tag_list.split(" ")
    for entry in tokens:
        word, tag = entry.rsplit('/', 1)
        prev = cur
        cur = next
        next = tag
        count += 1
        # print "prev:"+prev+" cur:"+cur+" next:"+next
        if count > 2:
            if prev in trigram_model_probability:
                if cur in trigram_model_probability[prev]:
                    if next in trigram_model_probability[prev][cur]:
                        probability = trigram_model_probability[prev][cur][next]
                        POSLM_feature = POSLM_feature + math.log(probability, 10)

    return POSLM_feature


def compute_title_length_feature(title_word_tag_list):
    """
    computes the log probability of particular title length and returns the value
    """
    global title_length_probability
    Length_feature = 0
    count = 0
    total_no_of_titles = 0
    for i in title_length_count:
        total_no_of_titles = total_no_of_titles + title_length_count[i]

    tokens = title_word_tag_list.split(" ")
    for entry in tokens:
        word, tag = entry.rsplit('/', 1)
        count = count + 1

    if count in title_length_probability:
        Length_feature = math.log(title_length_probability[count], 10)
    else:
        temp = 1 / float(total_no_of_titles)
        Length_feature = math.log(temp, 10)
    return Length_feature


def compute_language_model_feature(title):
    """Returns the language model feature value
    """
    global language_model_probability, word_count

    total_word_count = 0
    for i in word_count:
        total_word_count = total_word_count + word_count[i]
        # print "total word count:"+str(total_word_count)

    prev = "start"
    cur = "start"

    title = title.strip()
    WordOfLine = title.split()
    mycount = 0
    LM_value = 0
    tokens = title.split(" ")
    for entry in tokens:
        word, tag = entry.rsplit('/', 1)
        prev = cur
        cur = word
        # print "in prev:"+prev+"cur:"+cur+"count:"+str(mycount)
        mycount += 1
        if mycount > 1:

            if prev in language_model_probability:

                if cur in language_model_probability[prev]:

                    LM_value = LM_value + math.log(language_model_probability[prev][cur], 10)
                    # print "log LMvalue:"+str(math.log(language_model_probability[prev][cur],10))
                # if word given previous word probability does not exist we use others value as smoothing measure
                else:
                    temp = 1 / (word_count[prev])
                    LM_value += math.log(temp, 10)
            else:
                temp = 1 / (total_word_count)
                LM_value += math.log(temp, 10)

    return LM_value


def get_title_synthesis_features(title_word_tag_list):
    '''
    calls the feature functions and stores feature values for the model in a tuple in the format
    ({POSLM:"NN VB NN"},outcome,{title_len,len_val},outcome,
    '''
    global title_length_probability, language_model_probability, trigram_model_probability, feature_values
    compute_pos_language_model(title_word_tag_list)
    compute_language_model_probability(title_word_tag_list)
    compute_title_length_probability(title_word_tag_list)
    # adding all features of one title


    for head in title_word_tag_list:
        # print "####################################################################################"
        # print "line:"+head
        count = 0
        tokens = head.split(" ")
        # adding feature 1
        for entry in tokens:
            word, tag = entry.rsplit('/', 1)
            count += 1
        temp_dict = {'title_len': count}

        feature1 = (temp_dict, title_length_probability[count])
        # print "current f1 value:"+str(feature1)

        feature_values.append(feature1)

        # adding feature 2
        POSLM_feature = compute_POS_language_feature(head)
        pos_string = ""
        temp_dict = {}
        # print "pos tag string:"+pos_string

        # initialization of dictionary
        # tokens = head.split(" ")
        for entry in tokens:
            word, tag = entry.rsplit('/', 1)
            pos_string = pos_string + tag + " "
        temp_dict['pos_LM'] = pos_string
        feature2 = (temp_dict, POSLM_feature)
        feature_values.append(feature2)
        # print temp_dict
        # print "current f2 value:"+str(feature2)
        # adding feature 3
        LM_feature = compute_language_model_feature(head)
        word_bigram_string = ""
        temp_dict = {}
        # print "word  string:"+word_bigram_string
        prev = "start"
        cur = "start"
        lm = 0

        # tokens = head.split(" ")
        for entry in tokens:
            word, tag = entry.rsplit('/', 1)
            prev = cur
            cur = word
            word_bigram_string = word_bigram_string + " " + prev + "-" + cur

        # print "word  string:"+word_bigram_string
        LMvalue = compute_language_model_feature(head)
        temp_dict['LM'] = word_bigram_string
        feature3 = (temp_dict, LMvalue)
        feature_values.append(feature3)
        # print "current f3 value:"+str(feature3)
        del feature1
        del feature2
        del feature3
        # print feature_values
    return feature_values


def get_classification_dictionary(title_word_tag_list):
    '''
    returns the list of the form
    {'title_len': 3}, ({'pos_LM': 'NN VV MM '},'{'LM': ' start-a a-b b-c'},
    '''
    local_dict = {}
    count = 0
    tokens = title_word_tag_list.split(" ")
    # adding feature 1
    for entry in tokens:
        count += 1
    local_dict['title_len'] = count

    # adding feature 2

    pos_string = ""
    for entry in tokens:
        word, tag = entry.rsplit('/', 1)
        pos_string = pos_string + tag + " "
    local_dict['pos_LM'] = pos_string

    word_bigram_string = ""
    prev = "start"
    cur = "start"
    lm = 0

    for entry in tokens:
        word, tag = entry.rsplit('/', 1)
        prev = cur
        cur = word
        word_bigram_string = word_bigram_string + " " + prev + "-" + cur

    local_dict['LM'] = word_bigram_string
    return local_dict
