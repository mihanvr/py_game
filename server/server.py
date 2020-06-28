from flask import Flask, request, jsonify
from battle import test_class, database

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


@app.route('/weapons', methods=['GET'])
def get_weapons():
    return database.load_weapons()


@app.route('/weapons/<string:id>', methods=['GET'])
def get_weapons_by_id(id: str):
    return jsonify(database.load_weapons()[id])


@app.route('/weapons', methods=['POST'])
def create_weapon():
    data = request.json
    for weapon_db in data:
        new_weapon = database.load_weapon(weapon_db)
        database.save_weapon(new_weapon)
    return 'Weapons created'


@app.route('/weapons/<string:id>', methods=['DELETE'])
def delete_weapon(id: str):
    return database.delete_weapon(id)


if __name__ == '__main__':
    app.run(debug=True)


