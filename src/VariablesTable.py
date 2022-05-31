# clase para tener la estructura de tabla de variables 
# estará disponible para variables globales y locales
# locales solo en función

import sys


class DimNode:
    def __init__(self, val):
        self.lInf = 0
        self.lSup = val - 1
        self.m = None
        self.next = None

 
class VariablesTable:
    def __init__(self):
        self.table = {}

    #add var to table
    def addVar(self, name, type, val): # TODO: USE MEMORY AND TO ADD MATRIX
        if name in self.table.keys():
            print('Variable declarada aquí saldríamos')
            sys.exit()
        self.table[name] = {
            'type': type,
            'value': val,
            'isArray': False
        }

    def addDim(self, name, val):
        self.table[name]['dim'] = 1
        self.table[name]['isArray'] = True
        self.table[name]['size'] = None
        self.table[name]['r'] = val #we have c type arrays
        self.table[name]['nodes'] = DimNode(val)

    def getVar(self, name):
        return self.table[name]

    #TODO: Implement GETTERS AND SETTERS FOR DIRECTORY USE
    def searchVar(self, name):
        return name in self.table.keys()

    def getArrayFlag(self, name):
        return self.table[name]['isArray']

    def updateVal(self, name, val):
        self.table[name]['value'] = val

    def addDimNode(self, name, val):
        node = self.table[name]['nodes']
        while node.next != None:
            node = node.next
        node.next = DimNode(val)
        self.table[name]['r'] = self.table[name]['r'] * val
        self.table[name]['dim'] = self.table[name]['dim'] + 1

    def dimPostDeclarationCalc(self, name):
        node = self.table[name]['nodes']
        self.table[name]['size'] = self.table[name]['r']
        while node:
            r = self.table[name]['r']
            node.m = r / (node.lSup - node.lInf + 1)
            self.table[name]['r'] = node.m
            node = node.next    

    def printNodes(self, name):
        node = self.table[name]['nodes']
        while node:
            print(node.lSup, node.m)
            node = node.next