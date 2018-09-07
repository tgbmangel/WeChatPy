# -*- coding: utf-8 -*-
# @Project : WeChatPy 
# @Time    : 2018/8/10 16:41
# @Author  : 
# @File    : message_demo.py
# @Software: PyCharm

import itchat
from itchat.content import *

@itchat.msg_register
def general_reply(msg):
    print( 'I received a %s' % msg.type)
@itchat.msg_register(TEXT)
def text_reply(msg):
    print( 'You said to me one to one: %s' % msg.type)
itchat.auto_login(hotReload=True)
itchat.run()