import urllib
import requests

from bs4 import BeautifulSoup, BeautifulStoneSoup
from lxml import html
import xml
import requests
import pymysql as MySQLdb
import re
from _overlapped import NULL
from Tools.scripts.generate_opcode_h import header
from urllib import request
import pymysql

db = pymysql.connect(host='localhost', port=3306,user='GitComment', passwd='123456', db='gc',  charset='utf8')
cursor = db.cursor()

securityUrl = "https://github.com/topics/security"  # ��ȡ��ȫ������ҳ��
header = {
    'User-Agent': 'Mozilla/5.0',
    'Authorization': 'token ba38c8a41a2110af14f1b823dc3fc78fec85850c',
    'Content-Type': 'application/json',
    'method': 'GET',
    'Accept': 'application/json'
}
data = None
mf = requests.get(securityUrl)
msoup = BeautifulSoup(mf.content, "lxml")
followersUrlList = []  # ������Ŀ����洢��Ŀ����
for link in msoup.find_all(class_='f3'):  # ��ȡҳ������Ŀ����
    projects = link.find('a', href=True)
    projectName = str(projects['href'])
    thisProjectUrl = ("https://github.com" + projectName)  # ������Ŀ����
    pf = requests.get(thisProjectUrl)
    psoup = BeautifulSoup(pf.content, "lxml")
    try:  # ��ȡ�û��ǳ�,����û��ǳƲ����������
        userNameBlock = psoup.find(class_="commit-author tooltipped tooltipped-s user-mention")
        thisCreatorInfoUrl = ("https://github.com/" + str(userNameBlock.get_text()))
        cf = requests.get(thisCreatorInfoUrl)
        csoup = BeautifulSoup(cf.content, "lxml")
        creatorsInfoBlock = csoup.find(class_="p-name vcard-fullname d-block overflow-hidden")
        if len(str(creatorsInfoBlock.get_text())) != 0:
            thisCreatorUrl = ("https://api.github.com/search/users?q=fullname:" + str(creatorsInfoBlock.get_text()))
        cf = requests.get(thisCreatorUrl)
        thisCreatorInfo = cf.text
        try:  # ��ȡ�û���Ϣ
            userName = re.compile('"login":.+?"').search(thisCreatorInfo).group(0).lstrip('"login":"').rstrip('"')
            id = re.compile('"id":.+?,').search(thisCreatorInfo).group(0).lstrip('"id":').rstrip(',')
            url = re.compile('"url":.+?"').search(thisCreatorInfo).group(0).lstrip('"url":"').rstrip('"')
            type = re.compile('"type":.+?"').search(thisCreatorInfo).group(0).lstrip('"type":"').rstrip('"')
            site = re.compile('"site_admin":.+?,').search(thisCreatorInfo).group(0).lstrip('"site_admin":').rstrip(',')
            if site == 'false':
                site_admin = 0;
            else:
                site_admin = 1;
            sco = re.compile('"score":.+?}').search(thisCreatorInfo).group(0).lstrip('"score":').rstrip('}')
            score = float(sco)
            try:
                #ִ��sql���
                cursor.execute("INSERT INTO founder values ('%s', '%s', '%s', '%s', '%d', '%f')" % (userName, id, url, type, site_admin, score))
                #�ύ�����ݿ�ִ��
                db.commit()
                print("success")

                #�����ǻ�ȡ��Ŀ�Ĺ�ע��
                pagenum = 1
                while True:
                    try:
                        watchersPgae = (thisProjectUrl + "watchers?page="+str(pagenum)) #��ȡ��ע��ҳ������
                        watchersf = requests.get(watchersPgae)
                        watcherssoup = BeautifulSoup(watchersf.content, "lxml")
                        for watchersblock in watcherssoup.find_all(class_="css-truncate css-truncate-target"):
                            for watcherstext in watchersblock.find_all("a"):
                                watchersUrl = ("https://api.github.com/search/users?q=fullname:" + str(watcherstext.get_text()))
                                watchersUrlf = requests.get(thisCreatorUrl)
                                thisWatcherInfo = watchersf.text
                                try:  # ��ȡ�û���Ϣ
                                    userName = re.compile('"login":.+?"').search(thisWatcherInfo).group(0).lstrip(
                                        '"login":"').rstrip('"')
                                    id = re.compile('"id":.+?,').search(thisWatcherInfo).group(0).lstrip(
                                        '"id":').rstrip(',')
                                    url = re.compile('"url":.+?"').search(thisWatcherInfo).group(0).lstrip(
                                        '"url":"').rstrip('"')
                                    type = re.compile('"type":.+?"').search(thisWatcherInfo).group(0).lstrip(
                                        '"type":"').rstrip('"')
                                    site = re.compile('"site_admin":.+?,').search(thisWatcherInfo).group(0).lstrip(
                                        '"site_admin":').rstrip(',')
                                    if site == 'false':
                                        site_admin = 0;
                                    else:
                                        site_admin = 1;
                                    sco = re.compile('"score":.+?}').search(thisWatcherInfo).group(0).lstrip(
                                        '"score":').rstrip('}')
                                    score = float(sco)
                                    try:    #��ȡ��ע����Ϣ
                                        # ִ��sql���
                                        cursor.execute("INSERT INTO watcher values ('%s', '%s', '%s', '%s', '%d', '%f')" % (userName, id, url, type, site_admin, score))
                                        # �ύ�����ݿ�ִ��
                                        db.commit()
                                        print("success")
                                    except:
                                        db.rollback()
                                        print("false")
                                except:
                                    pass
                                continue
                        i = i+1     #��ҳ
                    except:
                        break
            except:
                db.rollback()
                print("false")
        except:
            pass
        continue
    except:
        pass
    continue

db.close()