# class description
from tabulate import tabulate

quadOperations = {
    '+': 1,
    '-': 2,
    '*': 3,
    '/': 4
}

class QuadGenerator:
    def __init__(self):
        self.quadsTable = []
        self.counter = 0

    def generateQuad(self, oper, dir1, dir2, dir3):
        self.counter = self.counter + 1
        quad = (oper, dir1, dir2, dir3)
        self.quadsTable.append(quad)

    def getQuadsTable(self):
        return self.quadsTable

    def printQuads(self):
        print (tabulate(self.quadsTable, headers=["Num","Oper", "LOp", "ROp", "Res"]))

    def printQuadsWithCount(self):
        nums = range(1, len(self.quadsTable) + 1)
        table = zip(nums, self.quadsTable)
        print (tabulate(table, headers=["Num","Oper", "LOp", "ROp", "Res"]))

    def updateJump(self, end):
        quad = self.quadsTable[end - 1] #index from 0
        newQuad = (quad[0], quad[1], quad[2], self.counter + 1)
        self.quadsTable[end - 1] = newQuad

    
    
