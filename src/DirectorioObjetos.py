
#Descripcion de la clase

from DirectorioFunciones import DirectorioFunciones
import sys

class DirectorioObjetos:
    def __init__(self):
        self.directorio = {}

    def addObject(self, name):
        if name in self.directorio.keys():
            print('Clase ya declarada')
            sys.exit()
        self.directorio[name]= {
            'funcDirectory': DirectorioFunciones()
        }

    def interCodeClassInfo(self, objName):
        info = []
        info.append(objName)
        for funcName in self.directorio[objName]['funcDirectory'].keys():
            info.append(self.directorio[objName]['funcDirectory'].interCodeInfo(funcName))
        return info

    def getObjectVars(self, objName):
        return self.directorio[objName]['funcDirectory'].directorio['program']['vars']

    

        