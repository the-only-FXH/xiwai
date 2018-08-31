import requests
import json
appId = "wx389123a9abcdaa54"
appSecret = "b037845a0dea69eb9d062bbcb6c1e7ab"


def token():
    
    url = 'https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=%s&secret=%s'%(appId, appSecret)
    urlResp = requests.get(url)   
    urlResp = json.loads(urlResp.text)   
    # urlResp = json.loads(urlResp.read())
    return urlResp.get('access_token')

class Menu(object):
    def __init__(self):
        pass
    def create(self, postData, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/create?access_token=%s" % accessToken
        postData = json.dumps(postData,ensure_ascii=False)
        postData = postData.encode('utf-8')
        request = requests.session()
        req = request.post(postUrl,data=postData)
        print(req.text)

    def query(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/get?access_token=%s" % accessToken
        urlResp = urllib.urlopen(url=postUrl)
        print(urlResp.read()) 

    def delete(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/menu/delete?access_token=%s" % accessToken
        urlResp = urllib.urlopen(url=postUrl)
        print (urlResp.read())
        print("sds")

    #获取自定义菜单配置接口
    def get_current_selfmenu_info(self, accessToken):
        postUrl = "https://api.weixin.qq.com/cgi-bin/get_current_selfmenu_info?access_token=%s" % accessToken
        urlResp = urllib.urlopen(url=postUrl)
        print (urlResp.read())

if __name__ == '__main__':
    myMenu = Menu()
    postJson ={
            "button":
            [

                {
                    "name":"成绩查询",
                    "sub_button":[
                        {
                            "type":"click",
                            "name":"绑定用户",
                            "key":"绑定用户"
                        },
                        {
                            "type":"click",
                            "name":"解绑用户",
                            "key":"解绑用户"
                        },
                        {
                            "type":"click",
                            "name":"成绩查询",
                            "key":"成绩查询"
                        }
                    ]
                    
                }
                
            ]

        }


    # {
    #     "button":
    #     [
    #         {
    #             "type": "click",
    #             "name": "开发指引",
    #             "key":  "mpGuide"
    #         },
    #         {
    #             "name": "公众平台",
    #             "sub_button":
    #             [
    #                 {
    #                     "type": "view",
    #                     "name": "更新公告",
    #                     "url": "http://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1418702138&token=&lang=zh_CN"
    #                 },
    #                 {
    #                     "type": "view",
    #                     "name": "接口权限说明",
    #                     "url": "http://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1418702138&token=&lang=zh_CN"
    #                 },
    #                 {
    #                     "type": "view",
    #                     "name": "返回码说明",
    #                     "url": "http://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1433747234&token=&lang=zh_CN"
    #                 }
    #             ]
    #         },
    #         {
    #             "type": "view",
    #             "name": "返回码说明",
    #             "url": "http://mp.weixin.qq.com/wiki?t=resource/res_main&id=mp1433747234&token=&lang=zh_CN"
    #         }
    #       ]
        # }
    accessToken = token()
    # print(accessToken)
    #myMenu.delete(accessToken)
    myMenu.create(postJson, accessToken)
