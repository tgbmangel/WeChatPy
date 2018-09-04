# -*- coding: utf-8 -*-
# @Time    : 2018/9/4 22:55
# @Author  : 
# @File    : Orange.py
# @Software: PyCharm Community Edition

import itchat
from itchat.content import *
import re

orange_msg_type = {
    -1:'no',
    1:'买橘子',
    2:'重量',
    3:'地址',
    4:'查询'
}

def get_content(content):
    print('content',content)
    #替换掉收到的信息中的一些符号
    string_c = re.sub("[\s+\.\!\/_,$%^*(\"\'\:\：\;\；]+|[+—！，。？、~@#￥%&*（）]+", "",content)
    org_compile=re.compile(r"^我要买橘子(.*)")
    dingdan_compile=re.compile(r"^订单(.*)")
    dizhi_compile=re.compile(r"^配送地址(.*)")
    chaxun=re.compile(r"^查询订单(.*)")

    #返回有一个列表
    a=org_compile.findall(string_c)
    b=dingdan_compile.findall(string_c)
    c=dizhi_compile.findall(string_c)
    d=chaxun.findall(string_c)
    if a:
        return 1
    elif b:
        return 2
    elif c:
        return 3
    elif d:
        return 4
    else:
        return -1

def send_msg_to_man(message):
    a=itchat.search_friends(name='西边有片云')
    print(a[0]['UserName'])
    itchat.send_msg(message,toUserName=a[0]['UserName'])

msg_turn={}
def parse_msg_turn(msg_t):
    msg_toman = ''
    for x in msg_t:
        msg_toman += msg_toman
        for y in msg_t[x]:
            msg_toman += y
    return msg_toman

@itchat.msg_register(FRIENDS)
def add_friend(msg):
    msg.user.verify()
    msg.user.send('您好！发送："我要买橘子"，将有客服为您转接！')



@itchat.msg_register([TEXT, MAP, CARD, NOTE, SHARING])
def text_reply(msg):
    print(msg.text)
    if msg.text:
        print(msg)
        msg_turn[msg['User']['NickName']]=[]
        wechat_content = msg.text
        msg_orange=get_content(wechat_content)
        if msg_orange==1:
            msg.user.send('请说明要多少，目前1件10斤，50元，发送格式：【订单+几件】')
        elif msg_orange==2:
            msg_turn[msg['User']['NickName']].append(wechat_content)
            msg.user.send('已收到订单信息:{}'.format(msg.text))
            msg.user.send('请发出您的姓名、地址和联系电话。格式：【配送地址+您的姓名，地址，联系电话】')
        elif msg_orange==3:
            msg_turn[msg['User']['NickName']].append(wechat_content)
            msg.user.send('已收到地址信息:{} \n---\n谢谢，稍后会联系您。'.format(msg.text))

            send_msg_to_man(parse_msg_turn(msg_turn))
        elif msg_orange==4:
            msg.user.send(parse_msg_turn(msg_turn))
        elif msg_orange==-1:
            msg.user.send('谢谢关注，买橘子请发：我要买橘子')


itchat.auto_login(True)
itchat.run()

