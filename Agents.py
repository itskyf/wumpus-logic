import numpy as np
from utils import Queue

from KB import KB_PL
from WumpusWorld import WumpusWorld
from WumpusWorldVars import ACTION, DIRECTION, PERCEPT, pos2num

from utils import bcolors


class Agent:
    def __init__(self, world: WumpusWorld, type="PL"):
        self.__alive = True
        self.__world = world
        self.__info = world.info
        self.__kb = KB_PL(self.__info)
        # TODO KBFOL

        self.__visited = np.full((self.__info.size, self.__info.size), False)

        self.__dir = DIRECTION.RIGHT
        self.__actionQueue = [ACTION.FOWARD]
        # TODO canh phai khong foward duoc

        self.__x, self.__y = self.__info.agent
        self.__visited[self.__x][self.__y] = True
        self.__safe = set(self.__info.getNeighbors(self.__x, self.__y))
        self.__doubt = set()
        self.__pit = set()
        self.__wum = []

    def startGame(self, debug=True):
        if self.__alive:
            action = (
                self.__actionQueue.pop()
                if len(self.__actionQueue) > 0
                else self.__planning()
            )
            self.__perform(action)
            print("---")
            if debug:
                if action[0] != ACTION.ROTATE:
                    print("Pos:\t", self.__x, self.__y)
                    print("Dir:\t", self.__dir)
                    print("Safe:\t", self.__safe)
                    print("Doubt:\t", self.__doubt)
                    print("Pit:\t", self.__pit)
                    print("Action:\t", action)
                    print("ActionQ:", self.__actionQueue)
                else:
                    print("Rotate:\t", self.__dir)

            self.__alive = self.__world.doAction(action)

    def __perform(self, action):
        assert action != None
        if action[0] == ACTION.ROTATE:
            self.__dir = action[1]
        elif action == ACTION.FOWARD:
            dx, dy = DIRECTION.DIR2POS[self.__dir]
            self.__x, self.__y = nx, ny = self.__x + dx, self.__y + dy
            self.__MGK()
            if not self.__visited[nx][ny]:
                self.__visited[nx][ny] = True
                percept = self.__world.getPercept(nx, ny)

                if (nx, ny) in self.__safe:
                    self.__safe.remove((nx, ny))
                know = []
                knowStr = ""
                for key, val in PERCEPT.ACRONYM.items():
                    if percept[val]:
                        know.append([pos2num(nx, ny, key)])
                        knowStr += key + str(nx) + str(ny) + " & "
                    else:
                        know.append([-pos2num(nx, ny, key)])
                        knowStr += "~" + key + str(nx) + str(ny) + " & "
                if len(know) > 0:
                    self.__kb.tell(know)
                    print("Tell kb:", knowStr[:-3])
                self.__explore(nx, ny, percept)

    def __MGK(self):
        x, y = self.__x, self.__y
        deadWum = np.full((len(self.__wum),), False)
        for idx, (ix, iy) in enumerate(self.__wum):
            if y == iy:
                deadWum[idx] = True
                self.__actionQueue.append(ACTION.SHOOT)
                if x < ix:
                    self.__actionQueue.append(ACTION.RRIGHT)
                elif ix < x:
                    self.__actionQueue.append(ACTION.RLEFT)
            elif x == ix:
                deadWum[idx] = True
                self.__actionQueue.append(ACTION.SHOOT)
                if y < iy:
                    self.__actionQueue.append(ACTION.RUP)
                elif iy < y:
                    self.__actionQueue.append(ACTION.RDOWN)
        newWum = [self.__wum[i] for i in range(len(self.__wum)) if not deadWum[i]]
        if len(newWum) < len(self.__wum):
            self.__actionQueue.append(ACTION.ROTATE + self.__dir)
            self.__wum = newWum

    def __explore(self, x, y, percept):
        neighbors = (
            set(
                [
                    p
                    for p in self.__info.getNeighbors(x, y)
                    if not self.__visited[p[0]][p[1]]
                ]
            )
            - self.__safe
            - self.__pit
            - set(self.__wum)
        )
        newSafe = set()
        newPit = set()

        if percept[PERCEPT.BREEZE] or percept[PERCEPT.STENCH]:
            self.__doubt |= neighbors
        else:
            self.__doubt -= {(x, y)}
            newSafe |= neighbors

        doubt = self.__doubt.copy()
        for p in doubt:
            c1, c2 = pos2num(p[0], p[1], "P"), pos2num(p[0], p[1], "W")
            if self.__kb.ask(c1):  # Pit
                newPit.add(p)
                self.__doubt.remove(p)
            elif self.__kb.ask(c2):  # Wumpus
                self.__wum.append(p)
                self.__doubt.remove(p)
            elif self.__kb.ask(-c1) and self.__kb.ask(-c2):  # ~P & ~W
                newSafe.add(p)
                self.__doubt.remove(p)

        if len(newSafe) > 0:
            self.__safe |= newSafe
        if len(newPit) > 0:
            self.__pit |= newPit

    def __planning(self):
        if len(self.__safe) > 0:
            safeList = sorted(
                list(self.__safe),
                key=lambda pos: abs(pos[0] - self.__x) + abs(pos[1] - self.__y),
                reverse=True,
            )
            self.__actionQueue = self.__path2actions(self.__bfs(safeList.pop()))
            self.__safe = set(safeList)
            return self.__actionQueue.pop()
        # TODO no more safe: comback and out

    def __bfs(self, goal):
        explored = np.full((self.__info.size, self.__info.size), False)
        frontier = Queue()
        frontier.push((self.__x, self.__y), ())
        while not frontier.empty():
            (x, y), path = frontier.pop()

            explored[x][y] = True
            for nx, ny in self.__info.getNeighbors(x, y):
                cPath = path + ((nx, ny),)
                if (nx, ny) == goal:
                    return cPath
                if (
                    not explored[nx][ny]
                    and (nx, ny) not in frontier
                    and self.__visited[nx][ny]
                ):
                    frontier.push((nx, ny), cPath)
        return None

    def __path2actions(self, path):
        plan = []
        px, py = self.__x, self.__y
        pd = self.__dir
        for x, y in path:
            dx, dy = x - px, y - py
            nd = DIRECTION.POS2DIR[(dx, dy)]
            if nd != pd:
                plan.append(ACTION.ROTATE + nd)
                pd = nd
            plan.append(ACTION.FOWARD)
            px, py = x, y
        plan.reverse()
        return plan
