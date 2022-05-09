# DESCRIPCION DEL DIRECTORIO DE FUNCIONES Y DE SUS METODOS

from VariablesTable import VariablesTable

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
    
    
