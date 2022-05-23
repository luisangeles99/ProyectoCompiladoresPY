# clase para tener la estructura de tabla de variables 
# estará disponible para variables globales y locales
# locales solo en función

import sys

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
            'value': val
        }

    def getVar(self, name):
        return self.table[name]

    #TODO: Implement GETTERS AND SETTERS FOR DIRECTORY USE
    def searchVar(self, name):
        return name in self.table.keys()

    def updateVal(self, name, val):
        self.table[name]['value'] = val
