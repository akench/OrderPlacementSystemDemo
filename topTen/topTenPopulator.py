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
    aggregate(
        [ 
            {
                $match: {'orderPlacedTime': { $gte: 1576457220}}
            }, 
            {
                $group: {_id: "$id", totalscore: { $sum: "$quantity"}}
            }, 
            {
                $sort : {totalscore : -1}
            }, 
            { 
                $limit : 10
            } 
        ]
    )

    aggregate 
    1st param = filter
    2nd param = grouping mechanism 
    3rd param = sort by total score desc
    4th param get the first 10
    """
    startTime = time.time() - sec
    query = ([
        { '$match': { 'orderPlacedTime': { '$gte': startTime } }},
        { '$group': { '_id': '$id', 'itemCount': { '$sum': '$quantity' } }},
        { '$sort': { 'itemCount': -1 }},
        { '$limit': 10 }
    ])

    topTenItems = list(collection.aggregate(query))

    r.set("topTen", json.dumps(topTenItems))

calculateTopTenItems(10)