# -*- coding: utf-8 -*-
# @Project : WeChatPy 
# @Time    : 2018/9/4 11:49
# @Author  : 
# @File    : chatroom_member_demo.py
# @Software: PyCharm

import itchat
from itchat.content import *
import csv
import pandas as pd
import time

def get_chatroom_username(room_name):
    try:
        chatroomUserName=itchat.search_chatrooms(room_name)[0]['UserName']
        return  chatroomUserName
    except Exception as e:
        return


def qun():
    tongxuequn = '人文-信计B-2006级1班同学群'
    jinjiqun = '打开'
    memberList = itchat.update_chatroom(get_chatroom_username(jinjiqun), detailedMember=True)
    # print(len(memberList))
    # print(memberList)
    sexy = {1: '男',
            2: '女',
            0: '其他'}
    gender = []
    members = []
    for x, y in memberList.items():
        # 打印群内所有信息
        print(x, y)
        n = 0
        if x == 'MemberList':
            for z in y:
                # '''[z['UserName'],sexy[z['Sex']] ,z['Province'],z['City']]'''
                print(z['NickName'], z['DisplayName'], z['Province'], z['City'])
                itchat.send('@%s\u2005你好'%z['NickName'], toUserName=get_chatroom_username(jinjiqun))
                time.sleep(0.5)
                n += 1
                # 添加性别信息
                # gender.append(sexy[z['Sex']])
                # 打印出当前群内所有个人信息
                for key,value in z.items():
                    print(key,value)
                print('--' * 10)
            print(n)

            # print('\u2005')


def show():
    pass
    # male=[m for m in gender if m=='男']
    # female=[m for m in gender if m=='女']
    # df=pd.DataFrame({'male':male,'female':female},index=['male','female'])
    # df.plot(kind='bar')
    # df.show()
@itchat.msg_register(TEXT,isGroupChat=True)
def print_msg(msg):
    if msg['FromUserName']==get_chatroom_username('打开'):
        print(msg.keys())
        print(dir(msg))
        msg.user.send(u'@%s\u2005I received: %s' % (msg.actualNickName, msg.text))


if __name__=="__main__":
    itchat.auto_login(hotReload=True)
    qun()


