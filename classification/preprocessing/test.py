# This file access each document in each category and
# make a preprocessed text file which contain all the term each document have.
import pandas as pd

def make_input():

    title = []
    stories = []

    input_data_path = '../data/normal_data/'
    output_data_path = '../title/data/'

    # categories of document and total file in each category
    categories = ['business','entertainment','politics','sport','tech']
    file_count = [510,386,417,511,401]

    itr = 0
    for cat in categories:
        for file_no in range(1,file_count[itr]+1,1):
            # category label added to list
            # add news to story
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
                    news =  infile.read().split('\n')
                    title.append(news[0])
                    stories.append('\n'.join(news[1:]))
            except:
                print("Error in Read file "+cat+file_name)
        itr += 1

    #now create excel file from both list
    df_dict = {'Head':title,'News':stories}
    news_data_frame = pd.DataFrame(df_dict)
    news_data_frame.to_excel(output_data_path+'title_document.xlsx', sheet_name='sheet 1', index=False)
    return

if __name__=='__main__':
    make_input()