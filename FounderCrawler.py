#Coding=UTF-8
from bs4 import BeautifulSoup
import requests
import pymysql
import re
import random

def HeaderMaker():  #产生随机token的header，用于使用github的api
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


def GetProjectList():   #获得所有项目链接并存为列表
    db = pymysql.connect(host='localhost', port=3306, user='GitComment', passwd='123456', db='gc', charset='utf8')
    cursor = db.cursor()
    query = ('select * from project')
    cursor.execute(query)

    projects = []
    for thisProject in cursor:
        projects.append([thisProject[0], thisProject[1]])

    db.close()
    print(str(len(projects))+ ' project url has been added.\n')
    return projects

def FounderCrawlerMethod():
    num = 0
    db = pymysql.connect(host='localhost', port=3306, user='GitComment', passwd='123456', db='gc', charset='utf8')
    cursor = db.cursor()
    projects = GetProjectList()
    for projectUrl in projects:
        mf = requests.get(projectUrl[0])
        msoup = BeautifulSoup(mf.content, "lxml")

        for link in msoup.find_all(class_='commit-author tooltipped tooltipped-s user-mention'):  #提取创建者信息
            founderName = link.get_text()   #获得创建者姓名
            thisFounderUrl = ("https://api.github.com/search/users?q=" + founderName)        #利用接口获得创建者信息
            cf = requests.get(thisFounderUrl, headers = HeaderMaker())
            thisCreatorInfo = cf.text
            try:  # 获取用户信息
                try:
                    id = re.compile('"id":.+?,').search(thisCreatorInfo).group(0).lstrip('"id":').rstrip(',')
                except:
                    id = 'Null'
                try:
                    url = re.compile('"url":.+?"').search(thisCreatorInfo).group(0).lstrip('"url":"').rstrip('"')
                except:
                    url = 'Null'
                try:
                    type = re.compile('"type":.+?"').search(thisCreatorInfo).group(0).lstrip('"type":"').rstrip('"')
                except:
                    type = "Null"
                try:
                    site = re.compile('"site_admin":.+?,').search(thisCreatorInfo).group(0).lstrip('"site_admin":').rstrip(
                        ',')
                    if site == 'false':
                        site_admin = 0;
                    else:
                        site_admin = 1;
                except:
                    site_admin = 0
                try:
                    sco = re.compile('"score":.+?}').search(thisCreatorInfo).group(0).lstrip('"score":').rstrip('}')
                    score = float(sco)
                except:
                    score = 0
                try:
                    cursor.execute("INSERT INTO founder values ('%s', '%s', '%s', '%s', '%s', '%d', '%f')" % (projectUrl[0], id, founderName, url, type, site_admin, score))
                    db.commit()
                    print("Information of " + projectUrl[1] + "'s founder "+ founderName + " has been insert success!")
                    num = num +1
                except Exception as e:
                    db.rollback()
                    print("Information of " + projectUrl[1] + "'s founder "+ founderName +  " has been insert failed! Error: ", e)
            except Exception as e:
                print(str(projectUrl[0]) + ":" + str(e))


    db.close()
    print('\nAll down! ' + str(num) + ' founder records has been insert!\n')


#FounderCrawler()