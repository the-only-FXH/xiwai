import web
import hashlib
import lxml
import time
import os
import json
from wechat.type import Wechat
from dao.userDao import UserDao
from dao.scoreDao import ScoreDao
from spider.login import login
from lxml import etree
from wechat.binding import binding, postBindData
from wechat.selectScore import Score

Templates_Path = '/var/www/html/web/templates'
urls = (
	'/wx','wx',
	'/binding','binding',
	'/postBindData','postBindData',
	'/Score','Score'
	)

web.internalerror = web.debugerror

class wx(object):
	def GET(self):
		try:
			data = web.input()
			if len(data) == 0:
				return "hello, this is handle view"
			signature = data.signature
			timestamp = data.timestamp
			nonce = data.nonce
			echostr = data.echostr
			token = "weixin"	# 请按照公众平台官网\基本配置中信息填写
			list1 = [token,timestamp,nonce]
			list1.sort()
			str_list1 = ''.join(list1)
			print(str_list1)
			sha1 = hashlib.sha1()
			sha1.update(str_list1.encode('utf-8'))
			hashcode = sha1.hexdigest()
			print("handle/GET func: hashcode, signature: ", hashcode, signature)
			if hashcode == signature:
				return echostr
			else:
				return ""
		except Exception as Argument:
			return Argument

			
	def POST(self):
		str_xml = web.data()
		xml = etree.fromstring(str_xml)	
		mywechat = Wechat(xml)
		content =  mywechat.choose()
		print(content)
		return content
		

app = web.application(urls,globals())
