from battle import test_class
from battle.users import User

while True:
    command = input()
    response_list = test_class.do_command(command, User(login='test', token='1'))
    for response in response_list:
        print(response)
