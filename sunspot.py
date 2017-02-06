import os
import shutil
import pandas as pd

def get_filenames(dir_str):
    files = []
    for file in os.listdir(dir_str):
        files.append(file)

    return files

def write_fileList(file_list, file_path):
    with open(file_path, 'w') as file:
        for item in file_list:
            file.write("%s\n" % item)

def read_txt_file(file_path):
    lines = []
    with open(file_path, 'r') as file:
        lines = file.readlines()

    return lines

def convert_filenames_to_csv(file_path, csv_path):
    lines = read_txt_file(file_path)
    rows = []
    for line in lines:
        items = line.strip().split('_')

        rows.append([line.strip(), items[1]])

    df = pd.DataFrame(rows, columns = ['Image', 'class'])
    df.to_csv(csv_path, index=False)

def classify_files(csv_path):
    df = pd.read_csv(csv_path, index_col='Image')
    data_root = csv_path.replace('.csv', '')
    for image in df.index:
        folder = df.loc[image, 'class']
        dst_path = os.path.join(data_root, folder)

        src = os.path.join(data_root, image)
        dst = os.path.join(dst_path, image)
        if not os.path.exists(dst_path):
            os.mkdir(dst_path)

        try:
            shutil.copyfile(src, dst)
        except:
            print('{}, {}'.format(src, dst))

if __name__ == "__main__":
    dirs = ['two_part', 'three_part']
    sub_dirs = ['training', 'validation', 'testing']

    for dirname in dirs:
        for sub_dirname in sub_dirs:
            path = os.path.join(dirname, sub_dirname)
            files = get_filenames(path)
            # print(files)
            file_list_txt = path + '.txt'
            file_list_csv = path + '.csv'
            print(file_list_txt, file_list_csv)
            write_fileList(files, file_list_txt)
            convert_filenames_to_csv(file_list_txt, file_list_csv)

    for dirname in dirs:
        for sub_dirname in sub_dirs:
            path = os.path.join(dirname, sub_dirname)
            file_list_csv = path + '.csv'
            classify_files(file_list_csv)
