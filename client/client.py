import requests

url_base = None


def send_request(command: str) -> str:
    response: requests.models.Response = requests.get(url_base + '/command/'+command, headers={"Token": token})
    return response.content.decode()


# TODO: Подключаться к серверу можно только имея не пустой логин
# TODO: Логин нужно сохранять между сессиями (перезапусками)


while True:
    command = input()
    if command.startswith('connect'):
        url_base = str(command[8:])
        params = {'login': 'me'}
        auth: requests.models.Response = requests.get(url_base + '/auth', json=params)
        token = auth.json()['token']
        print(send_request('look'))
    elif url_base is None:
        print('Вы не подключены к игре, введите "connect <имя_сервера>" для подключения')
    else:
        print(send_request(command))
