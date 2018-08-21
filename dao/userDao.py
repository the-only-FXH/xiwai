#!/usr/bin/env python3
# coding = utf-8
import sys

sys.path.append("..")
from tools.logger import logger 
from dao.model import User
from dao.engineAndSession import engine, Session

# 用户操作函数
class UserDao:
    def __init__(self):
        self.session = Session()
        self.user = User()

    # 查看该用户是否可以进行绑定
    def __selectUserFlag(self, opendiStr):
        self.user = self.session.query(User).filter_by(openid=opendiStr).first()
        if(self.user==None):
            logger.info("用户名 "+opendiStr+" 为空")
            return 1
        elif(self.user.flag==0):
            logger.info("用户名 "+opendiStr+" 以解绑")
            return 2
        else:
            logger.info("用户名 "+opendiStr+" 以绑定")
            return 3

    # 插入或者更新用户信息
    def insertOrUpdateUser(self, user):
        self.user.openid=user["openid"]
        self.user.username=user["username"]
        self.user.password=user["password"]
       
        flag=self.__selectUserFlag(self.user.openid)
        if(flag==1):
            self.session.add(self.user)
        elif(flag==2):
            self.user.flag=1
        else:
            logger.error("用户绑定失败")
            return False
        self.session.commit()
        logger.info("用户绑定成功")
        return True

    # 解除绑定
    def deleteUser(self, openidStr):
        flag=self.__selectUserFlag(openidStr)
        if(flag==3):
            self.user.flag=0
            self.session.commit()
            logger.error("用户解绑成功")
            return True
        else:
            logger.error("用户未绑定，无法解绑")
            return False

    def selectUserInfoByOpenid(self, openid):
        if(self.__selectUserFlag(openid)!=3):
            return None
        else:
            return(self.user.username,self.user.password)