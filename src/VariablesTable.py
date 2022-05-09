# clase para tener la estructura de tabla de variables 
# estará disponible para variables globales y locales
# locales solo en función

class VariablesTable:
    def __init__(self):
        self.table = {}

    #add var to table
    def addVar(self, name, type, val): # TODO: USE MEMORY AND TO ADD MATRIX
        if name in self.table.keys():
            print('Variable declarada aquí saldríamos')
            return
        self.table[name] = {
            'type': type,
            'value': val
        }

    #TODO: Implement GETTERS AND SETTERS FOR DIRECTORY USE
