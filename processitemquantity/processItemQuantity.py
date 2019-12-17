import pika
from pymongo import MongoClient
import json

mongoClient = MongoClient()
db = mongoClient.OrderPlacementDB
collection = db.itemQuantity

def recordItemQuantity(channel, method, properties, body):
    entry = json.loads(body)
    print("recording " + str(entry))
    collection.insert_one(entry)

if __name__ == '__main__':
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.basic_consume(queue='ItemQuantityQueue', auto_ack=True, on_message_callback=recordItemQuantity)

    print("waiting for message...")
    channel.start_consuming()