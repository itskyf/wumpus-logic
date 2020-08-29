from os import path
from time import sleep
from secrets import randbelow
from PIL import Image, ImageTk

import numpy as np
import tkinter as tk
from WumpusWorldVars import GAMEINFO, PERCEPT, ACTION, DIRECTION

from utils import bcolors


class WumpusWorld:
    def __init__(self, gui: tk, ginfo: GAMEINFO):
        self.info = ginfo
        self.__tk = gui
        # TONDO doc map (doc o utils, them tham so la vi tri wum/gold gi gi do)
        self.__onInit()

    def __onInit(self):
        wsize = self.info.size * 90
        self.__container = tk.Frame(
            self.__tk, width=wsize, height=wsize + 10, bg="#ffffff"
        )
        self.__container.grid_propagate(0)
        self.__container.grid(row=1, columnspan=5, pady=5, padx=5)
        self.__x, self.__y = self.info.agent

        # create images
        self.__loadImgs()
        self.__createWidgets()
        self.__initWorld()

        self.__dir = DIRECTION.RIGHT

    def reset(self):
        # TONDO right edge (khong di qua__placeHunter phai duoc)
        self.__container.grid_remove()
        self.__onInit()

    def __placeHunter(self, x, y):
        self.__delWidget(self.__x, self.__y)
        self.__x, self.__y = x, y
        self.__insertWidget(x, y, self.info.HUNTER)

    def __placeGold(self):
        for x, y in self.info.gold:
            self.__percepts[x][y][PERCEPT.GOLD] = True
            self.__insertWidget(x, y, PERCEPT.GOLD)

    def __placeWumpus(self):
        # TONDO n wumpus
        for x, y in self.info.wumpus:
            self.__percepts[x][y][PERCEPT.WUMPUS] = True
            self.__insertWidget(x, y, PERCEPT.WUMPUS)
            self.__insertAdjs(x, y, PERCEPT.STENCH)

    def __placePit(self):
        for x, y in self.info.pit:
            self.__percepts[x][y][PERCEPT.PIT] = True
            self.__insertWidget(x, y, PERCEPT.PIT)
            self.__insertAdjs(x, y, PERCEPT.BREEZE)

    def __insertAdjs(self, x, y, val):
        for x, y in self.info.getNeighbors(x, y):
            self.__insertWidget(x, y, val)

    def __createWidgets(self):
        for i in range(self.info.size):
            for j in range(self.info.size):
                tk.LabelFrame(self.__container, height=90, width=90, bg="#ffffff").grid(
                    row=i, column=j
                )

    def __loadImgs(self):
        imgSize = self.info.IMGSIZE
        img = Image.open(path.join("media", "wumpus.gif"))
        img.thumbnail(imgSize, Image.ANTIALIAS)
        self.__wimg = ImageTk.PhotoImage(img)
        # pit image
        img = Image.open(path.join("media", "pit.gif"))
        img.thumbnail(imgSize, Image.ANTIALIAS)
        self.__pimg = ImageTk.PhotoImage(img)
        # gold image
        img = Image.open(path.join("media", "gold.png"))
        img.thumbnail(imgSize, Image.ANTIALIAS)
        self.__gimg = ImageTk.PhotoImage(img)
        # hunter image
        img = Image.open(path.join("media", "hunter.png"))
        img.thumbnail(imgSize, Image.ANTIALIAS)
        self.__himg = ImageTk.PhotoImage(img)
        # breeze image
        img = Image.open(path.join("media", "breeze.png"))
        img.thumbnail(imgSize, Image.ANTIALIAS)
        self.__bimg = ImageTk.PhotoImage(img)
        # stench image
        img = Image.open(path.join("media", "stench.png"))
        img.thumbnail(imgSize, Image.ANTIALIAS)
        self.__simg = ImageTk.PhotoImage(img)

    def __delWidget(self, mx, my):
        x = self.info.size - 1 - my
        y = mx
        self.__visualGrid[x][y].grid_remove()
        self.__visualGrid[x][y] = None

    def __insertWidget(self, mx, my, obj):
        cellSize = 75
        x = self.info.size - 1 - my
        y = mx
        if obj == self.info.HUNTER:
            self.__visualGrid[x][y] = tk.Label(
                self.__container, height=cellSize, width=cellSize, image=self.__himg
            )
            self.__visualGrid[x][y].grid(row=x, column=y)
        elif obj == PERCEPT.WUMPUS:
            self.__visualGrid[x][y] = tk.Label(
                self.__container, height=cellSize, width=cellSize, image=self.__wimg
            )
            self.__visualGrid[x][y].grid(row=x, column=y)
        elif obj == PERCEPT.PIT:
            self.__visualGrid[x][y] = tk.Label(
                self.__container, height=cellSize, width=cellSize, image=self.__pimg
            )
            self.__visualGrid[x][y].grid(row=x, column=y)
        elif obj == PERCEPT.GOLD:
            self.__visualGrid[x][y] = tk.Label(
                self.__container, height=cellSize, width=cellSize, image=self.__gimg
            )
            self.__visualGrid[x][y].grid(row=x, column=y)
        elif obj == PERCEPT.STENCH:
            self.__visualGrid[x][y] = tk.Label(
                self.__container, height=cellSize, width=cellSize, image=self.__simg
            )
            self.__visualGrid[x][y].grid(row=x, column=y)
        elif obj == PERCEPT.BREEZE:
            self.__visualGrid[x][y] = tk.Label(
                self.__container, height=cellSize, width=cellSize, image=self.__bimg
            )
            self.__visualGrid[x][y].grid(row=x, column=y)

    def __initWorld(self):
        dim = self.info.size
        self.__percepts = np.full((dim, dim, 5), False)
        self.__visualGrid = [[0] * dim] * dim

        self.__placeGold()
        self.__placePit()
        self.__placeWumpus()
        self.__insertWidget(self.__x, self.__y, GAMEINFO.HUNTER)

        self.__goldLeft = len(self.info.gold)
        self.__wumLeft = len(self.info.wumpus)
        # TONDO init, o ben phai (hoac huong no di duoc) phai safe

    def doAction(self, action):
        if action[0] == ACTION.ROTATE:
            self.__dir = action[1]
        elif action == ACTION.FOWARD:
            dx, dy = DIRECTION.DIR2POS[self.__dir]
            x, y = self.__x + dx, self.__y + dy
            if self.__isStop():
                # TODO finish animation
                return False
            self.__placeHunter(x, y)
        x, y = self.__x, self.__y
        if self.__percepts[x][y][PERCEPT.GOLD]:
            self.__goldLeft -= 1

        sleep(0.25)
        self.__tk.update()
        return True

    def __isStop(self):
        x, y = self.__x, self.__y
        return (
            (self.__goldLeft == 0 and self.__wumLeft == 0)
            or (
                self.__percepts[x][y][PERCEPT.WUMPUS]
                or self.__percepts[x][y][PERCEPT.PIT]
            )
            or not self.info.validPos(x, y)
        )

    def getPercept(self, x, y):
        return self.__percepts[x][y]
