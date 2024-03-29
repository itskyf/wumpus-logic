from os import path


class PERCEPT:
    BREEZE = 0
    PIT = 1
    STENCH = 2
    WUMPUS = 3
    GOLD = 4
    AGENT = 5

    ACRONYM = {"B": BREEZE, "P": PIT, "S": STENCH, "W": WUMPUS}


class ACTION:
    FOWARD = "fw"
    ROTATE = "r"
    RLEFT = "rl"
    RRIGHT = "rr"
    RUP = "ru"
    RDOWN = "rd"
    SHOOT = "s"
    OUT = "o"


class DIRECTION:
    LEFT = "l"
    RIGHT = "r"
    UP = "u"
    DOWN = "d"
    POS2DIR = {(-1, 0): LEFT, (1, 0): RIGHT, (0, 1): UP, (0, -1): DOWN}
    DIR2POS = {val: key for key, val in POS2DIR.items()}


class GAMEINFO:
    def __init__(self, fname):
        tmp = self.__loadmap(path.join("maps", fname))
        self.size = tmp[0]
        self.pit = tmp[1]
        self.breeze = tmp[2]
        self.wumpus = tmp[3]
        self.stench = tmp[4]
        self.gold = tmp[5]
        self.agent = tmp[6]

        GAMEINFO.SAFE = "safe"
        GAMEINFO.IMGSIZE = (75, 75)

    def __loadmap(self, fname):
        pit = []
        breeze = []
        wumpus = []
        stench = []
        gold = []
        pos_map = []
        with open(fname, "r") as f:
            n = int(f.readline())
            temp = []
            for row in range(n):
                line = f.readline().rstrip("\n")
                for col, features in enumerate(line.split(".")):
                    temp.append(features)
                    pos_map.append([col + 1, n - 1 - row])
                    for feature in features:
                        if feature == "P":
                            pit.append((col, n - 1 - row))
                        if feature == "B":
                            breeze.append((col, n - 1 - row))
                        if feature == "W":
                            wumpus.append((col, n - 1 - row))
                        if feature == "S":
                            stench.append((col, n - 1 - row))
                        if feature == "G":
                            gold.append((col, n - 1 - row))
                        if feature == "A":
                            agent = (col, n - 1 - row)
                temp.clear()
        return (n, pit, breeze, wumpus, stench, gold, agent)

    def validPos(self, x, y):
        return 0 <= x and 0 <= y and x < self.size and y < self.size

    def getNeighbors(self, x, y):
        neighbors = []
        for dx, dy in DIRECTION.POS2DIR.keys():
            nx, ny = x + dx, y + dy
            if self.validPos(nx, ny):
                neighbors.append((nx, ny))
        return neighbors


def pos2num(x, y, character):
    assert character in PERCEPT.ACRONYM.keys()
    return PERCEPT.ACRONYM[character] * 100 + y * 10 + x + 1
