input_data_path = '../data/preprocessed/terms/'
out_data_path = '../data/preprocessed/category_files/'

def make_cat_file():

    # categories of document and total file in each category
    categories = ['business','entertainment','politics','sport','tech']
    file_count = [510,386,417,511,401]

    itr = 0
    for cat in categories:
        try:
            with open(out_data_path+'full_'+cat+'.txt','w') as outfile:
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
                            news =  infile.read()
                            outfile.write(news+'\n')
                    except:
                        print("Error in Read File")
        except:
                print("Error in Out file ")
        itr += 1
    return

if __name__=='__main__':
    make_cat_file()