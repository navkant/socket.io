import asyncio
from chat_client import ChatClient


if __name__ == '__main__':
    addr = ('3.23.103.244', 8000)
    obj = ChatClient(addr)
    obj.choose_option()
