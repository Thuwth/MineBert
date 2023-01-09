import os

def Add_Suffix(path, suffix):
    files = os.listdir(path)
    for file in files:
        if os.path.splitext(file)[1] != '.pdf':
            old_name = os.path.join(path, file)
            new_name = os.path.join(path, file + suffix)
            os.rename(old_name, new_name)

    
filepath = '/home/wth/Mine_data/data'
suffix = '.pdf'
Add_Suffix(filepath, suffix)



