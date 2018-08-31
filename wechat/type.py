import web
import hashlib
import lxml
import time
import os
from dao.userDao import UserDao
from wechat.xmlTemplate import Template
from config import configfile
from dao.keyWordDao import keyWordDao
Templates_Path = configfile.getConfig("web","Templates_Path")

class Wechat(object):
	"""docstring for wechat"""
	def __init__(self, xml):
		self.xml = xml
		
	def choose(self):
		msgType = self.xml.find("MsgType").text
		if msgType == 'event':
			keyword =  self.event()
		elif msgType == 'text':
			keyword =  self.xml.find("Content").text
		else:
			keyword = "else"
		
		#去掉空格
		keyword = keyword.strip()
		if keyword != "":
			resultKey=keyWordDao().selectkeyword(keyword)
			print(resultKey)
			if(resultKey!=False):
				content=self.contentRecv(resultKey)
			else:
				print("nope")
				return ""

			retXML = Template.returnTextXML(self.xml,content)
			return retXML
	
	def event(self):
		xml = self.xml
		event = xml.find("Event").text
		if event=="subscribe":
			return "subscribe"
		elif event == "CLICK":
			return xml.find("EventKey").text
		else:
			return  "else"

	def contentRecv(self,data):
		type = data["type"]
		print(type)
		if type=="text":
			return data["result"]
		elif type == "function":
			functionName = data["result"]
			if functionName == 'selectScore':
				data =  self.chengji()
				return data
			elif functionName == 'add':
				data = self.bangding()
				return data
			elif functionName == 'delete':
				data = self.jiebang()
				return data
			else:
				return ""


	def jiebang(self):
		xml = self.xml
		fromUser = xml.find("FromUserName").text
		user = UserDao()
		flag=user.deleteUser(fromUser)
		if(flag==True):
			resultStr='解绑成功'
		else:
			resultStr='解绑失败，您未绑定'
		return resultStr

	def bangding(self):
		xml = self.xml
		fromUser = xml.find("FromUserName").text
		user = UserDao()
		flag=user.selectUserFlag(fromUser)
		if(flag!=3):
			data = "<a href='http://xiwai.chdbwtx.cn/binding?openid=%s'>绑定</a>"%fromUser
		else:
			userInfo=user.selectUserInfoByOpenid(fromUser)
			username=userInfo[0]
			password=userInfo[1]
			data='您已绑定,您的绑定信息为\n用户名：{username}\n密  码：{password}'.format(username=username,password=password)
		return data
		


	def chengji(self):
		xml = self.xml
		fromUser = xml.find("FromUserName").text
		user = UserDao()
		flag=user.selectUserFlag(fromUser)
		if(flag==3):
			data = "<a href='http://xiwai.chdbwtx.cn/Score?openid=%s'>详细成绩</a>"%fromUser
		else:
			data='您未绑定'
		return data
		
