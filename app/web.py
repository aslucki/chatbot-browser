from flask import Flask, render_template, request, jsonify

from google_api_manager import prepare_answer, detect_intent_texts
from handlers import default_handler, mail_request_handler

app = Flask(__name__)


@app.route('/_check')
def health_check():
    resp = jsonify(success=True)
    return resp


@app.route('/', methods=['GET', 'POST'])
def chat():

    if request.method == 'POST':
        query = request.form['query']

        if query == "":
            text = "Możesz napisać swoimi słowami, tochę rozumiem"
            return render_template('conversation.html',
                                   text=text)

        conf, intent, answer, is_fallback =\
            detect_intent_texts('test-agent-fb700',
                                '3123123', query, 'pl')

        function = manage_handlers(intent)
        text = prepare_answer(conf, intent, answer, is_fallback)

        return render_template('conversation.html', text=text,
                               function=function)
    else:
        return render_template('start.html')


def manage_handlers(intent):
    if intent == 'start-action':
        return mail_request_handler()
    else:
        return default_handler()
