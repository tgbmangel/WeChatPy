# -*- coding: utf-8 -*-
# @Time    : 2018/9/4 22:55
# @Author  : 
# @File    : Orange.py
# @Software: PyCharm Community Edition

import itchat
from itchat.content import *
import re
from orange_databse import *
from orange_log import logger
import schedule
import time

ora=itchat.new_instance()
MSG_TURN={}
orange_info='正宗石门柑橘，自家种的新鲜橘子，一件10斤50元包邮。'
main_wechat_name='西边有片云'

def get_content(content):
    #替换掉收到的信息中的一些符号
    string_c = re.sub("[\s+_,$%^*(\"\']+|[+—！，。？、~@#￥%&*（）]+", "",content)
    org_compile=re.compile(r"^我要买橘子(.*)")
    dingdan_compile=re.compile(r"^我要订(.*)")
    dizhi_compile=re.compile(r"^配送信息(.*)")
    chaxun=re.compile(r"^查询订单(.*)")
    chaxun_not=re.compile(r"^查询未发订单(.*)")
    dingdanjilu=re.compile(r"^-(.*)")
    xiugai=re.compile(r"^已发(.*)")
    shanchu = re.compile(r"^删除(.*)")

    #返回有一个列表
    a=org_compile.findall(string_c)
    b=dingdan_compile.findall(string_c)
    c=dizhi_compile.findall(string_c)
    d=chaxun.findall(string_c)
    e=dingdanjilu.findall(string_c)
    f=chaxun_not.findall(string_c)
    g=xiugai.findall(string_c)
    h=shanchu.findall(string_c)
    if a:
        return 1
    elif b:
        return 2
    elif c:
        return 3
    elif d:
        return 4
    elif e:
        return 5
    elif f:
        return 6
    elif g:
        return 7
    elif h:
        return 8
    else:
        return -1

def send_msg_to_man(message):
    a=ora.search_friends(name=main_wechat_name)
    ora.send_msg(message,toUserName=a[0]['UserName'])

def parse_msg_turn(msg_t):
    msg_toman = ''
    for x,y in msg_t.items():
        msg_toman += '已收到订单：\n微信：{},'.format(x)
        for key,value in y.items():
            # msg_toman += key
            print(key,value)
            msg_toman += '{},'.format(value)
        msg_toman+='↓\n'
    return msg_toman

def unicode_nickname(input_string):
    '''
    微信的昵称或者备注名，有时候带有一些表情，写文件或者存数据库时会报错，此函数处理
    不记得处理的数据原型了。但是函数应该可以用（忘记当时实现过程很尴尬）
    如：数据原型为：\\U0008928\\02992\\0923
        那么处理过程取出U0008928 、02992、0923
        去掉U000开头的，然后将正常的拼回去组成一个string
        再通过encode('utf-8').decode('unicode_escape') 处理成正常的utf8
    '''
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

def orange_replay(chat_msg):
    # print(msg['MsgType'])
    if chat_msg.text:
        # print(msg)
        global MSG_TURN
        try:
            msg_nick_name = unicode_nickname(chat_msg['User']['NickName'])
            if not filter_name(msg_nick_name):
                add_data(name_string=msg_nick_name)
            if msg_nick_name in MSG_TURN.keys():
                pass
            else:
                MSG_TURN[msg_nick_name] = {}
            wechat_content = chat_msg.text
            msg_orange = get_content(wechat_content)
            logger.info('{}:{}'.format(msg_nick_name, chat_msg.text))
            if msg_orange == 1:
                chat_msg.user.send('亲，请说明要多少，目前1件10斤，50元，发送格式：\n【我要订 几件】')
            elif msg_orange == 2:
                MSG_TURN[msg_nick_name]['dingdan'] = wechat_content
                # print(msg_turn)
                chat_msg.user.send('已收到:{}'.format(chat_msg.text))
                filter_name(msg_nick_name).order_num = chat_msg.text
                time.sleep(0.5)
                chat_msg.user.send('亲，把您的收件人名、地址和联系电话发给我哦。格式：\n【配送信息 收件人姓名，地址，联系电话】')
            elif msg_orange == 3:
                MSG_TURN[msg_nick_name]['dizhi'] = wechat_content
                # print(msg_turn)
                chat_msg.user.send('亲，已收到:{} \n----\n谢谢，稍后会联系您。[愉快]'.format(chat_msg.text))
                filter_name(msg_nick_name).accept_money = time.strftime("%Y-%m-%d", time.localtime())
                filter_name(msg_nick_name).address = chat_msg.text
                send_msg_to_man(parse_msg_turn(MSG_TURN))
            elif msg_orange == 4:
                #查询所有：查询订单
                chat_msg.user.send(query_all())
            elif msg_orange == 6:
                #查询未发订单：查询未发订单
                all_not_send=query_not_send()
                for x in all_not_send:
                    time.sleep(1)
                    chat_msg.user.send(x)
                chat_msg.user.send(f'共有 {len(all_not_send)} 个订单未发')
            elif msg_orange==5:
                #添加数据：-
                order_msg=chat_msg.text[1:]
                print(order_msg)
                chat_msg.user.send(f'已收到:{order_msg}')
                try:
                    order_msg_get=re.split('[，。,. \t\s\n]',order_msg)
                    order_msg_get=[x for x in order_msg_get if not x=='']
                    order_addre, order_name, order_phone,*_other_msg=order_msg_get
                    if len(_other_msg)==1:
                        order_num=_other_msg[0]
                        order_beizhu='无'
                    elif len(_other_msg)==2:
                        order_num, order_beizhu=_other_msg
                    elif len(_other_msg)>2:
                        order_num, order_beizhu ,*_= _other_msg
                    else:
                        order_num, order_beizhu = '1件', '无'
                    order_address=f'{order_addre}#{order_phone}'
                    order_time=time.strftime("%Y-%m-%d", time.localtime())
                    print(f'添加数据：name_string={order_name},order_num_string={order_num},address_string={order_address},accept_money_string={order_time},info_string={order_beizhu})')
                    logger.info(f'添加数据：name_string={order_name},order_num_string={order_num},address_string={order_address},accept_money_string={order_time},info_string={order_beizhu}')
                    add_data(name_string=order_name,order_num_string=order_num,address_string=order_address,accept_money_string=order_time,info_string=order_beizhu)
                    chat_msg.user.send('数据添加成功。')
                except Exception as e:
                    logger.error(e)
                    chat_msg.user.send(e)
            elif msg_orange==7:
                #修改数据：已发
                send_id=chat_msg.text[2:]
                print('收到id',send_id)
                logger.info(f'修改：{int(send_id.strip())}')
                filter_id(int(send_id.strip())).if_send = '1'
                chat_msg.user.send(f'已修改{int(send_id.strip())}')
            elif msg_orange==8:
                #删除：删除
                send_id = chat_msg.text[2:]
                print('收到id', send_id)
                logger.info(f'删除：{int(send_id.strip())}')
                delete_by_id(int(send_id.strip()))
                chat_msg.user.send(f'已删除{int(send_id.strip())}')
            elif msg_orange == -1:
                chat_msg.user.send('谢谢关注，{}买橘子请发：\n【我要买橘子】\n'.format(orange_info))
            session.commit()
        except Exception as e:
            print('异常打印：{}:{}'.format(e, chat_msg))
            logger.error('异常打印：{}:{}'.format(e, chat_msg))

@ora.msg_register(FRIENDS)
def add_friend(msg):
    msg.user.verify()
    print('{}添加成功'.format(msg.user))
    msg.user.send('亲！您好！发送：【我要买橘子】，将有客服为您转接！\n{}'.format(orange_info))

@ora.msg_register([TEXT])
def text_reply(msg):
    orange_replay(msg)

@ora.msg_register(TEXT,isGroupChat=True)
def text_group_chat(msg):
    logger.info(msg['MsgType'])
    logger.info(msg.content)

if __name__=='__main__':


    ora.auto_login(hotReload=True,statusStorageDir='ora.pkl')
    try :
        ora.run()
    except Exception as e:
        logger.info(e)

