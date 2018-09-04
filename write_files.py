# -*- coding: utf-8 -*-
# @Time    : 2018/9/4 21:48
# @Author  : 
# @File    : write_files.py
# @Software: PyCharm Community Edition
import csv

class WriteCSV():
    '''写CSV文件'''
    def __init__(self,filename):
        '''
        创建文件对象
        :param filename: 文件名
        '''
        self.csvfile = open(filename, 'w', newline='')  # 设置newline，否则两行之间会空一行
        self.writer = csv.writer(self.csvfile)
    def writerow(self,data):
        '''
        写入行数据
        :param data: datalist
        :return:
        '''
        self.writer.writerow(data)
    def close(self):
        '''
        文件关闭
        :return:
        '''
        self.csvfile.close()