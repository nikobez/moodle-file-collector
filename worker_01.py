import configparser
import hashlib
import os
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

def config_read(path):
    config = configparser.ConfigParser()
    config.read(path)
    wdir = config.get("Settings", "work_dir")
    return wdir

def do_md5(fname: str):

    with open(fname, "rb") as file:
        md5 = hashlib.md5(file.read())
    file.close()

    with open(fname + '.md5', "w") as file:
        file.write(md5.hexdigest())
    file.close()

    return

def do_txt(fname: str):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)

    with open(fname, "rb") as file:
        interpreter = PDFPageInterpreter(rsrcmgr, device)
        password = ""
        maxpages = 0
        caching = True
        pagenos=set()
        for page in PDFPage.get_pages(file, pagenos, maxpages=maxpages, password=password,caching=caching, check_extractable=True):
            interpreter.process_page(page)
        text = retstr.getvalue()

    file.close()
    device.close()
    retstr.close()

    with open(fname + '.txt', "w", encoding="utf-8") as file:
        file.write(text)
    file.close()
    return

def do_work(wdir: str):
    dir_list = os.listdir(wdir)
    for sdir in dir_list:
        if os.path.isdir(wdir + '\\' + sdir):
            file_list = os.listdir(wdir + '\\' + sdir)
            print(wdir + '\\' + sdir)
            print(file_list)
            for sfile in file_list:
                print (sfile)
                f_ext = os.path.splitext(sfile)
                print (f_ext[1])
                if f_ext[1] == '.pdf':
                    do_txt(wdir + '\\' + sdir + '\\' + sfile)
                    do_md5(wdir + '\\' + sdir + '\\' + sfile)
    return

if __name__ == "__main__":
    work_dir = config_read('config.ini')
    do_work(work_dir)