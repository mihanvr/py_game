from battle import test_class, database


while True:
    command = input()
    response_list = test_class.do_command(command)
    for response in response_list:
        print(response)
