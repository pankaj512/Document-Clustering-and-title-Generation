from title.main import dev_test
from title.Evaluation import evaluation
import os


# open file and choose best title by comparing cosine score of each generated title with actual title
def get_best_title(file,in_path,out_path):
    file_path_with_name = os.path.join(in_path, file)
    with open(file_path_with_name, 'r') as filename:
        lines = filename.readlines()
        actual = lines[0]
        generated = lines[1:]
        best_title_line,score = evaluation.evaluate_headline(actual,generated)
        best_title = generated[best_title_line]

    file_path_with_name = os.path.join(out_path, file_name)
    with open(file_path_with_name,'w') as filename:
        filename.write("Actual: "+actual+'\n\n')
        filename.write("Best :"+best_title+'\n\n')
        filename.write('Similarity Score :'+str(score))

    return

if __name__ == '__main__':
    base = os.path.abspath("")
    dev_test.generate_tilte(base)
    in_path = base+'/data/result/test_output/'
    out_path = base +'/data/result/best_tilte_with_cosine/'
    for file_name in os.listdir(in_path):
        try:
            get_best_title(file_name,in_path,out_path)
        except:
            import traceback
            print(traceback.format_exc())

