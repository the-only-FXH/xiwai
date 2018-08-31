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
        #openid
        self.openidStr = openidStr
        #Session初始化
        self.session = Session()
        #分数返回结果初始化
        self.count=0
        #判断该用户是否绑定
        

        
    #比较是否需要更新成绩
    # 参数：数据库中取出的时间
    # 返回值：
    # True：今天访问过教务系统
    # False:今天未访问教务系统
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
    # 参数：无  
    # 返回值：
    # 1：用户未绑定
    # 2：查成绩超过三次超时
    # score：成绩字符串
    def selectScore(self):
        if(self.count>=2):
            #失败次数大于2次
            return 2

        #从数据库中拿出成绩
        term=configfile.getConfig("term","termStr")
        scoreInfo = self.session.query(Scores).filter_by(openid=self.openidStr,termStr=term).first()
        #如果数据库中的成绩不存在
        if(scoreInfo==None):
            logger.info("用户"+self.openidStr+"数据库中无成绩")
            #插入成绩 0表示插入
            TrueOrFalse=self.__updateScore(0)
            #如果插入失败
            if(TrueOrFalse==False):
                #失败次数+1
                self.count=self.count+1
                logger.warning("用户"+self.openidStr+"已爬"+str(self.count)+"次")
            #调用一次自身
            return self.selectScore()
        #如果数据库取出的成绩过期
        elif(self.__compareTime(scoreInfo.updateTime.date())==False):
            logger.info("用户"+self.openidStr+"使用爬虫爬取成绩")
            #更新 1表示更新
            TrueOrFalse=self.__updateScore(1)
            if(TrueOrFalse==False):
                #如果今天的成绩为空，更新失败，但是数据库原来有数据
                #直接取原来的数据库的数据
                logger.info("用户"+self.openidStr+"从数据库中取成绩")
                return scoreInfo.score
            else:
                #如果数据库跟新成功了，那就直接取数据库的
                return self.selectScore()
        else:
            logger.info("用户"+self.openidStr+"从数据库中取成绩")
            return scoreInfo.score


    # 插入成绩
    # 参数：成绩字符串
    # 返回值：
    # True：插入成功
    # False：插入失败


    def __insertScore(self,score_json):
        scoreInfo=Scores()
        scoreInfo.openid = self.openidStr
        scoreInfo.score = score_json
        scoreInfo.termStr = configfile.getConfig("term","termStr")
        try:
            self.session.add(scoreInfo)
            self.session.commit()
            logger.info("用户"+self.openidStr+"成绩插入成功")
            return True
        except:
            logger.info("用户"+self.openidStr+"成绩插入失败")
            return False

    #更新成绩
    # 参数：无
    # 返回值：
    # True：插入成功
    # False：插入失败

    def __updateScore(self,flag):
        user=UserDao()
        userInfo=user.selectUserInfoByOpenid(self.openidStr)
        username=userInfo[0]
        password=userInfo[1]
        user=Score(username,password)
        scoreStr=user.parseScorePage()
        if(scoreStr != None):
            if(flag==0):
                return self.__insertScore(scoreStr)
            else:
                scoreInfo= self.session.query(Scores).filter_by(openid=self.openidStr).first()
                scoreInfo.score=scoreStr
                scoreInfo.updateTime=datetime.datetime.now().date()
                self.session.commit()
                logger.info("用户"+self.openidStr+"成绩更新成功")
                return True
        else:
            logger.error("用户"+self.openidStr+"成绩查询失败")
            return False
