# encoding=utf-8

""" 初始的待爬队列 """

import random

MAX_ID = 5666540929

def generateWeiboID():
    random.seed(666)
    weiboID = []
    for i in range(10000):
        weiboID.append(random.randint(0, MAX_ID))
    return weiboID
