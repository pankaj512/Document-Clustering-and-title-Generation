import os

from title.main.decoding import initialise_all, get_file_headings
from title.main.Utils import remove_tags_from_line


# from title.POSTagger import pos_tagger


def get_file_path(input_path):
    """
    Creates a temp file which maintains the format in which decoding algorithm implements it.
    """
    temp_location = 'temp/trial.txt'
    with open(temp_location, 'w') as file:
        out_file = file
        with open(input_path, 'r') as in_file:
            lines = in_file.readlines()
            headline = lines[0]  # actual headline
            data = lines[1:]
            out_file.writelines(data)

    headline = remove_tags_from_line(headline.split())
    return headline, temp_location


def process_directory(input_dir, output_dir):
    """
    Processes all the files in input directory and writes the output to a different directory

    """
    for file_name in os.listdir(input_dir):
        print('\tGenerating Title for '+file_name)
        output_file = os.path.join(output_dir, '%s_processed.txt' % file_name.split('.')[0])
        with open(output_file, 'w') as out_file:
            headline, file_path = get_file_path(os.path.join(input_dir, file_name))
            top_sentences = get_file_headings(file_path, len(headline.split()))
            out_file.write('%s\n' % headline.strip())  # actual title
            sentences = '\n'.join(top_sentences)  # generated title
            out_file.write(sentences)
        print('\t\tAll top 10 Title written in file')

def generate_tilte(base):
    os.chdir('title/main/')
    initialise_all()

    # os.chdir("../../")
    # in_path = base+'/data/result/test_input/'
    print("Generating Title ....")
    seg_out_path = base + '/data/result/segmented/'  # files with tags in text
    out_path = base + '/data/result/test_output/'

    # pos_tagger.parse_directory(in_path,seg_out_path)
    # os.chdir('../title/main/')

    process_directory(seg_out_path, out_path)
