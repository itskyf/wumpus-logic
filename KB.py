from pysat.solvers import Glucose4
from WumpusWorldVars import GAMEINFO, pos2num


class KB_PL:
    def __init__(self, ginfo: GAMEINFO):
        self.__solver = Glucose4()
        self.__info = ginfo
        self.__clauses = self.__initClauses("B", "P") + self.__initClauses("S", "W")

    def tell(self, clause):
        pass

    def ask(self, clause):
        pass

    def __initClauses(self, c1, c2):
        cnf_clauses = []
        size = self.__info.size
        for x in range(size):
            for y in range(size):
                lhs = pos2num(x, y, c1)
                rhs = [pos2num(ix, iy, c2) for ix, iy in self.__info.getNeighbors(x, y)]
                cnf_clauses.append(self.__biconditional2cnf(lhs, rhs))
        return cnf_clauses

    def __biconditional2cnf(self, lhs: int, rhs: list):
        res = [[-lhs] + list(rhs)]
        for symbol in rhs:
            res.append([-symbol, lhs])
        return res

