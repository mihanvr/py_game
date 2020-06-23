import requests

command: str = 'hello'

response: requests.models.Response = requests.get('http://127.0.0.1:5000/'+command)
print(response.content)







