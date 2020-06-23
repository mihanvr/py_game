import string

from flask import Flask, jsonify
from flask import request
from battle import test_class

app = Flask(__name__)


@app.route('/command/<string:command>')
def get_command(command: str):
    do_command = test_class.do_command(command)
    response = "\n".join(do_command)
    return response


@app.route('/command/')
def get_command_index():
    return get_command('look')


@app.route('/')
def index():
    return get_command('look')


if __name__ == '__main__':
    app.run(debug=True)


