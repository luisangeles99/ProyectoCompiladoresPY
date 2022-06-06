from pdb import pm
import sys
from Memoria import MemoriaGlobal, MemoriaLocal, rangoGlobales, rangoConstantes, rangoLocales, rangoTemporales, dirBasePointers
import ast
import operator

#Global structs
quads = []
pMemorias = []
pEjecucion = []
funciones = {}
instructionP = 1
memoriaGlobal = MemoriaGlobal()
expOperators = {
    '+': operator.add, 
    '-': operator.sub, 
    '*': operator.mul,
    '/': operator.truediv, 
    '>': operator.gt, 
    '<': operator.lt, 
    '>=': operator.ge, 
    '<=': operator.le, 
    '==': operator.eq, 
    '!=': operator.ne, 
    '||': operator.or_, 
    '&&': operator.and_
}
jumps = ['goto', 'gotoF', 'gotoM', 'GOSUB']
specialFuncs = ['print', 'read']
funcOper = ['ERA', 'PARAM', 'ENDFUNC', 'return']

# Runs through all quads
def execute():
    global pMemorias, pEjecucion, instructionP
    progEnd = len(quads)
    while(instructionP < progEnd):
        oper = quads[instructionP][0]
        quad = quads[instructionP]
        #EXPRESIONES
        if oper in expOperators.keys():
            res = calc(oper, quad[1], quad[2])
            setValue(quad[3], res)
        #SALTOS
        elif oper in jumps:
            jump(oper, quad)
            continue
        #FUNCIONES ESPECIALES
        elif oper in specialFuncs:
            specialFunc(oper, quad)
        #ASIGNACION
        elif oper == '=':
            val = getValue(quad[1])
            address = int(quad[3])
            if address >= dirBasePointers:
                address = pMemorias[-1].getValue(address) 
            setValue(address, val)
        #VERIFY ARRAY
        elif oper == 'verify':
            val = getValue(quad[1])
            lInf = int(quad[2])
            lSup = int(quad[3]) + 1
            if val not in range(lInf, lSup):
                print(val)
                print('INDEX OUT OF LIMITS')
                sys.exit()
        #FUNCIONES
        elif oper in funcOper:
            funcOperations(oper, quad)
        elif oper == 'addBaseAdd':
            val = getValue(quad[1])
            baseAdd = int(quad[2])
            index = val + baseAdd
            setValue(quad[3], index)
        elif oper == 'stopFunc':
            pMemorias.pop()
            instructionP = pEjecucion.pop()
        elif oper == 'END':
            sys.exit()
        else:
            print('Oper no reconocido', oper)
        instructionP = instructionP + 1
        


def funcOperations(oper, quad):
    global instructionP
    if oper == 'ERA':
        memoriaFunc = MemoriaLocal()
        #Get func vars
        numVars = funciones[quad[3]]['numVars']
        memoriaFunc.allocateMemory(numVars, 0)
        #Get func temps
        numTemps = funciones[quad[3]]['numTemps']
        memoriaFunc.allocateMemory(numTemps, 1)
        #Get func pointers
        numPointer = funciones[quad[3]]['numPointers']
        memoriaFunc.allocateMemory([numPointer], 2)
        memoriaActual = pMemorias.pop()
        pMemorias.append(memoriaFunc)
        pMemorias.append(memoriaActual)
    elif oper == 'PARAM':
        param = getValue(quad[1])
        memoriaActual = pMemorias.pop()
        setValue(quad[3], param)
        pMemorias.append(memoriaActual)
    elif oper == 'return':
        val = getValue(quad[3])
        address = funciones[quad[1]]['globalRetAddress']
        setValue(address, val)
    elif oper == 'ENDFUNC':
        pMemorias.pop()
        instructionP = pEjecucion.pop()

def specialFunc(oper, quad):
    if oper == 'print':
        val = getValue(quad[3])
        print(val)
    elif oper == 'read':
        #TODO: read func
        pass

def calc(oper, address1, address2):
    valLeft = getValue(address1)
    valRight = getValue(address2)
    return expOperators[oper](valLeft, valRight)

def jump(oper, quad):
    global instructionP
    if oper == 'goto':
        instructionP = int(quad[3])
    elif oper == 'gotoF':
        val = getValue(quad[1])
        if not val:
            instructionP = int(quad[3])
        else:
            instructionP = instructionP + 1
    elif oper == 'GOSUB':
        memoriaActual = pMemorias.pop()
        memoriaNueva = pMemorias.pop()
        pMemorias.append(memoriaActual)
        pMemorias.append(memoriaNueva)
        pEjecucion.append(instructionP)
        instructionP = int(quad[3])
    elif oper == 'gotoM':
        memoria = MemoriaLocal()
        #Get func vars
        numVars = funciones['main']['numVars']
        memoria.allocateMemory(numVars, 0)
        #Get func temps
        numTemps = funciones['main']['numTemps']
        memoria.allocateMemory(numTemps, 1)
        pMemorias.append(memoria)
        #Get func pointers
        numPointer = funciones['main']['numPointers']
        memoria.allocateMemory([numPointer], 2)
        pMemorias.append(memoria)
        instructionP = int(quad[3])


def getValue(address):
    address = int(address)
    if address >= rangoLocales[0] and address < rangoLocales[1] or address >= rangoTemporales[0] and address < rangoTemporales[1]:
        return pMemorias[-1].getValue(address)
    elif address >= rangoGlobales[0] and address < rangoGlobales[1] or address >= rangoConstantes[0] and address < rangoConstantes[1]:
        return memoriaGlobal.getValue(address)
    elif address >= dirBasePointers and address <= dirBasePointers + 1000 - 1:
        address = pMemorias[-1].getValue(address)
        return getValue(address)
    else:
        print('MEMORY ERROR')
        sys.exit()

def setValue(address, value):
    address = int(address)
    if address >= rangoLocales[0] and address < rangoLocales[1] or address >= rangoTemporales[0] and address < rangoTemporales[1]:
        pMemorias[-1].setValue(address, value)
    elif address >= rangoGlobales[0] and address < rangoGlobales[1] or address >= rangoConstantes[0] and address < rangoConstantes[1]:
        memoriaGlobal.setValue(address, value)
    elif address >= dirBasePointers and address <= dirBasePointers + 1000 - 1:
        pMemorias[-1].setValue(address, value)
    else:
        print('MEMORY OVERFLOW')
        sys.exit()


def readQuads(code):
    global quads
    quads.append('dummy') #quads are 1 indexed and python list are 0 indexed
    start = code.index('QUADS-START')
    end = code.index('QUADS-END')
    for i in range(start + 1, end):
        quad = code[i].split(', ')
        quad = [s.strip("()\'") for s in quad]
        quads.append(quad)

def readFuncs(code):
    global funciones
    start = code.index('FUNC-INFO-START')
    end = code.index('FUNC-INFO-END')
    for i in range(start + 1, end):
        func = ast.literal_eval(code[i])
        funcName = func[0]
        funciones[funcName] = {
            'numParams': func[1],
            'numVars': func[2],
            'numTemps': func[3],
            'startCounter': func[4],
            'globalRetAddress': func[5],
            'numPointers': func[6]
        }
    numVariables = funciones['program']['numVars']
    memoriaGlobal.allocateMemory(numVariables, 0)

def readConst(code):
    start = code.index('CONST-INFO-START')
    end = code.index('CONST-INFO-END')
    numConstantes = funciones['program']['numTemps']
    memoriaGlobal.allocateMemory(numConstantes, 1)
    for i in range(start + 1, end):
        pair = code[i].split(', ')
        pair = [s.strip("()\'") for s in pair]
        setValue(pair[1], pair[0])

def splitRawCode(rawCode):
    splittedCode = []
    for x in range(len(rawCode)):
        splittedCode.append(rawCode[x].rstrip('\n'))
    return splittedCode

'''
if __name__ == '__main__':
    if (len(sys.argv)>1):
        file = sys.argv[1]
        try:
            f = open(file, 'r')
            data = f.readlines()
            f.close()
            data = clean_data(data)
            create(data)
            execute()
            # log()
        except EOFError:
            print(EOFError)
    else:
        print(".dout file not found")
'''

file = 'interCode.txt'
f = open(file, 'r')
rawCode = f.readlines()
code = splitRawCode(rawCode)
readQuads(code)
readFuncs(code)
readConst(code)
execute()