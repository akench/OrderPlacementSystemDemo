from flask import Flask,request, render_template

app = Flask(__name__)

@app.route('/placeOrder', methods=['GET'])
def index():
    pass

if __name__ == '__main__':
    app.run(debug=True, port=5001)