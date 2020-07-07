from datetime import date

from flask import Flask, request, jsonify, abort, Response

from battle import test_class, database
from battle.database import BaseRepository
from battle.users import User

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
        return jsonify(self.repository.find_one(id))

    def delete_one(self, id: str):
        if self.repository.delete_one(id) is not None:
            return jsonify(success=True)
        else:
            return jsonify(success=False)

    def get_all(self):
        return jsonify(self.repository.get_all())

    def create_one(self):
        data = request.json
        self.repository.create_one_json(data)
        self.repository.save_all()
        return 'Item created'

    def update_one(self):
        data = request.json
        self.repository.update_one(data)
        self.repository.save_all()
        return 'Item updated'


@app.route('/command/<string:command>')
def get_command(command: str):
    user = get_user_from_request()
    do_command = test_class.do_command(command, user)
    response = "\n".join(do_command)
    return response


@app.route('/command/')
def get_command_index():
    return get_command('look')


@app.route('/')
def index():
    return get_command('look')


@app.route('/auth')
def auth():
    data = request.json
    login = data['login']
    user = database.users_repository.find_by_login(login)
    if user is None:
        user = User(login=login, token=login + str(date.today()))
        database.users_repository.create_one(user)
        database.users_repository.save_all()
    return jsonify(success=True, token=user.token)


def get_user_from_request():
    token = request.headers.get('Token', None)
    if token is None:
        abort(Response('token not found', status=400))
    user = database.users_repository.find_by_token(token)
    if user is None:
        abort(Response('user not found by token', status=400))
    return user


@app.route('/check_token')
def check_token():
    user = get_user_from_request()
    return jsonify(success=True, login=user.login)


BaseRepositoryEndpoints('/weapons', app, database.weapon_repository)
BaseRepositoryEndpoints('/spells', app, database.spell_repository)

if __name__ == '__main__':
    app.run(debug=True)
