from datetime import datetime
import json
import os

from flask import (Flask, render_template,
                   request, jsonify)

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
            return handler()

        return jsonify(success=False)

    else:
        return render_template('home.html')

@app.after_request
def add_header(r):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    r.headers['Last-Modified'] = datetime.now()
    r.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, "\
                                 "post-check=0, pre-check=0, max-age=0"
    r.headers["Pragma"] = "no-cache"
    r.headers["Expires"] = "-1"
    return r



@app.route('/reset')
def reset_command():
    with open(get_command_file_path(), 'w') as f:
        f.write('alert("No action")')

    return jsonify(success=True)


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


def get_command_file_path():
    return os.path.join(app.root_path, 'static', 'command.js')


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
    with open(get_command_file_path(), 'w') as f:
        f.write('alert("gmail")')

    return jsonify(success=True)



