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
    name=Column(String(255),primary_key=True)
    order_num=Column(String(10))
    address=Column(String(255))
    accept_money=Column(String(10))
    if_send=Column(String(10))



def CreatDb():
    #创建表
    Base.metadata.create_all(engine)
def delDb():
    #删除表
    Base.metadata.drop_all(engine)

def add_data(name_string,order_num_string='',address_string='',accept_money_string='',if_send_string=''):
    _dt=Mybase(
        name=name_string,
        order_num=order_num_string,
        address=address_string,
        accept_money=accept_money_string,
        if_send=if_send_string
    )
    session.add(_dt)
    session.commit()

def update_data(filter_column,filter_data,update_column,update_data):
    _ModifyDt = session.query(Mybase).filter_by(filter_column=filter_data).first()
    _ModifyDt.update_column = update_data
    session.commit()

if __name__=="__main__":
    # delDb()
    # CreatDb()
    # add_data(name_string='rr')
    querydt = session.query(Mybase).filter()
    for i in querydt:
        print(i.name)