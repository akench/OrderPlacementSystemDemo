from flask import Flask, request, render_template
import pika
import json
import uuid


app = Flask(__name__)
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

@app.route('/placeOrder', methods=['POST'])
def index():
    """
    {
        order: {
            entries: [
                {
                    id: ItemId1,
                    quantity: 2
                }
            ]
        }
    }
    """
    if request.method == 'POST':
        id = uuid.uuid4().urn
        request.json["_id"] = id
        channel.basic_publish(exchange='', routing_key='OrdersQueue', body=json.dumps(request.json))
        return id

if __name__ == '__main__':
    app.run(debug=True, port=5001)
