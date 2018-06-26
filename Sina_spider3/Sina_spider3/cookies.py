# encoding=utf-8
# ------------------------------------------
#   版本：3.0
#   日期：2016-12-01
#   作者：九茶<http://blog.csdn.net/bone_ace>
# ------------------------------------------

import os
import time
import json
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import logging


logger = logging.getLogger(__name__)
logging.getLogger("selenium").setLevel(logging.WARNING)  # 将selenium的日志级别设成WARNING，太烦人

"""
    输入你的微博账号和密码，可去淘宝买，一元5个。
    建议买几十个，实际生产建议100+，微博反爬得厉害，太频繁了会出现302转移。
"""

myWeiBo = []
with open('account.txt') as f:
    for line in f.readlines():
        if line.startswith("#"):
            continue
        username, password = line.strip().split(",")
        myWeiBo.append((username, password))


def getCookie(account, password):
    return get_cookie_from_weibo_cn(account, password)


def get_cookie_from_weibo_cn(account, password):
    """ 获取一个账号的Cookie """
    try:
        browser = webdriver.Chrome()
        browser.get("https://weibo.cn/login/")
        time.sleep(1)

        failure = 0
        while u"微博" in browser.title and failure < 5:
            try:
                WebDriverWait(browser, 6000).until(lambda d: u"我的首页" in d.title)
                cookie = {}
                for elem in browser.get_cookies():
                    cookie[elem["name"]] = elem["value"]
                logger.warning("Get Cookie Success!( Account:%s )" % account)
                return json.dumps(cookie)
            except Exception, e:
                pass

    except Exception, e:
        logger.warning("Failed %s!" % account)
        return ""
    finally:
        try:
            browser.quit()
        except Exception, e:
            pass


def initCookie(rconn, spiderName):
    """ 获取所有账号的Cookies，存入Redis。如果Redis已有该账号的Cookie，则不再获取。 """
    for weibo in myWeiBo:
        if rconn.get("%s:Cookies:%s--%s" % (spiderName, weibo[0], weibo[1])) is None:  # 'SinaSpider:Cookies:账号--密码'，为None即不存在。
            cookie = getCookie(weibo[0], weibo[1])
            if len(cookie) > 0:
                rconn.set("%s:Cookies:%s--%s" % (spiderName, weibo[0], weibo[1]), cookie)
    cookieNum = "".join(rconn.keys()).count("SinaSpider:Cookies")
    logger.warning("The num of the cookies is %s" % cookieNum)
    if cookieNum == 0:
        logger.warning('Stopping...')
        os.system("pause")


def updateCookie(accountText, rconn, spiderName):
    """ 更新一个账号的Cookie """
    account = accountText.split("--")[0]
    password = accountText.split("--")[1]
    cookie = getCookie(account, password)
    if len(cookie) > 0:
        logger.warning("The cookie of %s has been updated successfully!" % account)
        rconn.set("%s:Cookies:%s" % (spiderName, accountText), cookie)
    else:
        logger.warning("The cookie of %s updated failed! Remove it!" % accountText)
        removeCookie(accountText, rconn, spiderName)


def removeCookie(accountText, rconn, spiderName):
    """ 删除某个账号的Cookie """
    rconn.delete("%s:Cookies:%s" % (spiderName, accountText))
    cookieNum = "".join(rconn.keys()).count("SinaSpider:Cookies")
    logger.warning("The num of the cookies left is %s" % cookieNum)
    if cookieNum == 0:
        logger.warning("Stopping...")
        os.system("pause")

if __name__ == '__main__':
    logger.addHandler(logging.NullHandler())
    for weibo in myWeiBo:
        cookie = getCookie(weibo[0], weibo[1])
        print(cookie)
        break
