import web
import json
from config import configfile
from dao.userDao import UserDao
from spider.login import login
from dao.scoreDao import ScoreDao

class Score(object):
	"""docstring for detail"""
	def GET(self):
		render = web.template.render(configfile.getConfig("web","Templates_Path"))
		getData = web.input()
		openid = getData['openid']

		user=UserDao()
		flag=user.selectUserFlag(openid)
		if(flag!=3):
			errMsg='您未绑定'
			return render.error(errMsg)
		score = ScoreDao(openid)
		scoreStr=score.selectScore()
		# 调取后台接口，获取成绩的数据
		if(scoreStr==2):
			errMsg='网络繁忙，稍后再试'
			return render.error(errMsg)
		else:
			data=json.loads(scoreStr)
		# data = [
		# 	{
		# 		'name':'数学',
		# 		'zuizhong':'89',
		# 		'xuefen':'2.1',
		# 		'jidian':'254'

		# 	},
		# 	{
		# 		'name':'数学',
		# 		'zuizhong':'89',
		# 		'xuefen':'2.1',
		# 		'jidian':'254'

		# 	}
		# ]
			return render.detail(data)