
from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/api/cats/<int:id>')
def get_command(id: int):
    return {
        'id': id,
        'breed': 'dog',
        'age': 10+id,
    }


@app.route('/')
def index():
    return get_command('look')


if __name__ == '__main__':
    app.run(debug=True)
