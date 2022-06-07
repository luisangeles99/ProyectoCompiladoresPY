"""
.##.....##....###....########.....########....###....########..##.......########
.##.....##...##.##...##.....##.......##......##.##...##.....##.##.......##......
.##.....##..##...##..##.....##.......##.....##...##..##.....##.##.......##......
.##.....##.##.....##.########........##....##.....##.########..##.......######..
..##...##..#########.##...##.........##....#########.##.....##.##.......##......
...##.##...##.....##.##....##........##....##.....##.##.....##.##.......##......
....###....##.....##.##.....##.......##....##.....##.########..########.########

Clase para tener la estructura de tabla de variables estará disponible para 
variables globales y locales solo en función. Dentro de la misma podemos encontrar
funciones que ayudan a guardar diferentes variables y funciones dentro de una tabla
de variables, esta tabla tiene diferentes funciones como hacer consultas de diferentes
valores y agregar funciones o variables a la misma. 
"""
import sys

'''DimNode
Esta es una estrucutra que simula una dimension en forma de nodo, se tiene un limite 
inferior y un superior, esta tiene una propiedad next que apunta a otro nodo y el size.
'''
class DimNode:    
    def __init__(self, val):    
        self.lInf = 0
        self.lSup = val - 1
        self.m = None
        self.next = None

''' VariablesTable
Es la estrucutra principal para el manejo de variables a lo largo de la vida el programa,
aqui podemos realizar opreaciones sobre la estrucutra que permita agregar variables o 
funciones de diferentes tipos, hacer consultas a las mismas, agregar dimensiones y
hacer actualizaciones en la tabla.
'''
class VariablesTable:
    def __init__(self):
        self.table = {}

    #add var to table
    def addVar(self, name, type, virtualAdd):
        """metodo principal para agregar variables a la tabla, guarda con llave usando
        el identificador y como valores un diccionario con el tipo, la memoria virtual y
        un flag para saber si es un array.

        Args:
            name (string): identificador
            type (string): tipo de dato
            virtualAdd (int): memoria virtual
        """        
        if name in self.table.keys():
            print('Variable previamente declarada', name)
            sys.exit()
        self.table[name] = {
            'type': type,
            'virtualAdd': virtualAdd,
            'isArray': False
        }

    def addComplexVar(self, name):
        """Para agregar a la tabla variales complejas, solamente se confirma que el
        identificador sea unico y de ser asi sera agregado a la tabla, utilizando como
        llave el nombre y de valores el tipo y el valor.

        Args:
            name (string): identificador
        """        
        if name in self.table.keys():
            print('Variable previamente declarada', name)
            sys.exit()
        self.table[name] = {
            'type': 'complex',
            'vars': VariablesTable()
        }
    
    def addObjectVar(self, complexName, name, type, vAddress):
        self.table[complexName]['vars'].addVar(name, type, vAddress)

    def addDim(self, name, val):
        """Metodo utilizado para agregar dimensiones a un tipo de variable
        array, donde se inicializan los primeros datos de esta estrcutura.

        Args:
            name (string): identificador
            val (any): valor a asignar
        """        
        self.table[name]['dim'] = 1
        self.table[name]['isArray'] = True
        self.table[name]['size'] = None
        self.table[name]['r'] = val #we have c type arrays
        self.table[name]['nodes'] = DimNode(val)

    def getVar(self, name):
        return self.table[name]

    def getVarVirtualAddress(self, name):
        return self.table[name]['virtualAdd']

    def searchVar(self, name):
        return name in self.table.keys()

    def getArrayFlag(self, name):
        return self.table[name]['isArray']

    def updateVal(self, name, val):
        self.table[name]['value'] = val

    def addDimNode(self, name, val):
        """Metodo utilizado para agregar mas dimensiones a un nodo.

        Args:
            name (string): identificador
            val (any): valor de para incrementar la dimension
        """        
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
        
    def getDimNode(self, name):
        return self.table[name]['nodes']

    def getVarSize(self, name):
        return self.table[name]['size']