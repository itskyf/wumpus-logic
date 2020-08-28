from os import path
from collections import deque


class bcolors:
    HEADER = "\033[95m"
    OKBLUE = "\033[94m"
    OKGREEN = "\033[92m"
    WARNING = "\033[93m"
    FAIL = "\033[91m"
    ENDC = "\033[0m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


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
