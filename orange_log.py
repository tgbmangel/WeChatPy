# -*- coding: utf-8 -*-
# @Project : WeChatPy 
# @Time    : 2018/9/7 9:46
# @Author  : 
# @File    : orange_log.py
# @Software: PyCharm
import logging
logger = logging.getLogger(__name__)
logger.setLevel(level = logging.INFO)
handler = logging.FileHandler("log/orange.log",encoding='utf-8')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setLevel(logging.INFO)
handler.setFormatter(formatter)
logger.addHandler(handler)