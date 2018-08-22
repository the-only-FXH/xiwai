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
    }
]
for key in KeyWordList:
    a=keyWordDao()
    a.updateKeywordList(key)

print("success")