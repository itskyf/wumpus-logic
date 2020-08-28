from os import path
import tkinter as tk
from secrets import randbelow
from PIL import Image, ImageTk

import numpy as np
from WumpusWorldVars import GAMEINFO, PERCEPT


class WumpusWorld:
    def __init__(self, ginfo: GAMEINFO):
        self.__info = ginfo
        self.__tk = tk.Tk()
        # TONDO doc map (doc o utils, them tham so la vi tri wum/gold gi gi do)

        self.stepButton = tk.Button(self.__tk, text="run", command=self.__loop)
        self.stepButton.grid_propagate(0)
        self.stepButton.grid(pady=10, padx=5, row=0, column=0)

        self.resetButton = tk.Button(self.__tk, text="reset", command=self.__resetWorld)
        self.resetButton.grid_propagate(0)
        self.resetButton.grid(pady=10, padx=5, row=0, column=1)

        self.quitButton = tk.Button(self.__tk, text="quit", command=self.__tk.quit)
        self.quitButton.grid_propagate(0)
        self.quitButton.grid(pady=10, padx=5, row=0, column=2)
        # TODO change KB type button

        self.__onInit()

    def __onInit(self):
        wsize = self.__info.size * 90
        self.__container = tk.Frame(
            self.__tk, width=wsize, height=wsize + 10, bg="#ffffff"
        )
        self.__container.grid_propagate(0)
        self.__container.grid(row=1, columnspan=5, pady=5, padx=5)

        # create images
        self.__loadImgs()
        self.__createWidgets()
        self.__initWorld()
        self.__tk.mainloop()

    def __resetWorld(self):
        # TONDO right edge (khong di qua__placeHunter phai duoc)
        self.__container.grid_remove()
        self.__onInit()

    def __placeHunter(self, apos):
        # self.__hunterPos = [x, y]
        self.__insertWidget(apos[0], apos[1], self.__info.HUNTER)

    def __placeGold(self):
        for x, y in self.__info.gold:
            self.__percepts[x][y][PERCEPT.GOLD] = True
            self.__insertWidget(x, y, PERCEPT.GOLD)

    def __placeWumpus(self):
        # TONDO n wumpus
        for x, y in self.__info.wumpus:
            self.__percepts[x][y][PERCEPT.WUMPUS] = True
            self.__insertAdjs(x, y, PERCEPT.STENCH)
            self.__insertWidget(x, y, PERCEPT.WUMPUS)

    def __placePit(self):
        for x, y in self.__info.pit:
            self.__percepts[x][y][PERCEPT.PIT] = True
            self.__insertAdjs(x, y, PERCEPT.BREEZE)
            self.__insertWidget(x, y, PERCEPT.PIT)

    def __insertAdjs(self, x, y, val):
        pass
        # TONDO pit thi ke no co breeze, wum thi co S

    def __createWidgets(self):
        for i in range(self.__info.size):
            for j in range(self.__info.size):
                tk.LabelFrame(self.__container, height=90, width=90, bg="#ffffff").grid(
                    row=i, column=j
                )

    def __loadImgs(self):
        imgSize = self.__info.IMGSIZE
        wumpus_img = Image.open(path.join("media", "wumpus.gif"))
        wumpus_img.thumbnail(imgSize, Image.ANTIALIAS)
        self.__wimg = ImageTk.PhotoImage(wumpus_img)
        # create pit image
        pit_img = Image.open(path.join("media", "pit.gif"))
        pit_img.thumbnail(imgSize, Image.ANTIALIAS)
        self.__pimg = ImageTk.PhotoImage(pit_img)
        # create gold image
        gold_img = Image.open(path.join("media", "gold.gif"))
        gold_img.thumbnail(imgSize, Image.ANTIALIAS)
        self.__gimg = ImageTk.PhotoImage(gold_img)
        # create gold image
        hunter_img = Image.open(path.join("media", "hunter.gif"))
        hunter_img.thumbnail(imgSize, Image.ANTIALIAS)
        self.__aimg = ImageTk.PhotoImage(hunter_img)

    def __insertWidget(self, mx, my, type):
        cellSize = 75
        x = self.__info.size - 1 - my
        y = mx
        if type == self.__info.HUNTER:
            self.__visualGrid[x][y] = tk.Label(
                self.__container, height=cellSize, width=cellSize, image=self.__aimg
            )
            self.__visualGrid[x][y].grid(row=x, column=y)
        elif type == PERCEPT.WUMPUS:
            self.__visualGrid[x][y] = tk.Label(
                self.__container, height=cellSize, width=cellSize, image=self.__wimg
            )
            self.__visualGrid[x][y].grid(row=x, column=y)
        elif type == PERCEPT.PIT:
            self.__visualGrid[x][y] = tk.Label(
                self.__container, height=cellSize, width=cellSize, image=self.__pimg
            )
            self.__visualGrid[x][y].grid(row=x, column=y)
        elif type == PERCEPT.GOLD:
            self.__visualGrid[x][y] = tk.Label(
                self.__container, height=cellSize, width=cellSize, image=self.__gimg
            )
            self.__visualGrid[x][y].grid(row=x, column=y)

    def __initWorld(self):
        dim = self.__info.size
        self.__percepts = np.full((dim, dim, 5), False)
        self.__visualGrid = [[0] * dim] * dim

        self.__placeGold()
        self.__placePit()
        self.__placeWumpus()
        self.__placeHunter(self.__info.agent)
        # TONDO init, o ben phai (hoac huong no di duoc) phai safe

    def __loop(self):
        # TODO died
        pass

    def getPercept(self, x, y):
        return self.__percepts[x][y]

    def getNeighbors(self, x, y):
        return self.__info.getNeighbors(x, y)
