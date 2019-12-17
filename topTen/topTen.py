from flask import Flask, request
import redis
import json

app = Flask(__name__)

@app.route('/topTenItems', methods=['GET'])
def topTenItems():
    r = redis.Redis()
    return r.get("topTen")


if __name__ == '__main__':
    app.run(debug=True, port=5002)