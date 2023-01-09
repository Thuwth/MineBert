import os
import re
import jionlp

def clean_txt(src_path, tgt_path):
    if os.path.isfile(src_path):
        with open(src_path) as fr:
            data = fr.readlines()
            doc = ''
            for sample in data:
                doc += sample
            doc = jionlp.clean_text(doc)
            doc = doc.replace('\n', '|')
            doc = doc.replace('-|', '')
            # replace all Capital letters
            cap_lets = ['A. ', 'B. ','C. ','D. ','E. ','F. ','G. ','H. ','I. ','J. ','K. ','L. ','M. ','N. ','O. ','P. ','Q. ','R. ','S. ','T. ','U. ','V. ','W. ','X. ','Y. ','Z. ']
            vcap_lets = ['A.', 'B.','C.','D.','E.','F.','G.','H.','I.','J.','K.','L.','M.','N.','O.','P.','Q.','R.','S.','T.','U.','V.','W.','X.','Y.','Z.']
            cap_len = len(cap_lets)
            for i in range(cap_len):
                doc = doc.replace(cap_lets[i], vcap_lets[i])
            # replace typical abbreviations
            typ_obbs = ['doi. ', 'Proc.', 'Ed', 'al.', 'Adv.', 'Mr.', 'Fig.', 'var.', 'pers.', 'desv.', 'carr.', 'Carr.', 'Mpio.', 'Hwy.', 's.n.', 'observ.', 'pp.', 'Vol.', 'Dr.', 'L.T.']
            vtyp_obbs = ['doi.', 'Proc', 'Ed', 'al', 'Adv', 'Mr', 'Fig', 'var', 'pers', 'desv', 'carr', 'Carr', 'Mpio', 'Hwy', 's.n', 'observ', 'pp', 'Vol', 'Dr', 'L.T']
            typ_obb_len = len(typ_obbs)
            for i in range(typ_obb_len):
                doc = doc.replace(typ_obbs[i], vtyp_obbs[i])

            # delete some miscellaneous items
            doc = doc.replace('ac.uk/?pid = resources', '')
            doc = doc.replace('- ', '')

            # replace numbers
            nums = ['(2002).', '(1986).', '(2013).', '(2015).', '(1978).', '(2014).', '(2010).', '(1989).', '(1930).', '(1960).', '(1996).', '(1977).', '(1961).', '(2007).', '(2000).', '(2006).', '(2001).', '(1997).', '(1988).', '(2008).', '(1949).', '(2003).', '(2012).']
            vnums = ['(2002)', '(1986)', '(2013)', '(2015)', '(1978)', '(2014)', '(2010)', '(1989)', '(1930)', '(1960)', '(1996)', '(1977)', '(1961)', '(2007)', '(2000)', '(2006)', '(2001)', '(1997)', '(1988)', '(2008)', '(1949)', '(2003)', '(2012)']
            num_len = len(nums)
            for i in range(num_len):
                doc = doc.replace(nums[i], vnums[i])
            for i in range(50):
                doc = doc.replace(str(i)+'.', str(i))
            sents = doc.split('.|')

                
        with open(tgt_path, "w") as fw:
            for sent in sents:
                sent = sent.strip()
                sent = sent + '.' + '\n'
                # replace double period from the end of sent
                sent = sent.replace('..', '.')
                fw.write(sent)
            fw.write('\n')

    else:
        files = os.listdir(src_path)
        for file in files:
            file_path = os.path.join(src_path, file)
            with open(file_path, "r") as fr:
                data = fr.readlines()
            doc = ''
            for sample in data:
                doc += sample
                doc = doc.replace('\n', ' ')
                doc = doc.replace('  ', ' ')
                # replace all Capital letters
                cap_lets = ['A. ', 'B. ','C. ','D. ','E. ','F. ','G. ','H. ','I. ','J. ','K. ','L. ','M. ','N. ','O. ','P. ','Q. ','R. ','S. ','T. ','U. ','V. ','W. ','X. ','Y. ','Z. ']
                vcap_lets = ['A.', 'B.','C.','D.','E.','F.','G.','H.','I.','J.','K.','L.','M.','N.','O.','P.','Q.','R.','S.','T.','U.','V.','W.','X.','Y.','Z.']
                cap_len = len(cap_lets)
                for i in range(cap_len):
                    doc = doc.replace(cap_lets[i], vcap_lets[i])
                # replace typical abbreviations
                typ_obbs = ['doi. ', 'Proc.', 'Ed', 'al.', 'Adv.', 'Mr.', 'Fig.', 'var.', 'pers.', 'desv.', 'carr.', 'Carr.', 'Mpio.', 'Hwy.', 's.n.', 'observ.', 'pp.', 'Vol.', 'Dr.']
                vtyp_obbs = ['doi.', 'Proc', 'Ed', 'al', 'Adv', 'Mr', 'Fig', 'var', 'pers', 'desv', 'carr', 'Carr', 'Mpio', 'Hwy', 's.n', 'observ', 'pp', 'Vol', 'Dr']
                typ_obb_len = len(typ_obbs)
                for i in range(typ_obb_len):
                    doc = doc.replace(typ_obbs[i], vtyp_obbs[i])

                # delete some miscellaneous items
                doc = doc.replace('ac.uk/?pid = resources', '')
                doc = doc.replace('- ', '')

                # replace numbers
                nums = ['(2002).', '(1986).', '(2013).', '(2015).', '(1978).', '(2014).', '(2010).', '(1989).', '(1930).', '(1960).', '(1996).', '(1977).', '(1961).', '(2007).', '(2000).', '(2006).', '(2001).', '(1997).', '(1988).', '(2008).', '(1949).', '(2003).', '(2012).']
                vnums = ['(2002)', '(1986)', '(2013)', '(2015)', '(1978)', '(2014)', '(2010)', '(1989)', '(1930)', '(1960)', '(1996)', '(1977)', '(1961)', '(2007)', '(2000)', '(2006)', '(2001)', '(1997)', '(1988)', '(2008)', '(1949)', '(2003)', '(2012)']
                num_len = len(nums)
                for i in range(num_len):
                    doc = doc.replace(nums[i], vnums[i])
                for i in range(50):
                    doc = doc.replace(str(i)+'.', str(i))
                sents = doc.split('. ')

                    
            with open(tgt_path, "a") as fw:
                for sent in sents:
                    sent = sent.strip()
                    sent = sent + '.' + '\n'
                    # replace double period from the end of sent
                    sent = sent.replace('..', '.')
                    fw.write(sent)
                fw.write('\n')
        print("finish save data in {}".format(tgt_path))


src_path = "//data/wth/Mine_data/data_clean/file.txt"
tgt_path = "/data/wth/Mine_data/data_clean/file_output.txt"
clean_txt(src_path, tgt_path)