# encoding=utf-8

# ------------------------------------------
#   增加了向Mysql数据库中保存pipeline
#   需要有MysqlDB,同时修改Spider文件，增加Item类所有变量的if else的返回值，使得可以标准化存储       
#   Updated by Charles Yan
#   Date:2017.1.4
#   Added Mysql insert method
# ------------------------------------------

import pymongo
from items import InformationItem, TweetsItem, RelationshipsItem


class MongoDBPipeline(object):
    def __init__(self):
        clinet = pymongo.MongoClient("localhost", 27017)
        db = clinet["Sina"]
        self.Information = db["Information"]
        self.Tweets = db["Tweets"]
        self.Relationships = db["Relationships"]

    def process_item(self, item, spider):
        """ 判断item的类型，并作相应的处理，再入数据库 """
        if isinstance(item, RelationshipsItem):
            try:
                self.Relationships.insert(dict(item))
            except Exception:
                pass
        elif isinstance(item, TweetsItem):
            try:
                self.Tweets.insert(dict(item))
            except Exception:
                pass
        elif isinstance(item, InformationItem):
            try:
                self.Information.insert(dict(item))
            except Exception:
                pass
        return item
