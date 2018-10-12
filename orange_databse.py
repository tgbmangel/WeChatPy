# -*- coding: utf-8 -*-
# @Project : WeChatPy 
# @Time    : 2018/9/6 9:53
# @Author  : 
# @File    : orange_databse.py
# @Software: PyCharm

from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine,Column,String,Integer

engine=create_engine('sqlite:///db/orange.sqlite3',echo=True)
DBSession = sessionmaker(bind=engine)
session = DBSession()
Base=declarative_base()

class Mybase(Base):
    #表名:

    __tablename__ ='orange_order'
    #字段，属性
    id=Column(Integer,primary_key=True)
    name=Column(String(255))
    order_num=Column(String(10))
    address=Column(String(255))
    accept_money=Column(String(10))
    if_send=Column(String(10))
    info=Column(String(100))




def CreatDb():
    #创建表
    Base.metadata.create_all(engine)
def delDb():
    #删除表
    Base.metadata.drop_all(engine)

def add_data(name_string,order_num_string='',address_string='',accept_money_string='',if_send_string='',info_string=''):
    _dt=Mybase(
        name=name_string,
        order_num=order_num_string,
        address=address_string,
        accept_money=accept_money_string,
        if_send=if_send_string,
        info=info_string
    )
    session.add(_dt)
    session.commit()

def query_all():
    _all_datas = session.query(Mybase).all()
    # print(_all_datas)
    n=0
    _all_datas_msg_string=''
    for r in _all_datas:
        if r.order_num:
            n+=1
            row_string=f'{r.id},{r.name},{r.order_num},{r.address},\n下单时间:{r.accept_money},{"已发" if r.if_send else "未发"},\n备注:{r.info if r.info else "无"}\n------\n'
            _all_datas_msg_string+=row_string
    _all_datas_msg_string=_all_datas_msg_string+f'\n共 {n} 个订单'
    return _all_datas_msg_string

def query_not_send():
    _all_datas = session.query(Mybase).filter_by(if_send='').all()
    _all_datas_msg_string=[]
    for r in _all_datas:
        if r.order_num:
            row_string=f'{r.id},{r.name},{r.order_num},{r.address},\n下单时间:{r.accept_money},{"已发" if r.if_send else "未发"},\n备注:{r.info if r.info else "无"}'
            _all_datas_msg_string.append(row_string)
    return _all_datas_msg_string

def filter_id(id):
    '''
    数据库中按照名字过滤，如果已存在，则直接返回查询结果
    然后通过以下方式修改对应的数据：
    filter_name(msg_nick_name).address = chat_msg.text
    :param name: 微信昵称
    :return:
    '''
    _ModifyDt = session.query(Mybase).filter_by(id=id).first()
    return _ModifyDt

def filter_name(name):
    '''
    数据库中按照名字过滤，如果已存在，则直接返回查询结果
    然后通过以下方式修改对应的数据：
    filter_name(msg_nick_name).address = chat_msg.text
    :param name: 微信昵称
    :return:
    '''
    _ModifyDt = session.query(Mybase).filter_by(name=name).first()
    return _ModifyDt

def delete_by_id(id):
    session.query(Mybase).filter_by(id=id).delete()
    session.commit()
def update_data(filter_column,filter_data,update_column,update_data):
    _ModifyDt = session.query(Mybase).filter_by(filter_column=filter_data).first()
    _ModifyDt.update_column = update_data
    session.commit()

if __name__=="__main__":
    # delDb()
    # CreatDb()
    # # add_data(name_string='rr')
    # querydt = session.query(Mybase).filter()
    # for i in querydt:
    #     print(i.name)
    for x in query_not_send():
        print(x)