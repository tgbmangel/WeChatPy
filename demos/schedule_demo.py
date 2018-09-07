# -*- coding: utf-8 -*-
# @Project : WeChatPy 
# @Time    : 2018/9/7 15:21
# @Author  : 
# @File    : schedule_demo.py
# @Software: PyCharm

import schedule
import itchat
import time

def get_chatroom_username(room_name):
    try:
        chatroomUserName=itchat.search_chatrooms(room_name)[0]['UserName']
        return  chatroomUserName
    except Exception as e:
        return


def send_message_chatroom(message):
    itchat.send(message,toUserName=get_chatroom_username('经济研讨'))

itchat.auto_login(hotReload=True)
schedule.every().day.at("15:35").do(send_message_chatroom, "哈哈",)
while True:
    print('itchat:{}'.format(itchat.check_login()))
    schedule.run_pending()
    time.sleep(10)