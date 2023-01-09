from data_clean import clean_normal, clean_single_char
from delect_zero import *
import os


txt_type = input('please input your txt type: \n')
txt_type = str(txt_type)


if txt_type == 'normal':
    # clean the normal text
    normal_input_dir_path = '/data/wth/Mine_data/splited_data/normal/'
    normal_output_dir_path = os.path.join('/data/wth/Mine_data/splited_data/output/', txt_type)
    if not os.path.exists(normal_output_dir_path):
        os.mkdir(normal_output_dir_path)

    files = os.listdir(normal_input_dir_path)
    for file in files:
        input_file_name = os.path.join(normal_input_dir_path, file)
        output_file_name = os.path.join(normal_output_dir_path, file)

        clean_normal(input_file_name, output_file_name)
    
    # delect the NULL txt
    deleteNullFile(normal_output_dir_path)

    # merge the txt
    files = os.listdir(normal_output_dir_path)
    file = open('/data/wth/Mine_data/splited_data/output/result/normal_result.txt', 'w')
    for filename in files:
        filepath = os.path.join(normal_output_dir_path, filename)
        for line in open(filepath):
            file.writelines(line)
        file.write('\n')
    file.close()



elif txt_type == 'single':
    # clean the single_char text
    single_input_dir_path = '/data/wth/Mine_data/splited_data/single/'
    normal_output_dir_path = os.path.join('/data/wth/Mine_data/splited_data/output/', txt_type)
    if not os.path.exists(normal_output_dir_path):
        os.mkdir(normal_output_dir_path)

    files = os.listdir(single_input_dir_path)
    for file in files:
        input_file_name = os.path.join(single_input_dir_path, file)
        output_file_name = os.path.join(normal_output_dir_path, file)

        clean_single_char(input_file_name, output_file_name)

    # delect the NULL txt
    deleteNullFile(normal_output_dir_path)

    # merge the txt
    files = os.listdir(normal_output_dir_path)
    file = open('/data/wth/Mine_data/splited_data/output/result/single_result.txt', 'w')
    for filename in files:
        filepath = os.path.join(normal_output_dir_path, filename)
        for line in open(filepath):
            file.writelines(line)
        file.write('\n')
    file.close()


else:
    print('You can only enter "single" and "normal".')
