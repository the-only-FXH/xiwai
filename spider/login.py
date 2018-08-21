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
        self.username = username
        self.password = password
        self.sess = requests.Session()
        self.proxy = server.get_proxy()
    
    
    def getindex(self, url, header):
        index_info = self.sess.get(url, headers=header, timeout=30, proxies=self.proxy)
        index_html = index_info.text
        pattern = re.compile(
            '[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}-')
        sec_str = pattern.findall(index_html)
        hash_str = sec_str[0]
        hash_str = hash_str + self.password
        sha1 = hashlib.sha1()
        sha1.update(hash_str.encode('utf-8'))
        res = sha1.hexdigest()
        return res

    def post_info(self, url, header, data,):
        self.sess.post(url, headers=header, data=data, timeout=30, proxies=self.proxy)
        return self.sess

    def main(self):
        header = {
            'Host':'jwxt.xisu.edu.cn',
            'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }
        indexurl = "http://jwxt.xisu.edu.cn/eams/login.action"
        realPass = self.getindex(indexurl, header)
        time.sleep(1)
        data = {
            'username': self.username,
            'password': realPass,
            'encodePassword': '',
            'session_locale': 'zh_CN'
        }
        self.sess = self.post_info(indexurl, header, data)
        return self.sess, self.proxy
