# -*- coding: utf-8 -*-
# @Project : WeChatPy 
# @Time    : 2018/9/4 11:49
# @Author  : 
# @File    : chatroom_member_demo.py
# @Software: PyCharm

import itchat
from itchat.content import *
import csv

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
csvFile2 = open('csvFile2.csv','w', newline='') # 设置newline，否则两行之间会空一行
writer = csv.writer(csvFile2)
sexy={1:'男',
      2:'女',
      0:'其他'}
for x,y in memberList.items():
    print(x,y)
    n=0
    if x=='MemberList':
        for z in y:
            # print(z['NickName'])
            writer.writerow([z['UserName'],sexy[z['Sex']] ,z['Province'],z['City']])
            n += 1
            for key,value in z.items():

                print(key,value)
            print('--'*10)
        print(n)
csvFile2.close()