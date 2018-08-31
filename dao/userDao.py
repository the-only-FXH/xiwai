#!/usr/bin/env python3
# coding = utf-8
import sys

sys.path.append("..")
from tools.logger import logger 
from dao.model import User,engine, Session
from spider.login import login
from sqlalchemy.sql import text
# 用户操作函数
class UserDao:
    def __init__(self):
        #session初始化
        self.session = Session()

    # 查看该用户是否可以进行绑定
    # 参数：openid
    # 返回值：
    # 1：用户名为空
    # 2：用户已解绑
    # 3：用户已绑定

    def selectUserFlag(self, opendiStr):
        dbconnect=engine.connect()
        result=dbconnect.execute(text('select flag from user where openid=:openid'), openid=opendiStr)
        if(result.rowcount<=0):
            logger.info("用户名 "+opendiStr+" 为空")
            return 1
        ru = result.fetchall()[0][0]
        if(ru==True):
            logger.info("用户名 "+opendiStr+" 以绑定")
            return 3
        elif(ru==False):
            logger.info("用户名 "+opendiStr+" 以解绑")
            return 2

    # 插入或者更新用户信息
    # 参数：user 是个map
    # 返回值：
    # False:用户绑定失败
    # True:用户绑定成功

    def insertOrUpdateUser(self, usermap):
        
        session=Session()
        user=User()
        user.openid=usermap["openid"]
        user.username=usermap["username"]
        user.password=usermap["password"]

        flag=self.selectUserFlag(user.openid)
        if(flag==1):
            try:
                session.add(user)
                session.commit()
                logger.info("用户"+user.openid+"用户绑定成功")
                return True
            except:
                logger.error("用户"+user.openid+"用户绑定失败")
                return False
        elif(flag==2):
            try:
                user= session.query(User).filter_by(openid=user.openid).first()
                user.username=usermap["username"]
                user.password=usermap["password"]
                user.flag=1
                session.commit()
                logger.info("用户"+user.openid+"用户更新成功")
                return True
            except:
                logger.error("用户"+user.openid+"用户绑定失败")
                return False
        else:
            logger.error("用户"+user.openid+"用户绑定失败")
            return False
        
        

    # 解除绑定
    # 参数：openid
    # 返回值：
    # True：用户解绑成功
    # False:用户解绑失败

    def deleteUser(self, openidStr):
        session=Session()
        flag=self.selectUserFlag(openidStr)
        if(flag==3):
            user = session.query(User).filter_by(openid=openidStr).first()
            user.flag=0
            session.commit()
            logger.info("用户"+openidStr+"解绑成功")
            return True
        else:
            logger.error("用户"+openidStr+"未绑定，无法解绑")
            return False
    
    #使用openid查询用户信息，scoreDao中使用
    # 参数：openid
    # 返回值：None User

    def selectUserInfoByOpenid(self,openid):
        if(self.selectUserFlag(openid)!=3):
            return None
        else:
            user = self.session.query(User).filter_by(openid=openid).first()
            return(user.username,user.password)


#a=UserDao() 
# data={
#    "openid":"o1X941FLNbaeLKKLwQjfYcR243aA",
#    "username":"107242017000646",
#    "password":"107242017000646"
# }

#print(a.selectUserFlag("o1X941FLNbaeLKKLwQjfYcR243aA"))
# a=UserDao()
#print(a.deleteUser('o1X941FLNbaeLKKLwQjfYcR243aA'))
