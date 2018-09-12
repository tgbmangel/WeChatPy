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
#定时给群消息发送消息。


def get_chatroom_username(room_name):
    try:
        chatroomUserName=itchat.search_chatrooms(room_name)[0]['UserName']
        return  chatroomUserName
    except Exception as e:
        return

def send_message_chatroom(message):
    '''
    定时任务
    '''
    print('send_message_chatroom')
    chat_room='人文-信计B-2006级1班同学群'
    itchat.send_image(message,toUserName=get_chatroom_username(chat_room))
    itchat.send('还没登记的同学快扫码登记哦！已登记的同学找刘乐领奖品哦。[害羞][愉快]',toUserName=get_chatroom_username(chat_room))

def schedule_send():
    print('start time:{}'.format(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime())))
    while True:
        schedule.run_pending()
        print('schedule_send...')
        time.sleep(20)

@itchat.msg_register(itchat.content.TEXT)
def print_msg(msg):
    print(msg.text)
if __name__=='__main__':
    itchat.auto_login(hotReload=True)
    filepath=r'D:\\we.jpg'
    #定时任务demo
    # schedule.every().day.at("17:07").do(send_message_chatroom, filepath)
    # schedule.every(1).minutes.do(send_message_chatroom, filepath)
    # schedule.every().hour.do(send_message_chatroom, filepath)
    schedule.every(3).hours.do(send_message_chatroom, filepath)
    # schedule.every().day.at("10:30").do(job)
    # schedule.every().monday.do(job)
    # schedule.every().wednesday.at("13:15").do(job)
    #启动时发送一次
    # send_message_chatroom(filepath)
    t=threading.Thread(target=schedule_send)
    t.start()
    itchat.run()
