#!/usr/bin/env python3
# coding=utf-8

import requests
import re
import hashlib
import time
import sys
sys.path.append("..")
from tools.logger import logger
from proxy import server


class login:
    def __init__(self, username, password):
        #初始化用户名密码
        self.username = username
        self.password = password
        #初始化Session
        self.sess = requests.Session()
        #拿到代理IP
        self.proxy = server.get_proxy()
        self.header = {
            'Host':'jwxt.xisu.edu.cn',
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
        self.indexurl = "http://jwxt.xisu.edu.cn/eams/login.action"
        self.count=0
    # 访问首页，拿到hash_code
    # 参数：url,请求头
    # 返回值：
    # False:访问首页失败，可能是代理出错了
    # realPass 真正的密码

    def getindex(self):
        try:
            index_info = self.sess.get(self.indexurl, headers=self.header, timeout=5, proxies=self.proxy)
            index_html = index_info.text
        except:
            # 如果访问失败了
            # 换一个代理IP重试一遍
            self.count=self.count+1
            logger.warning("代理ip不可用"+str(self.count)+"次")
            self.proxy = server.get_proxy()
            return self.getindex()
        if(self.count>=3):
            #如果换了两个IP还不行返回失败
            return False

            
        pattern = re.compile(
            '[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}-')
        try:
            sec_str = pattern.findall(index_html)
            if(sec_str==None):
                return False
            hash_str = sec_str[0]
            hash_str = hash_str + self.password
            sha1 = hashlib.sha1()
            sha1.update(hash_str.encode('utf-8'))
            res = sha1.hexdigest()
            return res
        except:
            return False

    def post_info(self, data):
        try:
            result=self.sess.post(self.indexurl, headers=self.header, data=data, timeout=30, proxies=self.proxy)
        except:
            self.post_info(data)
        TrueUrl='http://jwxt.xisu.edu.cn/eams/home.action'
        falseUrl='http://jwxt.xisu.edu.cn/eams/login.action'
        if(result.url==TrueUrl):
            return True
        elif(result.url==falseUrl):
            return False

    def main(self):
        realPass = self.getindex()
        time.sleep(1)
        if(realPass==False):
            return None
        else:
            data = {
                'username': self.username,
                'password': realPass,
                'encodePassword': '',
                'session_locale': 'zh_CN'
            }
            flag=self.post_info(data)
            if(flag==True):
                return self.sess, self.proxy
            else:
                return None
