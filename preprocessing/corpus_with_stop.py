# This file access each document in each category and
# make a preprocessed text file which contain all the term each document have.
import re
def make_term():
    input_data_path = '../data/normal_data/'
    out_data_path = '../data/preprocessed/withStop/'

    # categories of document and total file in each category
    categories = ['business','entertainment','politics','sport','tech']
    file_count = [510,386,417,511,401]

    itr = 0
    for cat in categories:
        for file_no in range(1,file_count[itr]+1,1):
            file_name = ""
            if file_no<10:
                file_name = file_name+'00'+str(file_no)
            elif file_no<100:
                file_name = file_name+'0'+str(file_no)
            else:
                file_name = file_name+str(file_no)

            file_name = file_name+'.txt'

            try:
                with open(input_data_path+cat+'/'+file_name,'r') as infile:
                    news = infile.read().lower()
                    words = re.findall('[a-z]+', news)
                    news = ' '.join(words)
                    try:
                        with open(out_data_path+cat+'/'+file_name,'w') as outfile:
                            outfile.write(news)
                    except:
                        print("Error in Write file ")
            except:
                print("Error in Read file ")
        itr += 1
    return

if __name__=='__main__':
    make_term()