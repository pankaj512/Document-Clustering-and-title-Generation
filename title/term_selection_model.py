from nltk.chunk import tree2conlltags
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree

def ie_preprocess(document,title):

    chunked = ne_chunk(pos_tag(word_tokenize(document)))
    print(chunked)
    iob_tagged = tree2conlltags(chunked)
    print(iob_tagged)
    ans_noun  = {}
    ans_verb = {}
    for word_tuple in iob_tagged:
        if word_tuple[0] in title and 'NN' in word_tuple[1]:
            if word_tuple not in ans_noun:
                ans_noun[word_tuple]=1
            else:
                ans_noun[word_tuple]+=1
        elif 'NE' in word_tuple[1] or 'VB' in word_tuple[1] or word_tuple[0] in title:
            if word_tuple not in ans_verb:
                ans_verb[word_tuple]=1
            else:
                ans_verb[word_tuple]+=1

    sorted_x = sorted(ans_noun, key=lambda x: ans_noun[x],reverse=True)
    print(sorted_x)
    sorted_x = sorted(ans_verb, key=lambda x: ans_verb[x], reverse=True)
    print(sorted_x)

    """
    for i in chunked:
        if type(i) == Tree:
            current_chunk.append(" ".join([token for token, pos in i.leaves()]))
        elif current_chunk:
            named_entity = " ".join(current_chunk)
            if named_entity not in continuous_chunk:
                continuous_chunk.append(named_entity)
                current_chunk = []
        else:
            continue
    """
    return

import pandas as pd
import nltk

if __name__=='__main__':
    news_data_frame = pd.read_excel(io='data/title_document.xlsx', sheetname='sheet 1')
    labels = news_data_frame['Head'].tolist()
    stories = news_data_frame['News'].tolist()
    total = len(stories)
    for i in range(1):
        data = stories[i]
        title = labels[i].split()

        bigram = list(nltk.bigrams(title))
        list_of_bi = []
        for b in bigram:
            list_of_bi.append(' '.join(b))
        title = title + list_of_bi

        entity = ie_preprocess("earthquake announced today",title)
        print('\n'+labels[i])
        print()