# DESCRIPCION DEL DIRECTORIO DE FUNCIONES Y DE SUS METODOS

from numpy import var
from VariablesTable import VariablesTable
import sys

class ParamTable:
    def __init__(self):
        self.table = []
        self.counter = 0
    
    def addParam(self, type):
        self.counter = self.counter + 1
        self.table.append(type)

    def getParamType(self, index):
        return self.table[index]

class DirectorioFunciones:
    
    def __init__(self):
        self.directorio = {}

    def addFunction(self, name, returnType): #TODO: PARAMETERS AND MEMORY
        if name in self.directorio.keys():
            print('Funcion ya declarada error')
            return
        self.directorio[name] = {
            'type': returnType,
            'vars': VariablesTable(),
            'numParams': 0,
            'numVars': 0,
            'numTemps': 0,
            'paramsTable': ParamTable(),
            'startCounter': None
        }
    
    def functionExists(self, name):
        return name in self.directorio.keys()
        
    def getVar(self, funcName, varName):
        if self.functionExists(funcName):
            if self.directorio[funcName]['vars'].searchVar(varName):
                return self.directorio[funcName]['vars'].getVar(varName)
            else:
                print('Variable ', varName, 'no existe en el contexto')
                sys.exit()
        else:
            print('Funcion no existe')
            sys.exit()

    def addVar(self, funcName, varName, type, val):
        if self.functionExists(funcName):
            if not self.directorio[funcName]['vars'].searchVar(varName):
                self.directorio[funcName]['vars'].addVar(varName, type, val)
                self.directorio[funcName]['numVars'] = self.directorio[funcName]['numVars'] + 1
            else:
                print('Variable ya declarada')
                sys.exit()
        else:
            print('Funcion no existe')
            sys.exit()
            
    def updateVarValue(self, funcName, varName, val):
        if self.functionExists(funcName):
            if self.directorio[funcName]['vars'].searchVar(varName):
                self.directorio[funcName]['vars'].updateVal(varName, val)
            else:
                print('Variable no existe en funcion ', funcName, ' ni en scope global')
                sys.exit()
        else:
            print('Funcion no existe')
            sys.exit()

    def addParam(self, funcName, type):
        self.directorio[funcName]['paramsTable'].addParam(type)
    
    def getParamType(self, funcName, index):
        if index < self.directorio[funcName]['numParams']:
            return self.directorio[funcName]['paramsTable'].getParamType(index)
        print('Numero de parametros incorrectos en funcion ', funcName)
        sys.exit()

    def setNumParams(self, funcName):
        self.directorio[funcName]['numParams'] = self.directorio[funcName]['paramsTable'].counter

    def setNumVars(self, funcName, num):
        self.directorio[funcName]['numVars'] = num

    def setNumTemp(self, funcName, num):
        self.directorio[funcName]['numTemps'] = num
    
    def setStartCounter(self, funcName, counter):
        self.directorio[funcName]['startCounter'] = counter


