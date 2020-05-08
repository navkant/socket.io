# standard library imports here
import asyncio
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
        self.other_client_id = ''

    def recieve_data(self):
        # while True:
        data = self.sock.recv(1024)
        data = data.decode('utf-8')
        print(data)

    def set_my_name(self, name):
        my_uuid = self.uuid
        my_name = name
        message = f'{my_uuid}:{str(1)}:{my_name}'
        self.sock.sendall(bytes(message, 'utf-8'))

    def get_all_users(self):
        my_uuid = self.uuid
        message = f'{my_uuid}:{str(2)}'
        self.sock.sendall(bytes(message, 'utf-8'))
        self.recieve_data()

    def chat(self, sender_id, reciever_id):
        while True:
            print('Enter your message here: ')
            message = str(input())
            packet = f'{sender_id}:{str(3)}:{reciever_id}:{message}'
            self.sock.sendall(bytes(packet, 'utf-8'))
            self.recieve_data()
            # data = self.sock.recv(1024)
            # data = data.decode('utf-8')
            # print(data)

    def choose_option(self):
        while True:
            print('Choose one of the option and enter that number: ')
            print('1. Set your name')
            print('2. Get all users')
            print('3. Start Chat')
            print('4. Recieve message')
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
            elif option == 3:
                print('Enter id of the other person you want to talk to.')
                other_client = input()
                self.other_client_id = other_client
                self.chat(self.uuid, self.other_client_id)
            elif option == 4:
                self.recieve_data()

    async def start_client(self, loop):
        # try:
        #     while True:
        chat_client = loop.create_task(self.choose_option())
        recv_service = loop.create_task(self.recieve_data(loop))
        await asyncio.gather(*chat_client, *recv_service)
