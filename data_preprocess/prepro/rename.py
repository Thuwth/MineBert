from PyPDF2 import PdfFileWriter, PdfFileReader
import os
from shutil import copy2

src_dir = '/home/wth/data/full/'
tar_dir = '/home/wth/data/new_full/'
num = 0 
EOF_MARKER = b'%%EOF'


# 如果不存在文件夹将创建一个文件夹
if not os.path.exists(tar_dir):
    os.mkdir(tar_dir)

if os.path.exists(src_dir):
    files = os.listdir(src_dir)
    for file in files:
        # 打开并建立一个pdf文件对象
        pdf_reader = PdfFileReader(open(os.path.join(src_dir, file), 'rb'))
        if pdf_reader.isEncrypted:
            pdf_reader.decrypt('')
        # 获取pdf的title
        paper_title = pdf_reader.getDocumentInfo().title
        print('num: %s' %num, paper_title)
        num += 1
        paper_title = str(paper_title)

        if paper_title.find('/') != -1:
            new_paper_title = paper_title.replace('/', '_')
            paper_title = new_paper_title
            copy2(os.path.join(src_dir, file), os.path.join(src_dir, paper_title) + '.pdf')
        else:
            copy2(os.path.join(src_dir, file), os.path.join(tar_dir, paper_title) + '.pdf')

else:
    print('该目录下不存在您要寻找的目录。')