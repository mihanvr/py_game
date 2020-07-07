from flask import Flask, request, jsonify

from battle import test_class, database
from battle.database import BaseRepository

app = Flask(__name__)


class BaseRepositoryEndpoints:
    repository: BaseRepository

    def __init__(self, path: str, app: Flask, repository: BaseRepository):
        self.repository = repository
        app.add_url_rule(path, path + '.get_all', self.get_all, methods=['GET'])
        app.add_url_rule(path, path + '.create_one', self.create_one, methods=['POST'])
        app.add_url_rule(path, path + '.update_one', self.update_one, methods=['PUT'])
        app.add_url_rule(path + '/<string:id>', path + '.get_one', self.get_one, methods=['GET'])
        app.add_url_rule(path + '/<string:id>', path + '.delete_one', self.delete_one, methods=['DELETE'])

    def get_one(self, id: str):
        return jsonify(self.repository.get_one(id))

    def delete_one(self, id: str):
        if self.repository.delete_one(id) is not None:
            return jsonify(success=True)
        else:
            return jsonify(success=False)

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
        return 'Item updated'


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


BaseRepositoryEndpoints('/weapons', app, database.weapon_repository)
BaseRepositoryEndpoints('/spells', app, database.spell_repository)

if __name__ == '__main__':
    app.run(debug=True)
