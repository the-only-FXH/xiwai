#!/usr/bin/env python3
# coding = utf-8

import time


class Template:

    @staticmethod
    def returnTextXML(xml,content):
        fromUser = xml.find("FromUserName").text
        toUser = xml.find("ToUserName").text
        returnXML = """	<xml>
				<ToUserName><![CDATA[%s]]></ToUserName>
				<FromUserName><![CDATA[%s]]></FromUserName>
				<CreateTime>%d</CreateTime>
				<MsgType><![CDATA[text]]></MsgType>
				<Content><![CDATA[%s]]></Content>
				</xml>"""%(fromUser,toUser,int(time.time()),content)
        return returnXML


