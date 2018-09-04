# -*- coding: utf-8 -*-
# @Project : WeChatPy 
# @Time    : 2018/9/4 11:49
# @Author  : 
# @File    : chatroom_member_demo.py
# @Software: PyCharm

import itchat
from itchat.content import *

def get_chatroom_username(room_name):
    try:
        chatroomUserName=itchat.search_chatrooms(room_name)[0]['UserName']
        return  chatroomUserName
    except Exception as e:
        return


itchat.auto_login(hotReload=True)
memberList = itchat.update_chatroom(get_chatroom_username('13栋业主群'), detailedMember=True)
print(len(memberList))
print(memberList)
for x,y in memberList.items():
    # print(x,y)
    n=0
    if x=='MemberList':
        for z in y:
            # print(z['NickName'])
            n += 1
            for key,value in z.items():

                print(key,value)
            print('--'*10)
        print(n)
