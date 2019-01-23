import json

from flask import (Flask, render_template,
                   request, jsonify,
                   redirect, url_for)

app = Flask(__name__)


@app.route('/_check')
def healthcheck():
    resp = jsonify(success=True)
    return resp

@app.route('/', methods=['GET', 'POST'])
def handle_intent():
    if request.method == 'POST':

        request_dict = json.loads(request.data.decode('utf-8'))

        confidence, function = extract_request_data(request_dict)

        handler = select_handler(confidence, function)

        if handler:
            handler()
            return jsonify(success=True)

        return jsonify(success=True)

    else:
        return render_template('home.html')


def extract_request_data(data_dict: dict) -> tuple:

    confidence = None
    function = None

    try:
        confidence = \
            float(data_dict['queryResult']['intentDetectionConfidence'])
        function = data_dict['queryResult']['parameters']['functions']

    except KeyError as error:
        print(error)

    except TypeError as error:
        print(error)

    except AttributeError as error:
        print(error)

    return confidence, function


def select_handler(confidence: float, funtion_name: str,
                   threshold: float = 0) -> callable:
    print(confidence)
    print(confidence < threshold)
    if confidence < threshold:
        return None

    if funtion_name == 'mail':
        print("returning handle")
        return handle_mail


def handle_mail():
    with open('static/command.js', 'w') as f:
        f.write('alert("gmail")')

    return jsonify(success=True)

