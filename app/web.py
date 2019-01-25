from flask import Flask, render_template, request, jsonify

from handlers_manager import HandlersManager
from api_manager import DialogFlowAPIManager

app = Flask(__name__)
api_manager = DialogFlowAPIManager('test-agent-fb700', 'pl')

@app.route('/_check')
def health_check():
    resp = jsonify(success=True)
    return resp


@app.route('/', methods=['GET', 'POST'])
def chat():

    if request.method == 'POST':
        query = request.form['query']

        intent, answer = api_manager.get_answer(query)
        function = HandlersManager.get_handler(intent)

        return render_template('conversation.html', text=answer,
                               function=function)
    else:
        return render_template('start.html')

