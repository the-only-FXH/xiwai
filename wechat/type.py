import web
import hashlib
import lxml
import json
import time
import os
from dao.userDao import UserDao
from dao.scoreDao import ScoreDao
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
		event = self.xml.find("Event").text
		if event=="subscribe":
			return "subscribe"
		elif event == "CLICK":
			return self.xml.find("EventKey").text
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
		fromUser = self.xml.find("FromUserName").text
		user = UserDao()
		flag=user.deleteUser(fromUser)
		if(flag==True):
			resultStr='解绑成功'
		else:
			resultStr='解绑失败，您未绑定'
		return resultStr

	def bangding(self):
		fromUser = self.xml.find("FromUserName").text
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
		fromUser = self.xml.find("FromUserName").text
		user = UserDao()
		flag=user.selectUserFlag(fromUser)
		if(flag!=3):
			data='您未绑定'
			return data
		score = ScoreDao(fromUser)
		scoreStr=score.selectScore()
		# 调取后台接口，获取成绩的数据
		if(scoreStr==2):
			data='网络繁忙，稍后再试'
			return data
		else:
			data = ''
			jidian=0.0
			datascore=json.loads(scoreStr)
			for score in datascore:
				jidian+=float(score['jidian'])
				data += score['name']+":\n"+\
				"成绩："+score['zuizhong']+"\n\n"
			data+="平均绩点："+str(round(jidian/len(datascore),1))+"\n"
			data+="<a href='http://xiwai.chdbwtx.cn/Score?openid=%s'>详细成绩</a>"%fromUser
			return data
		# if(flag==3):
		# 	data = "<a href='http://xiwai.chdbwtx.cn/Score?openid=%s'>详细成绩</a>"%fromUser
		# else:
		# 	data='您未绑定'
		# return data
		
