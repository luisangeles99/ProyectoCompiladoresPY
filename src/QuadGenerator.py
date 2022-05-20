# class description

quadOperations = {
    '+': 1,
    '-': 2,
    '*': 3,
    '/': 4
}

#TODO: 
class QuadGenerator:
    def __init__(self):
        self.quadsTable = []

    def generateQuad(self, oper, dir1, dir2, dir3):
        #TODO: use cube to validate correct quad
        quad = (oper, dir1, dir2, dir3)
        self.quadsTable.append(quad)
        print('Current quads table', self.quadsTable)

    def getQuadsTable(self):
        return self.quadsTable

    #TODO: Special cases for quads like ASSIGN, ETC...
    #TODO: Define all possible operations in a dict to use numbers instead of str
