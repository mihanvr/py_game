import requests
import os

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
        if os.path.exists('login.txt'):
            with open('login.txt', 'r') as file:
                login = file.read()
        else:
            print('Введите логин')
            login = str(input())
            with open('login.txt', 'w') as file:
                file.write(login)
        params = {'login': login}
        auth: requests.models.Response = requests.get(url_base + '/auth', json=params)
        token = auth.json()['token']
        print(send_request('look'))
    elif url_base is None:
        print('Вы не подключены к игре, введите "connect <имя_сервера>" для подключения')
    else:
        print(send_request(command))
