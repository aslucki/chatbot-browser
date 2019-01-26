import uuid

from flask import Flask, render_template, request, jsonify

from handlers_manager import HandlersManager
from api_manager import DialogFlowAPIManager

app = Flask(__name__)
api_manager = DialogFlowAPIManager('test-agent-fb700', 'pl')

# TODO: Implement real sessions
session_id = uuid.uuid4().hex


@app.route('/_check')
def health_check():
    resp = jsonify(success=True)
    return resp


@app.route('/', methods=['GET', 'POST'])
def chat():

    if request.method == 'POST':
        query = request.form['query']
        intent, answer = api_manager.get_answer(session_id, query)

        return HandlersManager.handle_intent(intent, answer)
    else:
        return render_template('start.html')


@app.route('/_test')
def test():
    intent = request.args.get('intent')
    query = request.args.get('query')

    chatbot_answer = "Kulfon odpowiedział " + intent

    return HandlersManager.handle_intent(intent,
                                         answer=chatbot_answer,
                                         query=query)


