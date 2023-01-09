#!/usr/bin/env python3

import os
import shutil

target_path = '/home/wth/data/Metamorphic_rock_txt'

if not os.path.exists(target_path):
    os.mkdir(target_path)

for i in range(0, 101):
    source_path = '/home/wth/data/raw_data/Metamorphic_rock/txt/' + str(i) + 'txt'

    if os.path.exists(source_path):
        for root, dirs, files in os.walk(source_path):
            for file in files:
                src_file = os.path.join(source_path, file)
                shutil.copy(src_file, target_path)
            print('Finished!')
    
print('All Finished!')    