#!/usr/bin/env python
# coding=utf-8

import sys
from bs4 import BeautifulSoup
sys.path.append("..")
from spider.login import login
import json
import time


class Score:
    def __init__(self,username,password):
        loginOb=login(username,password)
        loginInfo=loginOb.main()
        self.sess=loginInfo[0]
        self.proxy=loginInfo[1]


    def getscore(self):
        url="http://jwxt.xisu.edu.cn/eams/teach/grade/course/person!search.action?semesterId=29&projectType="
        header={
            'Host': 'jwxt.xisu.edu.cn',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36',
            'Referer': 'http://jwxt.xisu.edu.cn/eams/login.action',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests':'1',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }
        try:
            r=self.sess.get(url,headers=header,timeout=30,proxies=self.proxy)
            text=r.text
            return text
        except:
            return("")

    def parseScorePage(self):
        html=self.getscore()
        list=[]
        soup=BeautifulSoup(html,'html.parser')
        thead=soup.find_all('thead')[0]
        th_list=[]
        for th in thead.find_all('th'):
            th_list.append(th.string)
        if '最终'  not in th_list:
            return json.dumps('成绩未出')
        name_num=th_list.index('课程名称')
        xuefen_num=th_list.index('学分')
        zuizhong_num=th_list.index('最终')
        jidian_num=th_list.index('绩点')
        
        table=soup.find_all('tr')
        for tr in table[1:]:
            td=tr.find_all('td')
            list.append({'name':td[name_num].contents[0].replace('\n','').replace('\r','').replace('\t',''),
                         'xuefen':td[xuefen_num].string.replace('\n','').replace('\r','').replace('\t',''),
                         'zuizhong':td[zuizhong_num].string.replace('\r','').replace('\t','').replace(' ','').replace('\n',''),
                         'jidian':td[jidian_num].string.replace('\n','').replace('\r','').replace('\t','')
                        })
        jsonStr=json.dumps(list)
        return jsonStr