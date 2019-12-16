import pika
import json
from pymongo import MongoClient

mongoClient = MongoClient()
db = mongoClient.OrderPlacementDB
collection = db.orders



def processOrder(channel, method, properties, body):
    data = json.loads(body)
    print(data)

    # insert whole order into mongodb
    order_id = collection.insert_one(data).inserted_id

    # insert each order entry into queue so items ordered can be updated
    for entry in data["order"]["entries"]:
        channel.basic_publish(exchange='', routing_key='ItemQuantityQueue', body=json.dumps(entry))



if __name__ == '__main__':
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.basic_consume(queue='OrdersQueue', auto_ack=True, on_message_callback=processOrder)
    print("waiting for message...")
    channel.start_consuming()