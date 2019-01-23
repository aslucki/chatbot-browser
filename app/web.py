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

        try:
            request_dict = json.loads(request.data.decode('utf-8'))

            with open("test.txt", 'w') as f:
                json.dump(request_dict, f)

            confidence =\
                request_dict['queryResult']['intentDetectionConfidence']
            function = request_dict['queryResult']['parameters']['functions']
            query = request.data['queryResult']['queryText']

            print('Confidence: {}'
                  'Function: {}'
                  'Query: {}'.format(confidence, function, query))

        except KeyError as error:
            print(error)
        except TypeError as error:
            print(error)

        return jsonify(success=True)

    else:
        return 'received GET request'
