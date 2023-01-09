def clean_normal(input_path, output_path):
    one_new_row = ''
    f = open(input_path,'r',encoding = 'utf-8', errors='ignore')
    start_sign = False
    for line in f:   
        ls = line.strip('\n').strip(' ').strip('\t')

        if 'abstract' in ls.lower():
            start_sign = True
        
        if ls.lower() == 'references':
        #     start_sign_ref = True
        # if start_sign_ref == True:
        #     if 'abstract' in ls.lower():
            # start_sign = False
            break

        
        if len(ls) > 1 and start_sign:
            # new_rows.append(line)
            one_new_row += ls + ' '
    f.close()

    new_rows = one_new_row.split('.')

    special_dot_words_list = ['Fig.', 'a/.', 'ql.','AHo1.', 'AHos.','or.', 'U.','Cu1sFe2Sb.', 'of.','aL.', 'pers.', 'ol.', 'U,S.', 'all.', 'et al.','No.','Vol.','Rev.','(i.','etal.','et  al.',', i.','  i.', 'etc.', 'Dr.',
                                'A.', 'B.','C.','D.','E.','F.','G.','H.','I.','J.','K.','L.','M.','N.','O.','P.','Q.','R.','S.','T.','U.','V.','W.','X.','Y.','Z.',
                                'doi. ', 'Proc.', 'Ed', 'al.', 'Adv.', 'Mr.', 'Fig.', 'var.', 'pers.', 'desv.', 'carr.', 'Carr.', 'Mpio.', 'Hwy.', 's.n.', 'observ.', 'pp.', 'Vol.', 'Dr.', 'L.T.']    
    f = open(output_path,'w',encoding='utf-8')
    for new_row in new_rows:
        new_row = new_row.strip('\n').strip(' ').strip('\t') + '.'
        new_row = new_row.replace('- ', '')
        new_row = new_row.replace('  ', ' ')

        # delect special words
        new_row = new_row.replace('ABSTRAcT ', '')
        new_row = new_row.replace('INTRODUCTION ', '')
        new_row = new_row.replace('ANALYTICAL METHoDS AND DATA ', '')


        is_new_line = True
        for special_dot_words in special_dot_words_list:
            if special_dot_words == new_row[-len(special_dot_words):] or new_row=='e.':
                is_new_line = False
                break

        if is_new_line:
            new_row = new_row+'\n'

        if ' ' in new_row:  
            first_token = new_row.split(' ')[0]
            if not first_token.isdigit():
                f.write(new_row)
    f.close()

def clean_single_char(input_path, output_path):
    f = open(input_path,'r',encoding='utf-8',errors='ignore')

    one_new_row = ''

    is_blank = False
    for line in f:   
        if not is_blank:
            one_new_row += line.strip('\n')
            is_blank = True
        else:
            is_blank = False
    f.close()
    try:
        start_idx = one_new_row.index('Abstract')
    except:
        start_idx = 0
    try:
        end_idx = one_new_row.index('References')
    except:
        end_idx = -1
    one_new_row = one_new_row[start_idx:end_idx]

    new_rows = one_new_row.split('.')

    

    special_dot_words_list = ['Fig.', 'a/.', 'ql.','AHo1.', 'AHos.','or.', 'U.','Cu1sFe2Sb.', 'of.','aL.', 'pers.', 'ol.', 'U,S.', 'all.', 'et al.','No.','Vol.','Rev.','(i.','etal.','et  al.',', i.','  i.', 'etc.', 'Dr.',
                                'A.', 'B.','C.','D.','E.','F.','G.','H.','I.','J.','K.','L.','M.','N.','O.','P.','Q.','R.','S.','T.','U.','V.','W.','X.','Y.','Z.',
                                'doi. ', 'Proc.', 'Ed', 'al.', 'Adv.', 'Mr.', 'Fig.', 'var.', 'pers.', 'desv.', 'carr.', 'Carr.', 'Mpio.', 'Hwy.', 's.n.', 'observ.', 'pp.', 'Vol.', 'Dr.', 'L.T.']

    f = open(output_path,'w',encoding='utf-8')
    for new_row in new_rows:
        new_row = new_row.strip('\n').strip(' ').strip('\t') + '.'
        new_row = new_row.replace('- ', '')
        new_row = new_row.replace('  ', ' ')

        # delect special words
        new_row = new_row.replace('ABSTRAcT ', '')
        new_row = new_row.replace('INTRODUCTION ', '')
        new_row = new_row.replace('ANALYTICAL METHoDS AND DATA ', '')

        is_new_line = True
        for special_dot_words in special_dot_words_list:
            if special_dot_words == new_row[-len(special_dot_words):] or new_row=='e.':
                is_new_line = False
                break

        if is_new_line:
            new_row = new_row+'\n'

        if ' ' in new_row:  
            first_token = new_row.split(' ')[0]
            if not first_token.isdigit():
                f.write(new_row)
    f.close()


'''
input_path = 'input_normal.txt'
output_path = 'output_normal.txt'
clean_normal(input_path, output_path)

input_path = 'input_single_char.txt' # 'input_normal.txt'
output_path = 'output_single_char.txt' # 'output_normal.txt'
clean_single_char(input_path, output_path)
'''
input_path = '/data/wth/Mine_data/data_clean/file.txt'
output_path = '/data/wth/Mine_data/data_clean/file1.txt'
clean_normal(input_path, output_path)
