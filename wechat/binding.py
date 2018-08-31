import web
from config import configfile
from dao.userDao import UserDao
from spider.login import login

class binding(object):
	"""docstring for bang"""
	def GET(self):
		getData = web.input()
		render = web.template.render(configfile.getConfig("web","Templates_Path"))
		name = getData['openid']
		user=UserDao()
		flag=user.selectUserFlag(name)
		if(flag==3):
			errMsg='您已绑定'
			return render.error(errMsg)
		return render.bangding(name)
		# print(name)
	#def POST(self):
	#	postData = web.input()
	#	print(postData)

class postBindData(object):
	"""docstring for """
	def POST(self):
		postData = web.input()
		username=postData["username"]
		password=postData["password"]
		log=login(username,password)
		loginResult=log.main()
		
		# 调后台接口
		# 返回值为bool型变量判断是否绑定成功
		#flag = False  
		render = web.template.render(configfile.getConfig("web","Templates_Path"))

		if(loginResult==None):
			errMsg= "用户名和密码可能错误"
			return render.error(errMsg)
		else:
			binding = UserDao()
			flag=binding.insertOrUpdateUser(postData)

			if flag:
				return render.success()
			else:
				errMsg = "用户已绑定"
				return render.error(errMsg)