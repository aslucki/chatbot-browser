import uuid

from flask import Flask, render_template, request, jsonify, make_response

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

        user_id = __get_user_id(request, 'user_id')
        intent, answer = api_manager.get_answer(session_id=user_id,
                                                query=query)

        return HandlersManager.handle_intent(intent, answer)
    else:
        response = make_response(render_template('start.html'))
        __set_user_id(response, 'user_id')

        return response


@app.route('/_test')
def test():
    intent = request.args.get('intent')
    query = request.args.get('query')

    chatbot_answer = "Kulfon odpowiedział " + intent

    return HandlersManager.handle_intent(intent,
                                         answer=chatbot_answer,
                                         query=query)


def __get_user_id(request: request, cookie_key: str) -> str:

    user_id = request.cookies.get(cookie_key)
    if not user_id:
        user_id = uuid.uuid4().hex

    return user_id


def __set_user_id(response, cookie_key: str):

    user_id = request.cookies.get(cookie_key)
    if not user_id:
        user_id = uuid.uuid4().hex
        response.set_cookie(cookie_key, user_id)

    return response
