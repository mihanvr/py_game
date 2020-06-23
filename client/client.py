import requests

# url_base = 'http://03ce8324b700.ngrok.io/'
# url_base = 'http://6eee78d7e94b.ngrok.io/'
url_base = 'http://7e5acf8ee19c.ngrok.io/'

while True:
    command = input()
    response: requests.models.Response = requests.get(url_base + 'command/' + command)
    print(response.content.decode())
