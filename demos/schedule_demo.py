# -*- coding: utf-8 -*-
# @Project : WeChatPy 
# @Time    : 2018/9/7 15:21
# @Author  : 
# @File    : schedule_demo.py
# @Software: PyCharm

import schedule
import itchat
import time
import threading

def get_chatroom_username(room_name):
    try:
        chatroomUserName=itchat.search_chatrooms(room_name)[0]['UserName']
        return  chatroomUserName
    except Exception as e:
        return

def send_message_chatroom(message):
    print('send_message_chatroom')
    itchat.send(message,toUserName=get_chatroom_username('经济研讨'))

def schedule_send():
    while True:
        schedule.run_pending()
        print('schedule_send...')
        time.sleep(1)

@itchat.msg_register(itchat.content.TEXT)
def print_msg(msg):
    print(msg.text)
if __name__=='__main__':
    itchat.auto_login(hotReload=True)

    schedule.every().day.at("17:07").do(send_message_chatroom, "哈哈")
    t=threading.Thread(target=schedule_send)
    t.start()
    itchat.run()
