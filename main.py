#!/usr/bin/env python3

import sys
from os import path

import tkinter as tk

from Agents import Agent
from WumpusWorld import WumpusWorld
from WumpusWorldVars import GAMEINFO


if __name__ == "__main__":
    gui = tk.Tk()
    ginfo = GAMEINFO("map6.txt")
    world = WumpusWorld(gui, ginfo)
    agent = Agent(world)

    stepButton = tk.Button(gui, text="continue", command=agent.startGame)
    stepButton.grid_propagate(0)
    stepButton.grid(pady=10, padx=5, row=0, column=0)

    resetButton = tk.Button(gui, text="reset", command=world.reset)
    resetButton.grid_propagate(0)
    resetButton.grid(pady=10, padx=5, row=0, column=1)

    gui.mainloop()
    # TODO change KB type button
