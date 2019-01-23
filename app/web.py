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

        print(request.data)
        print(type(request.data))

        try:
            with open("test.txt", 'w') as f:
                f.write(str(request.data))
            print(json.loads(request.data))

            confidence = request.data['intentDetectionConfidence']
            function = request.data['queryResult']['parameters']['functions']
            query = request.data['queryResult']['queryText']

            print('Confidence: {}'
                  'Function: {}'
                  'Query: {}'.format(confidence, function, query))
        except KeyError as error:
            print(error)
        except TypeError:
            pass

        return request.data

    else:
        return 'received GET request'
