#!/usr/bin/env python3
# coding = utf-8
import sys
import datetime
import time

sys.path.append("..")
from config import configfile
from tools.logger import logger
from dao.model import Scores, User,engine, Session
from dao.userDao import UserDao
from spider.chengji import Score
from spider.login import login

# 成绩操作函数
class ScoreDao:
    def __init__(self,openidStr):
        self.openidStr = openidStr
        self.session = Session()
        self.scoreInfo = Scores()
        self.count = 3
        #允许失败三次

    #比较是否需要更新成绩
    def __compareTime(self,timeB):
        timeA=datetime.datetime.now().date()
        result=timeA-timeB
        if(result.days==0):
            logger.info("用户"+self.openidStr+"今天已经爬取过成绩")
            return True
        else:
            logger.info("用户"+self.openidStr+"今天未调取过爬虫")
            return False
    
    #按照学期查询成绩,直到成绩出现   
    def selectScore(self):
        if(self.count<=0):
            logger.error("用户"+self.openidStr+"查成绩失败")
            return False
        term=configfile.getConfig("term","termStr")
        self.scoreInfo = self.session.query(Scores).filter_by(openid=self.openidStr,termStr=term).first()
        if(self.scoreInfo==None):
            self.scoreInfo = Scores()
            logger.info("用户"+self.openidStr+"数据库中无成绩")
            TrueOrFalse=self.__updateOrInsertScore()
            if(TrueOrFalse==False):
                self.count=self.count-1
            return self.selectScore()
        elif(self.__compareTime(self.scoreInfo.updateTime.date())==False):
            logger.info("用户"+self.openidStr+"使用爬虫爬取成绩")
            TrueOrFalse=self.__updateOrInsertScore()
            if(TrueOrFalse==False):
                self.count=self.count-1
            return self.selectScore()
        else:
            logger.info("用户"+self.openidStr+"从数据库中取成绩")
            return self.scoreInfo.score

    # 插入成绩
    def __insertOrUpdateScore(self,score_json):
        self.scoreInfo.openid = self.openidStr
        self.scoreInfo.score = score_json
        self.scoreInfo.termStr = configfile.getConfig("term","termStr")
        try:
            self.session.add(self.scoreInfo)
            self.session.commit()
            logger.info("用户"+self.openidStr+"成绩更新成功")
            return True
        except:
            logger.info("用户"+self.openidStr+"成绩更新失败")
            return False

    #更新成绩
    def __updateOrInsertScore(self):
        user=UserDao()
        userInfo=user.selectUserInfoByOpenid(self.openidStr)
        username=userInfo[0]
        password=userInfo[1]
        user=Score(username,password)
        scoreStr=user.parseScorePage()
        if(scoreStr != None):
            return self.__insertOrUpdateScore(scoreStr)


a=ScoreDao("123456")
# er=a.insertOrUpdateScore(
#     '[{"name": "\u601d\u60f3\u9053\u5fb7\u4fee\u517b\u4e0e\u6cd5\u5f8b\u57fa\u7840\u5b9e\u8df5", "xuefen": "1", "zuizhong": "87", "jidian": "3.7"}, {"name": "\u4e2d\u56fd\u8fd1\u73b0\u4ee3\u53f2\u7eb2\u8981", "xuefen": "2", "zuizhong": "81", "jidian": "3.1"}, {"name":"\u5927\u5b66\u8bed\u6587II", "xuefen": "2", "zuizhong": "74", "jidian": "2.4"}, {"name": "\u5f62\u52bf\u4e0e\u653f\u7b56I", "xuefen": "1", "zuizhong": "88", "jidian": "3.8"},{"name": "\u4f53\u80b2II", "xuefen": "1", "zuizhong": "91", "jidian": "4.1"}, {"name": "\u5927\u5b66\u751f\u5fc3\u7406\u7d20\u8d28\u62d3\u5c55\u4e0e\u8bad\u7ec3", "xuefen": "2","zuizhong": "91", "jidian": "4.1"}, {"name": "\u521b\u4e1a\u57fa\u7840", "xuefen": "3","zuizhong": "74", "jidian": "2.4"}, {"name": "\u82f1\u8bed\u8bfb\u5199\u57fa\u7840", "xuefen": "2", "zuizhong": "85", "jidian": "3.5"}, {"name": "\u82f1\u8bed\u89c6\u542cII", "xuefen": "2", "zuizhong": "86", "jidian": "3.6"}, {"name": "\u82f1\u8bed\u53e3\u8bedII", "xuefen": "2", "zuizhong": "95", "jidian": "5"}, {"name": "\u9605\u8bfb\u4e0e\u601d\u8fa8\u00b7\u6587\u5316", "xuefen": "2", "zuizhong": "85", "jidian": "3.5"}, {"name": "\u5927\u5b66\u751f\u5fc3\u7406\u5065\u5eb7\u6559\u80b2", "xuefen": "2", "zuizhong": "92","jidian": "4.2"}, {"name": "\u57fa\u7840\u82f1\u8bedII", "xuefen": "6", "zuizhong": "78", "jidian": "2.8"}]'
# )

result=a.selectScore()
print(result)