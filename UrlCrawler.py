#Coding=UTF-8
from bs4 import BeautifulSoup
import requests
import pymysql
import random
import base64


db = pymysql.connect(host='localhost', port=3306,user='GitComment', passwd='123456', db='gc',  charset='utf8')
cursor = db.cursor()

def HeaderMaker():
    header_0 = {
        'User-Agent': 'Mozilla/5.0',
        'Authorization': 'token acea4d74b771b359866e43e0dd7c477741b03064 ',
        'Content-Type': 'application/json',
        'method': 'GET',
        'Accept': 'application/json'
    }
    header_1 = {
        'User-Agent': 'Mozilla/5.0',
        'Authorization': 'token be190d70aa534b5fbcd2e98e5eb2141e90413c0a ',
        'Content-Type': 'application/json',
        'method': 'GET',
        'Accept': 'application/json'
    }
    header_2 = {
        'User-Agent': 'Mozilla/5.0',
        'Authorization': 'token 935d0d8baea35835bd554d123e57a5181c7ce0a7  ',
        'Content-Type': 'application/json',
        'method': 'GET',
        'Accept': 'application/json'
    }
    header = [header_0, header_1, header_2]
    result = header[random.randint(0,2)]
    return result

def UrlCrawlerMethod():
    num = 0
    reNum = 1
    baseUrlNum = 30
    page = requests.Session()       #创建可持续链接
    securityUrl = "https://github.com/topics/security"  # 获取安全类主题页面
    mf = page.get(url = securityUrl, headers = HeaderMaker())

    while reNum:
        urlNum = baseUrlNum * reNum
        encodeStr = ('cursor:'+str(urlNum)).encode('utf-8')
        getNum = str(base64.b64encode(encodeStr), 'utf-8')
        data = {'utf8' : '✓', 'after' : getNum}
        r = page.get(url = securityUrl, data = data)        #发送请求主题的下一页，等效于点击Load More

        msoup = BeautifulSoup(r.content, "lxml")
        for link in msoup.find_all(class_='f3 text-gray text-normal lh-condensed'):  # 获取页面内项目名称
            if len(msoup.find_all(class_='f3 text-gray text-normal lh-condensed')) == 0:
                break
            projects = link.find('a', class_ = 'text-bold')
            projectName = str(projects['href'])
            thisProjectUrl = ("https://github.com" + projectName)  # 生成项目链接
            try:
                #执行sql语句
                cursor.execute("INSERT INTO project values ('%s', '%s')" % (thisProjectUrl, projectName))
                #提交到数据库执行
                db.commit()
                print("Project named"+projectName+"has been insert success!")
                num = num + 1
            except Exception as e:
                db.rollback()
                print("Project named "+projectName+" has been insert failed! Error information: ", e)
        reNum = reNum + 1


    db.close()
    print('\nAll down! ' + str(num) + ' project records has been insert!\n')

#UrlCrawler()