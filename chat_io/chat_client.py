# standard library imports here
import socket


class ChatClient:
    def __init__(self, addr):
        self.addr = addr
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(addr)
        data = self.sock.recv(1024)
        data = data.decode('utf-8')
        uuid = data.split('_')[1]
        self.uuid = uuid

    def set_my_name(self, name):
        my_uuid = self.uuid
        my_name = name
        message = f'{my_uuid}:{str(1)}:{my_name}'
        self.sock.sendall(bytes(message, 'utf-8'))

    def get_all_users(self):
        my_uuid = self.uuid
        message = f'{my_uuid}:{str(2)}'
        self.sock.sendall(bytes(message, 'utf-8'))
        data = self.sock.recv(1024)
        data = data.decode('utf-8')
        print(data)

    def choose_option(self,):
        print('Choose one of the option and enter that number: ')
        print('1. Set your name')
        print('2. Get all users')
        try:
            option = int(input())
        except Exception as e:
            print('Enter only numbers only')
            option = input()

        if option == 1:
            print('Enter name you suit yourself: ')
            name = str(input())
            self.set_my_name(name)
        elif option == 2:
            self.get_all_users()
