import flask
from flask import *
from damp11113.network import tcp_send, tcp_receive
from damp11113.file import writefile, readfile
from damp11113 import clock, list2str

app = Flask(__name__)
history = []

@app.route('/api/v1/new_donation', methods=['POST'])
def new_donation():
    try:
        name = request.form['name']
        amount = request.form['amount']
        message = request.form['message']
        if name == '' or amount == '' or message == '':
            return 'something wrong. please check your input.', 400
        tcp_send('localhost', 4231, name) # send name
        tcp_send('localhost', 4232, amount) # send amount
        tcp_send('localhost', 4233, message) # send message
        status = tcp_receive('localhost', 4234) # receive status
        if status == 'success':
            write_message = f"[{clock()}] {name} donated {amount} bath. message {message}"
            writefile('donate.log', write_message)
            history.append(write_message)
            return 'success', 200
        else:
            return f'something wrong. {status}', 400
    except Exception as e:
        return f'something wrong. {e}', 400
# history
@app.route('/log/history_donation/file/', methods=['GET'])
def history_donation():
    try:
        return readfile('donate.log'), 200
    except Exception as e:
        return f'something wrong. {e}', 400

@app.route('/log/history_donation/', methods=['GET'])
def history_donation_json():
    return list2str(history), 200

@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return 'something wrong. please check your route.', 404

@app.route('/image/icon', methods=['GET'])
def icon():
    return open('./templates/assis/icon.png', 'rb').read(), 200

@app.route('/Roboto-Regular.ttf', methods=['GET'])
def font():
    return open('C:\\Users\\Lenovo\\PycharmProjects\\pythonProject\\pygameassets\\font\\Roboto\\Roboto-Regular.ttf', 'rb').read(), 200

app.run(port=2658, debug=True)