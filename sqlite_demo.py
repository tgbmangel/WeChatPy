# -*- coding: utf-8 -*-
# @Project : WeChatPy 
# @Time    : 2018/9/5 9:05
# @Author  : 
# @File    : sqlite_demo.py
# @Software: PyCharm


from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine,Column,String,Integer

engine=create_engine('sqlite:///db/MyDB.sqlite3',echo=True)
DBSession = sessionmaker(bind=engine)
session = DBSession()
Base=declarative_base()

class Mybase(Base):
    #表名:
    __tablename__ ='mycars'
    #字段，属性
    myid=Column(String(50), primary_key=True)
    price=Column(String(50))

def CreatDb():
    #创建表
    Base.metadata.create_all(engine)
def delDb():
    #删除表
    Base.metadata.drop_all(engine)
#创建表
CreatDb()

#添加数据
dt=Mybase(myid='aaa',price="aaa")
session.add(dt)
session.commit()

#修改数据
dt.price='aaaaa'
session.commit()

#查询后修改
ModifyDt=session.query(Mybase).filter_by(myid='asd').first()
ModifyDt.price='bbbb'
session.commit()

#多条件查询，这里注意的是filter_by和filter的区别，filter可以多表查询。比较运算符也不一样。filter必需带表名
querydt=session.query(Mybase).filter(Mybase.myid == 'asd').filter(Mybase.price == 'bbbb')
for i in querydt:
    print(i.myid)