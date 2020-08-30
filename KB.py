import numpy as np
from itertools import product
from pysat.solvers import Glucose4

from WumpusWorldVars import GAMEINFO, pos2num


class KB_PL:
    def __init__(self, ginfo: GAMEINFO):
        self.__solver = Glucose4()
        self.__info = ginfo
        initSentences = self.__initClauses("B", "P") + self.__initClauses("S", "W")
        self.__solver.append_formula(initSentences)

    def __del__(self):
        self.__solver.delete()

    def tell(self, sentence):
        self.__solver.append_formula(sentence)

    def ask(self, sentence):
        neg = KB_PL.__negate(sentence)
        for clause in neg:
            if self.__solver.solve(assumptions=clause) == False:
                return True
        return False

    def __initClauses(self, c1, c2):
        cnf_clauses = []
        size = self.__info.size
        for x in range(size):
            for y in range(size):
                lhs = pos2num(x, y, c1)
                rhs = [pos2num(ix, iy, c2) for ix, iy in self.__info.getNeighbors(x, y)]
                cnf_clauses += KB_PL.biconditional2cnf(lhs, rhs)
        return cnf_clauses

    @staticmethod
    def __negate(sentence):
        if isinstance(sentence, int):
            return [[-sentence]]
        neg = -np.array(list(product(*sentence)))
        return neg.tolist()

    @staticmethod
    def biconditional2cnf(lhs: int, rhs: list):
        res = [[-lhs] + rhs]
        for symbol in rhs:
            res.append([-symbol, lhs])
        return res

