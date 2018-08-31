#!/usr/bin/env python3
# coding =utf-8
import sys

sys.path.append("..")
from dao.keyWordDao import keyWordDao

KeyWordList=[
    {
        "keyword":"绑定",
        "type":"function",
        "value":"add"
    },
    {
        "keyword":"解绑",
        "type":"function",
        "value":"delete"
    },
    {
        "keyword":"成绩",
        "type":"function",
        "value":"selectScore"
    },  
    {
        "keyword":"你好",
        "type":"text",
        "value":"你也好"
    },
    {
        "keyword":"subscribe",
        "type":"text",
        "value":'欢迎关注西安外国语博文天下，本公众号主要用于西安外国语大学成绩查询\n\n西安外国语大学查成绩的同学在公众号回复“成绩”即可\n\n账号密码为教务系统的账号密码，账号密码都默认学号，如果改过就按新的密码查成绩遇到问题的同学请联系博文君微信号：1745649321'
    }
]

flag=keyWordDao.dropkeywordList()
if(flag==True):
    for key in KeyWordList:
        print(key)
        a=keyWordDao()
        a.updateKeywordList(key)
