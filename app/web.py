import json

from flask import (Flask, render_template,
                   request, jsonify)

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/_check')
def healthcheck():
    resp = jsonify(success=True)
    return resp

@app.route('/chatbot', methods=['GET', 'POST'])
def handle_intent():
    if request.method == 'POST':

        request_dict = json.loads(request.data.decode('utf-8'))

        confidence, function, query = extract_request_data(request_dict)

        handler = select_handler(confidence, function)

        if handler:
            return

        return jsonify(success=True)

    else:
        return 'received GET request'


def extract_request_data(data_dict: dict) -> tuple:

    confidence = None
    function = None
    query = None

    try:
        confidence = \
            float(data_dict['queryResult']['intentDetectionConfidence'])
        function = data_dict['queryResult']['parameters']['functions']
        query = data_dict['queryResult']['queryText']

    except KeyError as error:
        print(error)

    except TypeError as error:
        print(error)

    except AttributeError as error:
        print(error)

    return confidence, function, query


def select_handler(confidence: float, funtion_name: str,
                   threshold: float = 0) -> callable:

    if confidence < threshold:
        return None

    if funtion_name == 'mail':
        return handle_mail


def handle_mail():
    return render_template('home.html', test_val="MAIL")

