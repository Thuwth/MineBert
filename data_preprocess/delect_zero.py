#-*-conding:utf-8-*-
import os

print('------------------------start working------------------------')


def delectBySize(size, txtpath):
    # 删除小于size的文件
    files = os.listdir(txtpath)
    for file in files:
        if os.path.getsize(file) < size * 1000:
            os.remove(os.path.join(txtpath, file))
            print('finish deleting' + file)
    return

def deleteNullFile(txtpath):
    '''删除所有大小为0的文件'''
    files = os.listdir(txtpath)
    for file in files:
        if os.path.getsize(os.path.join(txtpath, file))  == 0:   #获取文件大小
            os.remove(os.path.join(txtpath, file))
            print(file + " deleted.")
    return


