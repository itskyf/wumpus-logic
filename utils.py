from os import path
from collections import deque


class bcolors:
    RED = "\033[1;31m"
    BLUE = "\033[1;34m"
    CYAN = "\033[1;36m"
    GREEN = "\033[0;32m"
    RESET = "\033[0;0m"
    BOLD = "\033[;1m"
    REVERSE = "\033[;7m"


class Queue:
    def __init__(self):
        self.__key = deque()
        self.__path = deque()

    def __contains__(self, key):
        return key in self.__key

    def push(self, key, path):
        self.__key.append(key)
        self.__path.append(path)

    def pop(self):
        return self.__key.popleft(), self.__path.popleft()

    def empty(self):
        return len(self.__key) == 0
