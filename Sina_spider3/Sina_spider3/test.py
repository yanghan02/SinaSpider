# coding=utf-8

import re
import datetime


def parse_date(text):
    # 2015-03-23 22:37:38
    # 06月03日 19:27
    try:
        return datetime.datetime.strptime(text, "%Y-%m-%d %H:%M:%S")
    except:
        try:
            m = re.search(r'(\d+)月(\d+)日 (\d+):(\d+)', text)
            month = int(m.group(1))
            day = int(m.group(2))
            hour = int(m.group(3))
            minute = int(m.group(4))
            today = datetime.datetime.today()
            return  datetime.datetime(year=today.year, month=month, day=day, hour=hour, minute=minute)
        except:
            return None

def date_to_str(datetime_obj):
    return datetime_obj.strftime("%Y-%m-%d %H:%M")

d1 = parse_date('2015-03-23 22:37:38')
d2 = parse_date('06月03日 19:27')

print(d1.year)
print(d2.year)
print date_to_str(d1)
print date_to_str(d2)