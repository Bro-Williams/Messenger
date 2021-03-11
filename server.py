import time
from datetime import datetime

from flask import Flask, request, abort

app = Flask(__name__)

db = [
    {
        'name': 'Sam',
        'text': 'Hello',
        'time': time.time()
    }, {
        'name': 'Kate',
        'text': 'Hello, Sam',
        'time': time.time()
    }
]


@app.route("/")
def hello():
    return "Hello world"


@app.route("/status")
def status():
    return {'status': True,
            'name': 'Messenger',
            'time': datetime.now().strftime('%Y/%m/%d/ %H:%M')
            }


@app.route("/send", methods=['POST'])
def send_messages():
    if not isinstance(request.json, dict):
        return abort(400)

    name = request.json.get('name')
    text = request.json.get('text')

    if not isinstance(name, str) \
            or not isinstance(text, str) \
            or not name or not text:
        return abort(400)

    new_message = {
        'name': name,
        'text': text,
        'time': time.time()
    }
    db.append(new_message)

    return {'ok': True}


@app.route("/messages")
def get_messages():
    try:
        after = float(request.args.get("after", 0))
    except ValueError:
        return abort(400)

    messages = []
    for message in db:
        if message['time'] > after:
            messages.append(message)

    return {'messages': messages}


app.run()