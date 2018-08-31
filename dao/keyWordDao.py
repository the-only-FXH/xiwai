#!/usr/bin/env python3
# coding = utf-8
import sys
import datetime
import time

sys.path.append("..")
from config import configfile
from tools.logger import logger
from dao.model import KeyWord,engine, Session
from sqlalchemy.sql import text

class keyWordDao:
    def __init__(self):
        self.session = Session()
        self.keyword = KeyWord()


    def deletekeyword(self,keyword):
        self.keyword.wordID=keyword
        try:
            self.session.delete(self.keyword)
            self.session.commit()
            logger.info("关键字"+keyword+"删除成功")
            return True
        except:
            logger.info("关键字"+keyword+"删除失败")
            return False

    @staticmethod
    def selectkeyword(keywordStr):
        dbconnect=engine.connect()
        result=dbconnect.execute(text('select result,type from keyword where INSTR(:ID,wordID)'), ID=keywordStr)
        if(result.rowcount<=0):
            return False
        else:
            ru = result.fetchall()[0]
            resultData={
                "type":ru[1],
                "result":ru[0]
            }
            return resultData

    @staticmethod
    def dropkeywordList():
        dbconnect=engine.connect()
        result=dbconnect.execute('delete from keyword')
        if(result.rowcount >=0):
            logger.info("关键字列表已清空")
            return True
        else:
            logger.info("关键字列表清空失败")
            return False

    def updateKeywordList(self,key):
        self.keyword.wordID=key["keyword"]
        self.keyword.type=key["type"]
        self.keyword.result=key["value"]
        keyword=self.session.query(KeyWord).filter_by(wordID=key["keyword"]).first()
        if(keyword is None):
            self.session.add(self.keyword)
            logger.info("关键字"+self.keyword.wordID+"添加成功")
        else:
            keyword.type=self.keyword.type
            keyword.result=self.keyword.result
            logger.info("关键字"+self.keyword.wordID+"更新成功")
        self.session.commit()


#print(keyWordDao().selectkeyword("我要绑定"))

