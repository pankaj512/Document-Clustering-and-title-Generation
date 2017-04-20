# -*- coding: utf-8 -*-
import re
"""
from treetaggerwrapper import TreeTagger

def pos_tagging_head(line):
    tagged_line = ''
    tagger = TreeTagger()
    tagged = tagger.tag_text(line)
    for data in tagged:
        data = data.split('\t')
        tagged_line += data[0] + '/' + data[1] + ' '
    return tagged_line

def pos_tagging_text(lines):
    tagger = TreeTagger()
    text = ''
    for line in lines:
        tagged_line = ''
        tagged = tagger.tag_text(line)
        for data in tagged:
            data = data.split('\t')
            tagged_line += data[0] + '/' + data[1] + ' '
        text += tagged_line+'\n'
    return text
"""
def process_directory():
    """Processes the text files in input directory and puts the final data as a text file in the output directory.

    """
    input_data_path = '../../data/normal_data/'
    out_data_path = 'segmented/'

    # categories of document and total file in each category
    categories = ['business', 'entertainment', 'politics', 'sport', 'tech']
    file_count = [510, 386, 417, 511, 401]

    itr = 0
    for cat in categories:
        for file_no in range(1, file_count[itr] + 1, 1):
            file_name = ""
            if file_no < 10:
                file_name = file_name + '00' + str(file_no)
            elif file_no < 100:
                file_name = file_name + '0' + str(file_no)
            else:
                file_name = file_name + str(file_no)

            file_name = file_name + '.txt'

            try:
                with open(input_data_path + cat + '/' + file_name, 'r') as infile:
                    news = infile.read().split('\n')
                    head = news[0]
                    head = re.sub('[;:!,]','',head)
                    data = '\n'.join(news[1:])
                    data = re.sub('[;:!,]', '', data)
                    data = '.\n'.join(data.split('. '))
                    try:
                        with open(out_data_path+cat+file_name, 'w') as outfile:
                            outfile.write(head+'\n')
                            outfile.write(data)
                    except:
                        print("Error in Write file ")
            except:
                print("Error in Read file ")
        itr += 1
    return


if __name__ == '__main__':
    process_directory()
