import requests

url_base = None

while True:
    command = input()
    if command.startswith('connect'):
        url_base = str(command[8:])
        response:requests.models.Response = requests.get(url_base + '/command/look')
        print(response.content.decode())
    elif url_base is None:
        print('Вы не подключены к игре, введите "connect <имя_сервера>" для подключения')
    else:
        response:requests.models.Response = requests.get(url_base + '/command/' + command)
        print(response.content.decode())
