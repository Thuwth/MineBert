import os
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import shutil


file_path = '/data/wth/Mine_data/splited_data/data/'



def get_txt_len(filepath):
    lens = []
    single_path = '/data/wth/Mine_data/splited_data/single'
    if not os.path.exists(single_path):
        os.mkdir(single_path)

    normal = '/data/wth/Mine_data/splited_data/normal/'
    if not os.path.exists(normal):
        os.mkdir(normal)
    files = os.listdir(filepath)
    for file in files:
        filename = os.path.join(filepath, file)
        with open(filename, 'rb') as f:
            txt_len = len(f.readlines())
            lens.append(txt_len)
            if txt_len >= 10000:
                shutil.move(filename, single_path)
            else:
                shutil.move(filename, normal)
    return lens

lens = get_txt_len(file_path)
plt.figure(num=1, figsize=(12, 8))
plt.bar(range(len(lens)), lens)
plt.savefig('/data/wth/Mine_data/splited_data/bar.jpg')
