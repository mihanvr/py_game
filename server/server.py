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
    return jsonify(database.weapon_repository.get_all())


@app.route('/weapons/<string:id>', methods=['GET'])
def get_weapons_by_id(id: str):
    return jsonify(database.weapon_repository.get_one(id))


@app.route('/weapons', methods=['POST'])
def create_weapon():
    data = request.json
    database.weapon_repository.create_one(data)
    database.weapon_repository.save_all()
    return 'Weapons created'


@app.route('/weapons', methods=['PUT'])
def update_weapon():
    data = request.json
    database.weapon_repository.update_one(data)
    database.weapon_repository.save_all()
    return 'Weapons created'


@app.route('/weapons/<string:id>', methods=['DELETE'])
def delete_weapon(id: str):
    if database.weapon_repository.delete_one(id) is not None:
        return jsonify(success=True)
    else:
        return jsonify(success=False)


if __name__ == '__main__':
    app.run(debug=True)


