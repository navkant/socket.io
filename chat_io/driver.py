import asyncio

from chat_server import ChatServerSocket


if __name__ == '__main__':
    server = ChatServerSocket(('localhost', 8000))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(server.start_accepting(loop))
