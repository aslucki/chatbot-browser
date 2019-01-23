from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('home.html')

@app.route('/chatbot', methods=['GET', 'POST'])
def handle_fulfillment():
    if request.method == 'POST':
        return request.data
    else:
        return "received GET request"
