import asyncio
import socket


async def echo_server(address, loop):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(address)
    sock.listen(1)
    print(f'listening at {address}')
    sock.setblocking(False)
    while True:
        client, addr = await loop.sock_accept(sock)
        print(f'Connected to client at {addr}')
        loop.create_task(echo_handler(client, loop))


async def echo_handler(client, loop):
    try:
        while True:
            data = await loop.sock_recv(1024)
            if not data:
                print('exit command recieved')
                raise KeyboardInterrupt
            await loop.sock_sendall(client, b'Got: ' + data)
    except KeyboardInterrupt as k:
        print('Connection closed')
        client.close()


if __name__ == '__main__':
    echo_server(('',  8000))
