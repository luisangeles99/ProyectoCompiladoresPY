"""
.##.....##.########.##.....##..#######..########..####....###...
.###...###.##.......###...###.##.....##.##.....##..##....##.##..
.####.####.##.......####.####.##.....##.##.....##..##...##...##.
.##.###.##.######...##.###.##.##.....##.########...##..##.....##
.##.....##.##.......##.....##.##.....##.##...##....##..#########
.##.....##.##.......##.....##.##.....##.##....##...##..##.....##
.##.....##.########.##.....##..#######..##.....##.####.##.....##

Clase principal para manejo de memoria, dentro de si misma se
declaran los directorios a utilizar, al igual que sus rangos y
contiene dos metodos pinciaples para administrar la memoria.
"""

# Espacios de memoria designados.
dirBasesLocales = {
    'int': 1000,
    'float': 3000,
    'char': 5000,
    'bool':7000
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

dirBasePointers = 30000 #limite 1000 pointers

rangoLocales = [1000,8999]
rangoGlobales = [9000,16999]
rangoConstantes = [17000, 20999]
rangoTemporales = [21000, 28999]

#Clase Base con metodos compartidos y estructura de memoria
class Memoria:
    def __init__(self):
        self.memoria = [[[],[],[],[]],[[],[],[],[]],[[]]]
    
    def allocateMemory(self, numCells, memoryType):
        """Alocacion de la memoria.

        Args:
            numCells (int): numero de celdas a utilizar
            memoryType (int): tipo de memoria
        """        
        i = 0
        for num in numCells:
            self.memoria[memoryType][i] = [None] * num
            i = i + 1

#Clase derivada con implementaciones para vars globales y constantes
class MemoriaGlobal(Memoria):
    def __init__(self):
        super().__init__()

    def memoryType(self, address):
        """Obtencion de tipo de memoria.

        Args:
            address (int): direccion de memoria

        Returns:
            int: global(0) o constante(1)
        """        
        if address >= rangoGlobales[0] and address <= rangoGlobales[1]:
            return 0
        if address >= rangoConstantes[0] and address <= rangoConstantes[1]:
            return 1
    
    def setValue(self, address, val): 
        """Asignacion de valor a memoria, donde estan las constantes y aputandores
        globales.

        Args:
            address (int): direccion de memoria
            val (any): valor que se estara asignando
        """        
        memoryType = self.memoryType(address)
        index, offset = self.memoryOffset(address, memoryType)
        if index == 0:
            val = int(val)
        elif index == 1:
            val = float(val)
        elif index == 2:
            val = str(val)
        elif index == 3:
            val = bool(val)
        self.memoria[memoryType][index][offset] = val

    def memoryOffset(self, address, memoryType):
        """Calculo de offset para memoria.

        Args:
            address (int): direccion de memoria
            memoryType (int): tipo de memoria

        Returns:
            int: index
            int: valor calculado de offset
        """        
        if memoryType == 0:
            if address >= dirBasesGlobales['int'] and address < dirBasesGlobales['float']:
                offset = address - dirBasesGlobales['int']
                index = 0
            elif address >= dirBasesGlobales['float'] and address < dirBasesGlobales['char']:
                offset = address - dirBasesGlobales['float']
                index = 1
            elif address >= dirBasesGlobales['char'] and address < dirBasesGlobales['bool']:
                offset = address - dirBasesGlobales['char']
                index = 2
            elif address >= dirBasesGlobales['bool'] and address < (dirBasesGlobales['bool'] + 1999):
                offset = address - dirBasesGlobales['bool']
                index = 3
        elif memoryType == 1:
            if address >= dirBasesConstantes['int'] and address < dirBasesConstantes['float']:
                offset = address - dirBasesConstantes['int']
                index = 0
            elif address >= dirBasesConstantes['float'] and address < dirBasesConstantes['char']:
                offset = address - dirBasesConstantes['float']
                index = 1
            elif address >= dirBasesConstantes['char'] and address < dirBasesConstantes['bool']:
                offset = address - dirBasesConstantes['char']
                index = 2
            elif address >= dirBasesConstantes['bool'] and address < (dirBasesConstantes['bool'] + 1999):
                offset = address - dirBasesConstantes['bool']
                index = 3
        return index, offset
    
    def getValue(self, address):
        memoryType = self.memoryType(address)
        index, offset = self.memoryOffset(address, memoryType)
        return self.memoria[memoryType][index][offset]
      
#Clase derivada con implementaciones para vars locales y temporales
class MemoriaLocal(Memoria):
    def __init__(self):
        super().__init__()

    def memoryType(self, address):
        if address >= rangoLocales[0] and address <= rangoLocales[1]:
            return 0
        if address >= rangoTemporales[0] and address <= rangoTemporales[1]:
            return 1
        if address >= dirBasePointers and address < dirBasePointers + 1000 - 1:
            return 2

    def setValue(self, address, val):
        """Asignacion de valor a memoria local, donde estan las variables, 
        temporales y apuntadores.

        Args:
            address (int): direccion de memoria
            val (any): valor que se estara asignando
        """       
        memoryType = self.memoryType(address)
        index, offset = self.memoryOffset(address, memoryType)
        if index == 0:
            val = int(val)
        elif index == 1:
            val = float(val)
        elif index == 2:
            val = str(val)
        elif index == 3:
            val = bool(val)
        self.memoria[memoryType][index][offset] = val

    def memoryOffset(self, address, memoryType):
        """Calculo de offset para memoria.

        Args:
            address (int): direccion de memoria
            memoryType (int): tipo de memoria

        Returns:
            int: index
            int: valor calculado de offset
        """ 
        if memoryType == 0:
            if address >= dirBasesLocales['int'] and address < dirBasesLocales['float']:
                offset = address - dirBasesLocales['int']
                index = 0
            elif address >= dirBasesLocales['float'] and address < dirBasesLocales['char']:
                offset = address - dirBasesLocales['float']
                index = 1
            elif address >= dirBasesLocales['char'] and address < dirBasesLocales['bool']:
                offset = address - dirBasesLocales['char']
                index = 2
            elif address >= dirBasesLocales['bool'] and address < (dirBasesLocales['bool'] + 1999):
                offset = address - dirBasesLocales['bool']
                index = 3
        elif memoryType == 1:
            if address >= dirBasesTemporales['int'] and address < dirBasesTemporales['float']:
                offset = address - dirBasesTemporales['int']
                index = 0
            elif address >= dirBasesTemporales['float'] and address < dirBasesTemporales['char']:
                offset = address - dirBasesTemporales['float']
                index = 1
            elif address >= dirBasesTemporales['char'] and address < dirBasesTemporales['bool']:
                offset = address - dirBasesTemporales['char']
                index = 2
            elif address >= dirBasesTemporales['bool'] and address < (dirBasesTemporales['bool'] + 1999):
                offset = address - dirBasesTemporales['bool']
                index = 3
        elif memoryType == 2:
            offset = address - dirBasePointers
            index = 0
        return index, offset
    
    def getValue(self, address):
        memoryType = self.memoryType(address)
        index, offset = self.memoryOffset(address, memoryType)
        return self.memoria[memoryType][index][offset]
