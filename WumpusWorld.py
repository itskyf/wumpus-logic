from os import path
import tkinter as tk
from secrets import randbelow
from PIL import Image, ImageTk

import numpy as np
import WumpusWorldVars as wv


class WumpusWorld:
    def __init__(self, dim):
        self.__dim = dim
        self.__app = tk.Tk()

        # insert Buttons
        self.startButton = tk.Button(self.__app, text="run", command="")
        self.startButton.grid_propagate(0)
        self.startButton.grid(pady=10, padx=5, row=0, column=0)

        self.stepButton = tk.Button(self.__app, text="step", command=self.step)
        self.stepButton.grid_propagate(0)
        self.stepButton.grid(pady=10, padx=5, row=0, column=1)

        self.resetButton = tk.Button(self.__app, text="reset", command=self.resetWorld)
        self.resetButton.grid_propagate(0)
        self.resetButton.grid(pady=10, padx=5, row=0, column=2)

        self.quitButton = tk.Button(self.__app, text="quit", command=self.__app.quit)
        self.quitButton.grid_propagate(0)
        self.quitButton.grid(pady=10, padx=5, row=0, column=3)

        self.__onInit()

    def __onInit(self):
        # insert container frame
        size = self.__dim * 90
        self.container = tk.Frame(
            self.__app, width=size, height=size + 10, bg="#ffffff"
        )
        self.container.grid_propagate(0)
        self.container.grid(row=1, columnspan=5, pady=5, padx=5)

        # create images
        self.__loadImgs()
        self.createWidgets(self.container)
        self.initWorld()
        self.__app.mainloop()

    def resetWorld(self):
        self.container.grid_remove()
        self.__onInit()

    def getCell(self, x, y):
        return self.__percepts[x][y]

    def __placeHunter(self, x, y):
        self.hunterLoc = [x, y]
        self.__updateImg(x, y, wv.HUNTER)

    def placeGold(self):
        x, y = randbelow(self.__dim), randbelow(self.__dim)
        self.__percepts[x][y] = wv.GOLD
        self.__updateImg(x, y, wv.GOLD)

    def placeWumpus(self):
        # TONDO n wumpus
        x, y = randbelow(self.__dim), randbelow(self.__dim)
        self.__percepts[x][y] = wv.WUMPUS
        self.__insertAdjs(x, y, wv.STENCH)
        self.__updateImg(x, y, wv.WUMPUS)

    def placePit(self):
        for _ in range(self.__dim - 2):
            x, y = randbelow(self.__dim), randbelow(self.__dim)
            self.__percepts[x][y] = wv.PIT
            self.__insertAdjs(x, y, wv.BREEZE)
            self.__updateImg(x, y, wv.PIT)

    def __insertAdjs(self, x, y, val):
        pass
        # TONDO

    def __updateImg(self, x, y, obj):
        self.__insertWidget(x, y, obj)

    def createWidgets(self, container):
        for i in range(self.__dim):
            for j in range(self.__dim):
                tk.LabelFrame(container, height=90, width=90, bg="#ffffff").grid(
                    row=i, column=j
                )

    def __loadImgs(self):
        wumpus_img = Image.open(path.join("media", "wumpus.gif"))
        wumpus_img.thumbnail(wv.img_size, Image.ANTIALIAS)
        self.wumpus_img = ImageTk.PhotoImage(wumpus_img)
        # create pit image
        pit_img = Image.open(path.join("media", "pit.gif"))
        pit_img.thumbnail(wv.img_size, Image.ANTIALIAS)
        self.pit_img = ImageTk.PhotoImage(pit_img)
        # create gold image
        gold_img = Image.open(path.join("media", "gold.gif"))
        gold_img.thumbnail(wv.img_size, Image.ANTIALIAS)
        self.gold_img = ImageTk.PhotoImage(gold_img)
        # create gold image
        hunter_img = Image.open(path.join("media", "hunter.gif"))
        hunter_img.thumbnail(wv.img_size, Image.ANTIALIAS)
        self.hunter_img = ImageTk.PhotoImage(hunter_img)

    def __insertWidget(self, x, y, type):
        if type == wv.HUNTER:
            self.__visualGrid[x][y] = tk.Label(
                self.container, height=75, width=75, image=self.hunter_img
            )
            self.__visualGrid[x][y].grid(row=x, column=y)
        elif type == wv.WUMPUS:
            self.__visualGrid[x][y] = tk.Label(
                self.container, height=75, width=75, image=self.wumpus_img
            )
            self.__visualGrid[x][y].grid(row=x, column=y)
        elif type == wv.PIT:
            self.__visualGrid[x][y] = tk.Label(
                self.container, height=75, width=75, image=self.pit_img
            )
            self.__visualGrid[x][y].grid(row=x, column=y)
        elif type == wv.GOLD:
            self.__visualGrid[x][y] = tk.Label(
                self.container, height=75, width=75, image=self.gold_img
            )
            self.__visualGrid[x][y].grid(row=x, column=y)

    def initWorld(self):
        dim = self.__dim
        self.__percepts = np.full((dim, dim, 5), False)
        self.__visualGrid = [[0] * dim] * dim

        self.placeGold()
        self.placePit()
        self.placeWumpus()
        self.__placeHunter(0, 0)
        # TONDO random thang tren, o ben phai no phai an toan

    def step(self):
        x = self.hunterLoc[0]
        y = self.hunterLoc[1]
        self.__visualGrid[x][y].grid_remove()
        self.__visualGrid[x][y] = None
        self.__placeHunter(x + 1, y + 1)
        # TODO
