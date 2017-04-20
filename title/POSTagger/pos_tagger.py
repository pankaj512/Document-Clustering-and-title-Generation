# -*- coding: utf-8 -*-
import os
from RDRPOSTagger.pSCRDRtagger.RDRPOSTagger4En import RDRPOSTagger4En
from RDRPOSTagger.Utility.Utils import readDictionary

# TODO edit needed in this file for english language tagger

DICTIONARY_LOCATION = '../../RDRPOSTagger/Models/POS/English.DICT'
RDR_LOCATION = '../../RDRPOSTagger/Models/POS/English.RDR'
tagger, DICT = None, None


def initialise():
    global tagger, DICT
    tagger = RDRPOSTagger4En()
    tagger.constructSCRDRtreeFromRDRfile(RDR_LOCATION)
    DICT = readDictionary(DICTIONARY_LOCATION)

    #my_text = "Twitter has found more creative ways to ease its 140-character limit without officially raising it."
    #agged_text = tagger.tagRawEnSentence(DICT,my_text)
    #print(tagged_text)

def parse_directory(input_directory, output_directory):
    global tagger, DICT
    count =1
    print(os.path.abspath(""))
    for file_name in os.listdir(input_directory):
        file_path = os.path.join(input_directory, file_name)
        out_path = os.path.join(output_directory, '%s_TAGGED.txt' % count)
        print(file_path)
        try:
            with open(file_path,'r') as input_file:
                lines = [line.strip() for line in input_file.readlines()]
                tagged_lines = [tagger.tagRawEnSentence(DICT,line) for line in lines]
                head = tagged_lines[0]
                text = '\n'.join(tagged_lines[1:])
                try:
                    with open(out_path,mode='w') as out_file:
                        out_file.write(head+'\n')
                        out_file.write(text)
                except:
                    print("Error in write File")
        except:
            print("Error in read File")
        count+=1
    return

if __name__ == '__main__':
    initialise()
    in_path = 'C:/Users/Pankaj Kumar/Desktop/Project/major/major_project/data/segmented/'
    out_path = 'C:/Users/Pankaj Kumar/Desktop/Project/major/major_project/data/out_pos_tagged'
    parse_directory(in_path,out_path)
