import asyncio
from chat_client import ChatClient


if __name__ == '__main__':
    addr = ('localhost', 8000)
    obj = ChatClient(addr)
    obj.choose_option()
