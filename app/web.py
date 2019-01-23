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
        print(dir(request))

        try:
            print(request.args)
            print(request.data.decode('utf-8'))
            with open("test.txt", 'w') as f:
                f.write(request.content)
            print(json.loads(str(request.data)))

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
