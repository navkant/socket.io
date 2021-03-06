import socket


def echo_server(address):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(address)
    sock.listen(1)
    print(f'listening at {address}')
    while True:
        client, addr = sock.accept()
        print(f'Connected to client at {addr}')
        echo_handler(client)


def echo_handler(client):
    try:
        while True:
            data = client.recv(1024)
            if not data:
                print('exit command recieved')
                raise KeyboardInterrupt
            # print(f'Recieved: {data.decode("utf-8")}')
            client.sendall(b'Got:' + data)
    except KeyboardInterrupt as k:
        print('Connection closed')
        client.close()


if __name__ == '__main__':
    echo_server(('',  8000))
