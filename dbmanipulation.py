# -*- coding: UTF-8 -*-
import pymongo
from datetime import datetime
from dateutil import relativedelta
import time

db = None
col = None

def processInit():
    global db
    global col
    client = pymongo.MongoClient("localhost", 27017, connect=True)
    db = client["Vessels"]
    col = db["vess"]

#精确到分钟
def insertIntodb(mydict):
    col.insert_one(mydict)

#精确到天
def queryDB(start, end):
    if start == end:
        end = start + relativedelta.relativedelta(hours=24)
        starttimestamp =int(time.mktime(start.timetuple()))
        endtimestamp = int(time.mktime(end.timetuple()))
        results = col.find({'timeStamp':{'$gte':starttimestamp, '$lt':endtimestamp}})
    else:
        starttimestamp = int(time.mktime(start.timetuple()))
        endtimestamp = int(time.mktime(end.timetuple()))
        results = col.find({'timeStamp':{'$gte':starttimestamp, '$lt':endtimestamp}})
    return results

if __name__ == "__main__":

    processInit()

    #插入操作
    times = datetime(2020, 02, 27)
    timestamp = int(time.mktime(times.timetuple()))
    # mydict = {"timeStamp":timestamp, "num":1}
    # insertIntodb(mydict)

    #查询操作
    # start = datetime(2020,02,05)
    # end = datetime(2020, 02, 06)
    # re = queryDB(start, end)
