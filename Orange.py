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
    string_c = re.sub("[\s+_,$%^*(\"\']+|[+—！，。？、~@#￥%&*（）]+", "",content)
    org_compile=re.compile(r"^我要买橘子(.*)")
    dingdan_compile=re.compile(r"^我要订(.*)")
    dizhi_compile=re.compile(r"^配送信息(.*)")
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
    itchat.send_msg(message,toUserName=a[0]['UserName'])

msg_turn={}
def parse_msg_turn(msg_t):
    msg_toman = ''
    for x,y in msg_t.items():
        msg_toman += '\n微信：{}，'.format(x)
        for key,value in y.items():
            # msg_toman += key
            print(key,value)
            msg_toman += '{},'.format(value)
    print('msg:',msg_toman)
    return msg_toman

def unicode_nickname(input_string):
    strrr=ascii(input_string)
    b=''
    if 'U000' in strrr:
        str_list = strrr.split('\'')[1].split('\\')
        for x in str_list:
            if 'U000' in x:
                pass
            elif not x:
                pass
            else:
                a = '\\{}'.format(x)
                b=b+a
        final_str=b.encode('utf-8').decode('unicode_escape')
        return final_str
    else:
        return input_string

orange_info='正宗石门柑橘，自家种的，一件10斤50元。目前是特早熟，现摘现卖。'

@itchat.msg_register(FRIENDS)
def add_friend(msg):
    msg.user.verify()

    msg.user.send('亲！您好！发送："我要买橘子"，将有客服为您转接！\n{}'.format(orange_info))

@itchat.msg_register([TEXT])
def text_reply(msg):
    print(msg.text)
    if msg.text:
        print(msg)
        global msg_turn
        msg_nick_name=unicode_nickname(msg['User']['NickName'])
        if msg_nick_name in msg_turn.keys():
            pass
        else:
            msg_turn[msg_nick_name]={}
        wechat_content = msg.text
        msg_orange=get_content(wechat_content)
        if msg_orange==1:
            msg.user.send('亲，请说明要多少，目前1件10斤，50元，发送格式：【我要订+几件】')
        elif msg_orange==2:
            msg_turn[msg_nick_name]['dingdan']=wechat_content
            print(msg_turn)
            msg.user.send('已收到:{}'.format(msg.text))
            msg.user.send('亲，把您的收件人名、地址和联系电话发给我哦。格式：【配送信息+收件人姓名，地址，联系电话】')
        elif msg_orange==3:
            msg_turn[msg_nick_name]['dizhi']=wechat_content
            print(msg_turn)
            msg.user.send('亲，已收到:{} \n---\n谢谢，稍后会联系您。[愉快]'.format(msg.text))
            send_msg_to_man(parse_msg_turn(msg_turn))
        elif msg_orange==4:
            msg.user.send(parse_msg_turn(msg_turn))
        elif msg_orange==-1:
            msg.user.send('谢谢关注，买橘子请发：“我要买橘子”。。\n{}'.format(orange_info))


itchat.auto_login(True)
itchat.run()

