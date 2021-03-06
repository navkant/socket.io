# standard library imports here
import asyncio
import json
import socket
import uuid


class ChatServerSocket:

    def __init__(self, address):
        self.address = address
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients_dict = dict()

    def _get_task(self, task_id):
        task = self.task_dict[task_id]
        return task

    def get_listening_address(self):
        print(f'Listening at : {self.address}')

    def _bind_and_listen(self):
        self.sock.bind(self.address)
        self.sock.listen(1)
        self.get_listening_address()
        self.sock.setblocking(False)

    async def chat_handler(self, client, loop):
        try:
            while True:
                data = await loop.sock_recv(client, 1024)
                print('data received: ', data)
                if not data:
                    print('exit command recieved')
                    raise KeyboardInterrupt
                data = data.decode('utf-8')
                task_id = data.split(':')[1]

                if task_id == '1':
                    client_id = data.split(':')[0]
                    client_name = data.split(':')[2]
                    await self.set_client_name(client_id, client_name)
                elif task_id == '2':
                    client_id = data.split(':')[0]
                    await self.get_all_clients(client_id, loop)
                elif task_id == '3':
                    reciever_id = data.split(':')[2]
                    sender_id = data.split(':')[0]
                    message = data.split(':')[3]
                    sender_name = self.clients_dict[sender_id]['name']
                    reciever_client = self.clients_dict[reciever_id]['client']
                    message = f'{sender_name}: {message}'
                    print(f'message to sent: {message}')
                    await loop.sock_sendall(reciever_client, bytes(message, 'utf-8'))

                # other_client = self.clients_dict[other_client_key]
                # await loop.sock_sendall(other_client, bytes(message, 'utf-8'))
        except KeyboardInterrupt as k:
            print('Connection closed')
            client.close()

    async def start_accepting(self, loop):
        self._bind_and_listen()
        try:
            while True:
                client, addr = await loop.sock_accept(self.sock)
                client_uuid = str(uuid.uuid4())
                welcome_string = f'Welcome to chat server. Your id is _{client_uuid}_, use this to set your name'
                await loop.sock_sendall(client, bytes(welcome_string, 'utf-8'))
                self.clients_dict[client_uuid] = {'name': '', 'client': client}
                print(self.clients_dict)
                # clients_list = json.dumps(list(self.clients_dict.keys()))
                # await loop.sock_sendall(client, bytes(clients_list, 'utf-8'))
                loop.create_task(self.chat_handler(client, loop))
        except KeyboardInterrupt as k:
            pass

    async def set_client_name(self, client_uuid, name):
        self.clients_dict[client_uuid]['name'] = name

    async def get_all_clients(self, client_uuid, loop):
        client = self.clients_dict[client_uuid]['client']
        temp_client_dict = dict()
        for key in self.clients_dict.keys():
            if key == client_uuid:
                continue
            temp_client_dict[self.clients_dict[key]['name']] = key

        message = json.dumps(temp_client_dict)
        message = bytes(message, 'utf-8')
        print(message)
        await loop.sock_sendall(client, message)
