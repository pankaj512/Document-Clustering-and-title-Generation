from nltk.chunk import tree2conlltags
from nltk import ne_chunk, pos_tag, word_tokenize
from nltk.tree import Tree
import pickle
import pandas as pd

def ie_preprocess_title(title):
    chunked = ne_chunk(pos_tag(word_tokenize(title)),binary=False)
    iob_tagged = tree2conlltags(chunked)

    ans_tag  = []
    for term_tuple in iob_tagged:
        ans_tag.append(term_tuple[1])

    entity_term = []
    prev = None
    current_chunk = []
    for chunk in chunked:
        if type(chunk) == Tree:
            current_chunk.append(" ".join([token for token, pos in chunk.leaves()]))
        elif current_chunk:
            named_entity = " ".join(current_chunk)
            if named_entity not in entity_term:
                entity_term.append(named_entity)
                current_chunk = []
        else:
            continue
    return ans_tag, entity_term

def ie_preprocess_data(document,tags):
    chunked = ne_chunk(pos_tag(word_tokenize(document)), binary=False)
    entry_term = []
    prev = None
    continuous_chunk = []
    current_chunk = []
    for chunk in chunked:
        if type(chunk) == Tree:
            tokens = []
            token_tag = ""
            for entry in chunk.leaves():
                tokens.append(entry[0])
                token_tag = entry[1]
            current_chunk.append(" ".join(tokens))
        elif current_chunk:
            named_entity = " ".join(current_chunk)
            if named_entity not in continuous_chunk:
                continuous_chunk.append((named_entity,token_tag))
                current_chunk = []
                token_tag = ""
        else:
            continue

    for entry in continuous_chunk:
        if entry[1] in tags and entry[0] not in entry_term:
            entry_term.append(entry[0])
    return entry_term

def training_model():
    news_data_frame = pd.read_excel(io='data/title_document.xlsx', sheetname='sheet 1')
    labels = news_data_frame['Head'].tolist()
    stories = news_data_frame['News'].tolist()
    total = len(stories)

    tag_dict = {}
    entity_list = []

    for i in range(total):
        data = stories[i]
        title = labels[i]
        tags, entity_list_title = ie_preprocess_title(title)
        entity_list_data = ie_preprocess_data(data,tags)
        entity_list += entity_list_title + entity_list_data
        for tag in tags:
            if tag not in tag_dict:
                tag_dict[tag]=1
            else:
                tag_dict[tag]+=1
    tags = sorted(tag_dict, key=lambda x:tag_dict[x],reverse=True)
    with open('data/tags.p','wb') as file:
        pickle.dump(tags,file,protocol=pickle.HIGHEST_PROTOCOL)
    with open('data/words.p','wb') as file:
        pickle.dump(entity_list,file,protocol=pickle.HIGHEST_PROTOCOL)


def test_model(document,title):
    with open('data/tags.p','rb') as file:
        tags = pickle.load(file)
        print(tags)
        entity_terms = ie_preprocess_data(document,tags)
        print(entity_terms)
        print(title)

if __name__=='__main__':
    with open('test_data.txt','r') as file:
        lines = file.read().split('\n')
        title = lines[0]
        data = '\n'.join(lines[1:])
        test_model(data,title)
