from flask import Flask, request, render_template, redirect
import requests as r

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        json = buildOrderJSON(request.form)
        response = r.post(url="http://localhost:5001/placeOrder", json=json)
        id = response.text
        return redirect("http://localhost:5000?previousOrder=" + str(id))

    elif request.method == 'GET':
        return render_template('index.html', id = request.args.get('previousOrder', default=None, type=str))


def buildOrderJSON(formData):
    json = {
        'order': {
            'entries': []
        }
    }

    itemIdBase = 'ItemId'
    quantityBase = 'Quantity'
    num = 1
    while formData.get(quantityBase + str(num)):
        entry = {
            'id': formData.get(itemIdBase + str(num)),
            'quantity': formData.get(quantityBase + str(num))
        }
        json['order']['entries'].append(entry)
        num += 1

    return json
    

if __name__ == '__main__':
    app.run(debug=True, port=5000)
