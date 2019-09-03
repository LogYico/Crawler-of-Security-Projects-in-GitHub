#Coding=UTF-8
from bs4 import BeautifulSoup
import requests
import pymysql
import re
import random

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

def FollowerCrawlerMethod():
    num = 0
    db = pymysql.connect(host='localhost', port=3306, user='GitComment', passwd='123456', db='gc', charset='utf8')
    cursor = db.cursor()
    projects = GetProjectList()

    for projectUrl in projects:
        watchnum = 1
        while True:
            watcherf = requests.get(projectUrl[0] + "/watchers?page=" + str(watchnum))
            watchersoup = BeautifulSoup(watcherf.content, "lxml")
            if watchersoup.find(class_ = 'octicon octicon-eye blankslate-icon'):
                break
            for watcher in watchersoup.find_all("a", class_ = "", attrs = {"data-hovercard-type" : "user"}):#提取关注者信息
                followerName = watcher.get_text()   #获得创建者姓名
                thisFollowerUrl = ("https://api.github.com/search/users?q=" + followerName)        #利用接口获得创建者信息
                cf = requests.get(thisFollowerUrl, headers = HeaderMaker())
                thisWatcherInfo = cf.text
                try:  # 获取用户信息
                    try:
                        id = re.compile('"id":.+?,').search(thisWatcherInfo).group(0).lstrip('"id":').rstrip(',')
                    except:
                        id = 'Null'
                    try:
                        url = re.compile('"url":.+?"').search(thisWatcherInfo).group(0).lstrip('"url":"').rstrip('"')
                    except:
                        url = 'Null'
                    try:
                        type = re.compile('"type":.+?"').search(thisWatcherInfo).group(0).lstrip('"type":"').rstrip('"')
                    except:
                        type = "Null"
                    try:
                        site = re.compile('"site_admin":.+?,').search(thisWatcherInfo).group(0).lstrip('"site_admin":').rstrip(
                            ',')
                        if site == 'false':
                            site_admin = 0;
                        else:
                            site_admin = 1;
                    except:
                        site_admin = 0
                    try:
                        sco = re.compile('"score":.+?}').search(thisWatcherInfo).group(0).lstrip('"score":').rstrip('}')
                        score = float(sco)
                    except:
                        score = 0
                    try:
                        cursor.execute("INSERT INTO follower values ('%s', '%s', '%s', '%s', '%s', '%d', '%f')" % (projectUrl[0], id, followerName, url, type, site_admin, score))
                        db.commit()
                        print("Information of " + projectUrl[1] + "'s watcher "+ followerName + " has been insert success!")
                        num = num +1
                    except Exception as e:
                        db.rollback()
                        print("Information of " + projectUrl[1] + "'s watcher "+ followerName +  " has been insert failed! Error: ", e)
                except Exception as e:
                    print(str(projectUrl[0]) + ":" + str(e))
            watchnum = watchnum + 1

                
    db.close()
    print('\nAll down! ' + str(num) + ' watcher records has been insert!\n')


#FollowerCrawler()