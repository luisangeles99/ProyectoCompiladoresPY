#class memoria description
# not using dictionaries but spaces as specified in class

dirBasesLocales = {
    'int': 5000,
    'float': 6000,
    'char': 7000,
    'bool':8000
}

dirBasesGlobales = {
    'int': 9000,
    'float': 11000,
    'char': 13000,
    'bool': 15000
}

dirBasesConstantes = {
    'int': 17000,
    'float': 18000,
    'char': 19000,
    'bool': 20000
}

dirBasesTemporales = {
    'int': 21000,
    'float': 23000,
    'char': 25000,
    'bool': 27000
}

dirBasePointers = 30000

class Memoria:
    def __init__(self):
        self.memoria = []
        #clase memoria

    def setValue(self, offset, val, type):
        pass

    def allocateMemory(self, numInt, numFloat, numChar, numBool, scope):
        if scope == 'local':
            pass