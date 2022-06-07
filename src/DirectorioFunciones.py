"""
.########.##.....##.##....##..######.....########..####.########.
.##.......##.....##.###...##.##....##....##.....##..##..##.....##
.##.......##.....##.####..##.##..........##.....##..##..##.....##
.######...##.....##.##.##.##.##..........##.....##..##..########.
.##.......##.....##.##..####.##..........##.....##..##..##...##..
.##.......##.....##.##...###.##....##....##.....##..##..##....##.
.##........#######..##....##..######.....########..####.##.....##

Estructura que administra la tabla de funciones, en ella se iran
almacenando las funciones con la informacion pertinente de las
mismas.
"""

from VariablesTable import VariablesTable
import sys

class ParamTable:
    def __init__(self):
        self.table = []
        self.paramNames = []
        self.counter = 0
    
    def addParam(self, type, name):
        self.counter = self.counter + 1
        self.table.append(type)
        self.paramNames.append(name)

    def getParamType(self, index):
        return self.table[index]
    
    def getParamName(self, index):
        return self.paramNames[index]

class DirectorioFunciones:
    
    def __init__(self):
        self.directorio = {}

    def addFunction(self, name, returnType): 
        """Metodo principal para agregar funciones a la tabla.

        Args:
            name (string): identificador
            returnType (string): tipo de dato de retorno
        """        
        if name in self.directorio.keys():
            print('Funcion ya declarada error')
            return
        self.directorio[name] = {
            'type': returnType,
            'vars': VariablesTable(),
            'numParams': 0,
            'numVars': 0,
            'numTemps': 0,
            'numPointers': 0,
            'paramsTable': ParamTable(),
            'startCounter': None,
            'return': False,
            'globalRetAddress': None
        }
    
    def functionExists(self, name):
        return name in self.directorio.keys()

    def getVar(self, funcName, varName):
        """Metodo de consulta a variables por medio del
        nombre de la funcion.

        Args:
            funcName (string): nombre de la funcion
            varName (string): nombre de la variable buscada

        Returns:
            any: variable encontrada
        """        
        if self.functionExists(funcName):
            if self.directorio[funcName]['vars'].searchVar(varName):
                return self.directorio[funcName]['vars'].getVar(varName)
            elif self.directorio['program']['vars'].searchVar(varName):
                return self.directorio['program']['vars'].getVar(varName)
            else:
                print('Variable ', varName, 'no existe en el contexto')
                sys.exit()
        else:
            print('Funcion no existe')
            sys.exit()

    def getVarDimNode(self, funcName, varName):
        if self.directorio[funcName]['vars'].searchVar(varName):
            return self.directorio[funcName]['vars'].getDimNode(varName)
        else:
            return self.directorio['program']['vars'].getDimNode(varName)

    def checkVarIsDim(self, funcName, varName):
        if self.directorio[funcName]['vars'].searchVar(varName):
            return self.directorio[funcName]['vars'].getArrayFlag(varName)
        else:
            return self.directorio['program']['vars'].getArrayFlag(varName)

    def addVar(self, funcName, varName, type, virtualAdd):
        """Metodo para agregar variables a la tabla por medio del nombre
        de la funcion.

        Args:
            funcName (string): nombre de la funcion
            varName (string): nombre de la variable
            type (string): tipo de dato
            virtualAdd (int): direccion virtual
        """               
        if self.functionExists(funcName):
            if not self.directorio[funcName]['vars'].searchVar(varName):
                self.directorio[funcName]['vars'].addVar(varName, type, virtualAdd)
            else:
                print('Variable ya declarada ', varName)
                sys.exit()
        else:
            print('Funcion no existe')
            sys.exit()

    def addComplexVar(self, funcName, varName):
        self.directorio[funcName]['vars'].addComplexVar(varName)

    def addObjectVar(self, funcName, name, varName, type, vAddress):
        self.directorio[funcName]['vars'].addObjectVar(name, varName, type, vAddress)
            
    def addDimToVar(self, funcName, varName, val):
        if not self.directorio[funcName]['vars'].getArrayFlag(varName):
            self.directorio[funcName]['vars'].addDim(varName, val)
        else:
            self.directorio[funcName]['vars'].addDimNode(varName, val)
    
    def dimPostDeclarationCalc(self, funcName, varName):
        self.directorio[funcName]['vars'].dimPostDeclarationCalc(varName)

    def updateVarValue(self, funcName, varName, val):
        """Actualizacion del valor de un registro en la tabla, pero medio
        del nombre de la funcion y la variable.

        Args:
            funcName (string): nombre de la funcion
            varName (string): nombre de la variable
            val (any): nuevo valor
        """        
        if self.functionExists(funcName):
            if self.directorio[funcName]['vars'].searchVar(varName):
                self.directorio[funcName]['vars'].updateVal(varName, val)
            else:
                print('Variable no existe en funcion ', funcName, ' ni en scope global')
                sys.exit()
        else:
            print('Funcion no existe')
            sys.exit()

    def addParam(self, funcName, type, varName):
        self.directorio[funcName]['paramsTable'].addParam(type, varName)
    
    def getParamType(self, funcName, index):
        if index < self.directorio[funcName]['numParams']:
            return self.directorio[funcName]['paramsTable'].getParamType(index)
        print('Numero de parametros incorrectos en funcion ', funcName)
        sys.exit()

    def getParamName(self, funcName, index):
        if index < self.directorio[funcName]['numParams']:
            return self.directorio[funcName]['paramsTable'].getParamName(index)

    def setNumParams(self, funcName):
        self.directorio[funcName]['numParams'] = self.directorio[funcName]['paramsTable'].counter

    def setNumVars(self, funcName, num):
        self.directorio[funcName]['numVars'] = num

    def setNumTemp(self, funcName, num):
        self.directorio[funcName]['numTemps'] = num

    def setNumPointer(self, funcName, num):
        self.directorio[funcName]['numPointers'] = num
    
    def setStartCounter(self, funcName, counter):
        self.directorio[funcName]['startCounter'] = counter

    def setReturnFlag(self, funcName):
        self.directorio[funcName]['return'] = True

    def setGlobalReturnAddress(self, funcName, address):
        self.directorio[funcName]['globalRetAddress'] = address

    def getVarVirtualAddress(self, funcName, varName):
        if self.directorio[funcName]['vars'].searchVar(varName):
            return self.directorio[funcName]['vars'].getVarVirtualAddress(varName)
        else:
            return self.directorio['program']['vars'].getVarVirtualAddress(varName)

    def getVarSize(self, funcName, varName):
        if self.directorio[funcName]['vars'].searchVar(varName):
            return self.directorio[funcName]['vars'].getVarSize(varName)
        else:
            return self.directorio['program']['vars'].getVarSize(varName)

    def interCodeInfo(self, funcName):
        """Informacion de codigo intermedio, es una impresion
        que contiene informacion relevante para ser utilizada por
        la maquina virutal.

        Args:
            funcName (string): nombre de la funcion

        Returns:
            array: nombre de funcion, numero de parametros, variables,
            temporales, counter, direccion y apuntadores.
        """        
        info = []
        info.append(funcName)
        info.append(self.directorio[funcName]['numParams'])
        info.append(self.directorio[funcName]['numVars'])
        info.append(self.directorio[funcName]['numTemps'])
        info.append(self.directorio[funcName]['startCounter'])
        info.append(self.directorio[funcName]['globalRetAddress'])
        info.append(self.directorio[funcName]['numPointers'])
        return info

