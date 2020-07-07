from flask import Flask, request, jsonify

from battle import test_class, database
from battle.database import BaseRepository

app = Flask(__name__)


class BaseRepositoryEndpoints:
    repository: BaseRepository

    def __init__(self, path: str, app: Flask, repository: BaseRepository):
        self.repository = repository
        app.view_functions['self.get_all'] = self.get_all
        app.view_functions['self.create_one'] = self.create_one
        app.view_functions['self.update_one'] = self.update_one
        app.add_url_rule(path, 'self.get_all', self.get_all, methods=['GET'])
        app.add_url_rule(path, 'self.create_one', self.create_one, methods=['POST'])
        app.add_url_rule(path, 'self.update_one', self.update_one, methods=['PUT'])

    def get_all(self):
        return jsonify(self.repository.get_all())

    def create_one(self):
        data = request.json
        self.repository.create_one(data)
        self.repository.save_all()
        return 'Item created'

    def update_one(self):
        data = request.json
        self.repository.update_one(data)
        self.repository.save_all()
        return'Item updated'


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


# @app.route('/weapons', methods=['GET'])
# def get_weapons():
#     return jsonify(database.weapon_repository.get_all())


# @app.route('/weapons/<string:id>', methods=['GET'])
def get_weapons_by_id(id: str):
    return jsonify(database.weapon_repository.get_one(id))


# @app.route('/weapons', methods=['POST'])
# def create_weapon():
#     data = request.json
#     database.weapon_repository.create_one(data)
#     database.weapon_repository.save_all()
#     return 'Weapons created'


# @app.route('/weapons', methods=['PUT'])
# def update_weapon():
#     data = request.json
#     database.weapon_repository.update_one(data)
#     database.weapon_repository.save_all()
#     return 'Weapons created'


# @app.route('/weapons/<string:id>', methods=['DELETE'])
def delete_weapon(id: str):
    if database.weapon_repository.delete_one(id) is not None:
        return jsonify(success=True)
    else:
        return jsonify(success=False)


# app.route('/weapons', endpoint=get_weapons, methods=['GET'])
# app.route('/weapons/<string:id>', endpoint=get_weapons_by_id, methods=['GET'])

BaseRepositoryEndpoints('/weapons', app, database.weapon_repository)
BaseRepositoryEndpoints('/spells', app, database.spell_repository)

if __name__ == '__main__':
    app.run(debug=True)


