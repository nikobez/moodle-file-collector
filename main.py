import requests
import urllib.parse
import configparser
import bs4
import re
import os

auth_data = {
    'login': 'xxx',
    'password': 'xxx',
    'url': 'https://sdo.xxx.ru',
    'url_course': 'https://sdo.xxx.ru/course/view.php?id=xxx'
}

work_dir = ''

results_table = []

def moodle_auth(data: dict):
    login, password, url_domain, url_course = data.values()
    s = requests.Session()
    rq1 = s.get(url=url_domain + "/login/index.php")
    pattern_auth = '<input type="hidden" name="logintoken" value="\w{32}">'
    token = re.findall(pattern_auth, rq1.text)
    token = re.findall("\w{32}", token[0])[0]
    payload = {'anchor': '', 'logintoken': token, 'username': login, 'password': password, 'rememberusername': 1}
    rq2 = s.post(url=url_domain + "/login/index.php", data=payload)
    counter = 0
    for i in rq2.text.splitlines():
        if "loginerrors" in i or (0 < counter <= 3):
            counter += 1
            print(i)
    return s

def moodle_getassign(data: dict, s: requests.Session()):
    login, password, url_domain, url_course = data.values()
    rq3 = s.get(url_course)
    soup = bs4.BeautifulSoup(rq3.content, 'lxml')
    linkp = soup.find_all('a')
    links = []
    for link in linkp:
        islink = str(link.get('href')).find('/mod/assign/')
        if islink > 0:
            links.append(str(link.get('href')))
    return links

def moodle_getdata( links: list, s: requests.Session()):
    for link in links:
        rq4 = s.get(link+'&action=grading')
        soup = bs4.BeautifulSoup(rq4.content, 'lxml')
        print('===> Start '+link)
        tr_list = soup.find_all('tr')
        del tr_list[0]
        for tr_ in tr_list:
            if not (str(tr_.find('label')) == ''):
                name = str(tr_.find('label')).partition('>')[2]
                name = name.partition('<')[0]
                name = name.partition(' ')[2]
                if not (name == ''):
                    files = tr_.find_all('a')
                    urls = []
                    for f_ref in files:
                        s_ref = f_ref.get('href')
                        if s_ref.find('/assignsubmission_file/submission_files') > 0:
                            urls.append(s_ref)
                    file_save(urls, name, s)
    return links

def filename_clear(url: str):
    file_name = urllib.parse.unquote(url)
    file_name = file_name.split("#")[0]
    file_name = os.path.basename(file_name.split("?")[0])
    return file_name

def module_id_get(url: str):
    print(url)
    id = url.partition('.')[2]
    id = id.partition('/')[2]
    id = id.partition('/')[2]
    id = id.partition('/')[0]
    return id

def table_save(f_name: str, ):

    return

def file_save(links: list, f_name: str, s: requests.Session()):
    global work_dir
    for link in links:
        cl_name = filename_clear(link)
        cl_dir = work_dir + '\\' + module_id_get(link)
        file_name =  cl_dir + '\\' + f_name + '_' + cl_name
        print('   [> ' + file_name)
        if not os.path.isdir(cl_dir):
            os.mkdir(cl_dir)
        with open(file_name, "wb") as file:
            response_bin = s.get(link)
            file.write(response_bin.content)
        file.close()
    return s

def config_read(path):
    global auth_data
    global work_dir
    config = configparser.ConfigParser()
    config.read(path)

    d_login = config.get("Settings", "login")
    d_password = config.get("Settings", "password")
    d_url = config.get("Settings", "url")
    d_url_course = config.get("Settings", "url_course")
    work_dir = config.get("Settings", "work_dir")
    auth_data.update ({'login': d_login,'password': d_password,'url': d_url, 'url_course': d_url_course})

if __name__ == "__main__":
    config_read('config.ini')
    ses = moodle_auth( data=auth_data )
    print(ses)
    course_links = moodle_getassign(auth_data,ses)
    print(course_links)
    print(moodle_getdata(course_links,ses))