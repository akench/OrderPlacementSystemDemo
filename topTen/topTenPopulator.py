import redis
from pymongo import MongoClient
import time
import json

mongoClient = MongoClient()
db = mongoClient.OrderPlacementDB
collection = db.itemQuantity
r = redis.Redis()


def calculateTopTenItems(sec):
    """
    aggregate 
    1st param = filter
    2nd param = grouping mechanism 
    3rd param = sort by total score desc
    4th param get the first 10
    """
    startTime = time.time() - sec
    aggregateQuery = ([
        {'$match': {'orderPlacedTime': {'$gte': startTime}}},
        {'$group': {'_id': '$id', 'itemCount': {'$sum': '$quantity'}}},
        {'$sort': {'itemCount': -1}},
        {'$limit': 10}
    ])

    topTenItems = list(collection.aggregate(aggregateQuery))

    r.set("topTen", json.dumps(topTenItems))


if __name__ == '__main__':
    timeWindow = 10
    while True:
        print("calculating top 10")
        calculateTopTenItems(timeWindow)
        time.sleep(timeWindow)
