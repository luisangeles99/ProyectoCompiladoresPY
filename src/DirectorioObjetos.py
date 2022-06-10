"""
.########..####.########......#######..########........##.########.########..######.
.##.....##..##..##.....##....##.....##.##.....##.......##.##..........##....##....##
.##.....##..##..##.....##....##.....##.##.....##.......##.##..........##....##......
.##.....##..##..########.....##.....##.########........##.######......##.....######.
.##.....##..##..##...##......##.....##.##.....##.##....##.##..........##..........##
.##.....##..##..##....##.....##.....##.##.....##.##....##.##..........##....##....##
.########..####.##.....##.....#######..########...######..########....##.....######.

Esta es la clase pincipal que administra la tabla de objetos, tiene metodos para 
agregar y hacer consultas de objetos.
"""

from DirectorioFunciones import DirectorioFunciones
import sys

class DirectorioObjetos:
    def __init__(self):
        self.directorio = {}

    def addObject(self, name):
        """Agregar un nuevo objeto mediante el identificador.

        Args:
            name (string): identificador
        """        
        if name in self.directorio.keys():
            print('Clase ya declarada')
            sys.exit()
        self.directorio[name]= {
            'funcDirectory': DirectorioFunciones()
        }

    def getObjectVars(self, objName):
        return self.directorio[objName]['funcDirectory'].directorio['program']['vars']

    def getObjectInfo(self, objName):
        info = []
        funcInfo = []
        for func in self.directorio[objName]['funcDirectory'].directorio.keys():
            funcInfo.append(self.directorio[objName]['funcDirectory'].interCodeInfo(func))
        info.append(objName)
        info.append(funcInfo)
        return info
        