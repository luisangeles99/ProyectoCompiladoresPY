# DESCRIPCION DEL DIRECTORIO DE FUNCIONES Y DE SUS METODOS

from numpy import var
from VariablesTable import VariablesTable
import sys

class DirectorioFunciones:
    
    def __init__(self):
        self.directorio = {}

    def addFunction(self, name, returnType): #TODO: PARAMETERS AND MEMORY
        if name in self.directorio.keys():
            print('Funcion ya declarada error')
            return
        self.directorio[name] = {
            'type': returnType,
            'vars': VariablesTable()
        }
    
    def functionExists(self, name):
        return name in self.directorio.keys()
        
    def getVar(self, funcName, varName):
        if self.functionExists(funcName):
            if self.directorio[funcName]['vars'].searchVar(funcName, varName):
                return self.directorio[funcName]['vars'][varName]
            else:
                print('Variable no existe en el contexto')
                sys.exit()
        else:
            print('Funcion no existe')
            sys.exit()

    def addVar(self, funcName, varName, type, val):
        if self.functionExists(funcName):
            if not self.directorio[funcName]['vars'].searchVar(varName):
                self.directorio[funcName]['vars'].addVar(varName, type, val)
            else:
                print('Variable ya declarada')
                sys.exit()
        else:
            print('Funcion no existe')
            sys.exit()
            

    

