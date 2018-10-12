# -*- coding: utf-8 -*-
# @Project : WeChatPy 
# @Time    : 2018/10/12 10:51
# @Author  : 
# @File    : jieba_demo.py
# @Software: PyCharm
import jieba.posseg as psg

def parse_order_info(order_accept):
    ren_ming='init'
    for x in psg.cut(order_accept):
        # print(x.word, x.flag)
        if x.flag=='nr':
            ren_ming=x.word
    print(ren_ming,order_accept)


a='''湖南省株洲市醴陵市孙家湾乡陶润实业发展有限公司，曾祥，18692621360'''
b=',陈露,1件,深圳市罗湖区水贝二路27号；#15017902030,'
parse_order_info(b)