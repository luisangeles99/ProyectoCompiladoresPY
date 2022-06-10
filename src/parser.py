"""
.########.....###....########...######..########.########.
.##.....##...##.##...##.....##.##....##.##.......##.....##
.##.....##..##...##..##.....##.##.......##.......##.....##
.########..##.....##.########...######..######...########.
.##........#########.##...##.........##.##.......##...##..
.##........##.....##.##....##..##....##.##.......##....##.
.##........##.....##.##.....##..######..########.##.....##

La clase fundamental de todo el compilador, donde se encuentran
las reglas gramaticales, las acciones semanticas y los puntos
neuralgicos.
"""
import ply.yacc as yacc
from Avail import Avail
from lexer import tokens
from DirectorioFunciones import DirectorioFunciones
from DirectorioObjetos import DirectorioObjetos
from QuadGenerator import QuadGenerator
from CuboSemantico import SemanticCube
from Memoria import dirBasesConstantes, dirBasesGlobales, dirBasesLocales, dirBasesTemporales, dirBasePointers
import sys

precedence = (
    
    ('right', 'ASSIGN'),
    ('left', 'NE'),
    ('nonassoc', 'LT', 'GT'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIVIDE'),
    ('left', 'LBRACE', 'RBRACE'),
    ('left', 'LPAREN', 'RPAREN'),
    ('left', 'CTEF', 'CTEI')
    
)

currTypeVar = None
currVar = None
currObj = None
currVarObj = None
currTypeFunc = None
currFunc = None
currFuncCall = None
currScope = 'global'
currNode = None
currClass = None
kParam = 0
counterConstantes = [0,0,0,0]
counterGlobales = [0,0,0,0]
counterLocales = [0,0,0,0]
counterTemporales = [0,0,0,0]
subFunc = False

#auxiliares
auxCounterGlobales = None

start = 'P'

#------------------------------------ INSTANTIATE NEEDED DATA STR ------------------------------------

funcDirectory = DirectorioFunciones()
objDirectory = DirectorioObjetos()
quadGenerator = QuadGenerator()
cubo = SemanticCube()
avail = Avail()
constants = []
pOperadores = []
pOperandos = []
pTipos = []
pSaltos = []
pDims = []
pNodos = []
relationalOperators = [
    '>', '<', '>=', '<=', '==', '!='
]
typesIndex = {
    'int': 0,
    'float': 1,
    'char': 2,
    'bool': 3
}

#------------------------------------ PROGRAM SYNTAX ------------------------------------
'''
Reglas gramaticales para la definicion del programa, se especifican declaracion, estructura,
miemebros y librerias.
'''
def p_PROGRAM(p):
    '''P            : PROGRAM ID startProgram SEMICOLON P_STRUCTURE MAIN_FUNC endProgram'''

def p_P_STRUCTURE(p):
    '''P_STRUCTURE  : P_STR_ONE PROG_MEMBERS PROG_M_ONE'''

def p_P_STR_ONE(p):
    '''P_STR_ONE    : LIBS_DECLARATION
                    | empty'''

def p_PROG_MEMBERS(p):
    '''PROG_MEMBERS : CLASS_STR
                    | FUNCTION
                    | DEC_VAR'''

def p_PROG_M_ONE(p):
    '''PROG_M_ONE   : PROG_MEMBERS PROG_M_ONE
                    | empty'''

def p_LIBS_DECLARATION(p):
    '''LIBS_DECLARATION : LIB LIB_ONE'''

def p_LIB_ONE(p):
    '''LIB_ONE      : LIB LIB_ONE
                    | empty'''

def p_LIB(p):
    '''LIB          : IMPORT ID SEMICOLON'''

#------------------------------------ CLASS SYNTAX ------------------------------------

def p_CLASS(p):
    '''CLASS_STR    : CLASS_DEC LBRACE CLASS_BODY RBRACE endClass'''

def p_CLASS_DEC(p):
    '''CLASS_DEC    : CLASS ID addClass CLASS_DEC_ONE'''

def p_CLASS_DEC_ONE(p):
    '''CLASS_DEC_ONE    : CLASS_INHERITS
                        | empty'''

def p_CLASS_INHERITS(p):
    '''CLASS_INHERITS   : DERIVES ID'''

def p_CLASS_BODY(p):
    '''CLASS_BODY       : CLASS_BODY_MEMBER CLASS_B_M_ONE CLASS_CONSTRUCTOR CLASS_BODY_MEMBER CLASS_B_M_ONE'''

def p_CLASS_B_M_ONE(p):
    '''CLASS_B_M_ONE    : CLASS_BODY_MEMBER CLASS_B_M_ONE
                        | empty'''

def p_CLASS_BODY_MEMBER(p):
    '''CLASS_BODY_MEMBER    : FUNCTION
                            | DEC_VAR'''

def p_CLASS_CONSTRUCTOR(p):
    '''CLASS_CONSTRUCTOR    : ID addClassConstructor LPAREN CLASS_C_ONE RPAREN constructorParam setFuncCounter BLOCK endFunc'''

def p_CLASS_C_ONE(p):
    '''CLASS_C_ONE          : PARAM
                            | empty'''

def p_OBJECT_ACCESS(p):
    '''OBJECT_ACCESS        : ID setCurrObj POINT ID setCurrObjVar OBJECT_ACCESS_ONE '''

def p_setCurrObj(p):
    '''setCurrObj           : '''
    global currObj
    currObj = p[-1]

def p_setCurrObjVar(p):
    '''setCurrObjVar        : '''
    global currVarObj
    currVarObj = p[-1]

def p_setCurrObjVarFunc(p):
    '''setCurrObjVarFunc        : '''
    global currTypeVar
    varInfo = funcDirectory.getVar(currFunc, currObj)
    currTypeVar = varInfo['objType'] 

def p_setObjFlag(p):
    '''setObjFuncFlag       : '''
    global subFunc
    subFunc = True

def p_OBJECT_ACCESS_ONE(p):
    '''OBJECT_ACCESS_ONE    : setCurrObjVarFunc setObjFuncFlag verifyFunction LPAREN FUNCTION_C_ONE verifyNumParams RPAREN gosubFunc
                            | fieldAccess empty'''

def p_fieldAccess(p):
    '''fieldAccess         : '''
    objName = currObj
    varName = currVarObj
    objInfo = funcDirectory.getVar(currFunc, objName)
    if objInfo['type'] != 'complex':
        print('Variable', objName, 'no es un objeto')
        sys.exit()
    if not objInfo['vars'].searchVar(varName):
        print('Objeto', objName, 'no tiene la variable', varName)
        sys.exit()
    varInfo = objInfo['vars'].getVar(varName)
    varType = varInfo['type']
    vAddress = varInfo['virtualAdd']
    pOperandos.append(vAddress)
    pTipos.append(varType)

#------------------------------------ FUNCTION SYNTAX ------------------------------------


def p_FUNCTION_CALL(p):
    '''FUNCTION_CALL        : ID verifyFunction LPAREN FUNCTION_C_ONE verifyNumParams RPAREN gosubFunc'''

def p_FUNCTION_C_ONE(p):
    '''FUNCTION_C_ONE       : EXP verifyParam FUNCTION_C_TWO
                            | empty'''

def p_FUNCTION_C_TWO(p):
    '''FUNCTION_C_TWO       : COMMA EXP verifyParam FUNCTION_C_TWO
                            | empty'''

def p_FUNCTION_DEC(p):
    '''FUNCTION_DEC         : FUNC FUNCTION_D_ONE ID addFunc LPAREN FUNCTION_D_TWO RPAREN setNumParams'''

def p_MAIN_FUNC(p):
    '''MAIN_FUNC            : MAIN addMain LPAREN RPAREN BLOCK endFunc'''

def p_FUNCTION(p):
    '''FUNCTION             : FUNCTION_DEC setFuncCounter BLOCK endFunc'''

def p_FUNCTION_D_ONE(p):
    '''FUNCTION_D_ONE       : SIMPLE_TYPE
                            | VOID'''
    if p[1] == 'void':
        global currTypeFunc
        currTypeFunc = p[1]

def p_FUNCTION_D_TWO(p):
    '''FUNCTION_D_TWO       : PARAM
                            | empty'''

def p_PARAM(p):
    '''PARAM                : SIMPLE_TYPE ID addParam PARAM_ONE'''


def p_PARAM_ONE(p):
    '''PARAM_ONE            : COMMA PARAM
                            | empty'''

#------------------------------------ VARIABLES SYNTAX ------------------------------------

def p_VARIABLE(p):
    '''VARIABLE             : ID pushVar VARIABLE_ONE
                            | OBJECT_ACCESS'''

def p_VARIABLE_ONE(p): #TODO. If time allows it; allow more dims
    '''VARIABLE_ONE         : LSBRACKET verifyArray EXP createArrayQuads RSBRACKET VARIABLE_TWO createLastArrayQuads
                            | empty'''

def p_VARIABLE_TWO(p):
    '''VARIABLE_TWO         : LSBRACKET updateDimArray EXP createArrayQuads RSBRACKET
                            | empty'''

def p_ASSIGN_OP(p):
    '''ASSIGN_OP            : VARIABLE ASSIGN EXP SEMICOLON'''
    temp = pOperandos.pop()
    tempType = pTipos.pop()
    varId = pOperandos.pop()
    varType = pTipos.pop()
    if varType != tempType:
        print('Type mismatch in assign for var: ', varId)
        sys.exit()
    vAddress = temp
    vAddress2 = varId
    if type(temp) != int:
        if currClass != None:
            vAddress = objDirectory.directorio[currClass]['funcDirectory'].getVarVirtualAddress(currFunc, temp)
        else:
            vAddress = funcDirectory.getVarVirtualAddress(currFunc, temp)
    if type(varId) != int:
        if currClass != None:
            vAddress2 = objDirectory.directorio[currClass]['funcDirectory'].getVarVirtualAddress(currFunc, varId)
        else:
            vAddress2 = funcDirectory.getVarVirtualAddress(currFunc, varId)
    quadGenerator.generateQuad(p[2], vAddress, None, vAddress2)
    

def p_DEC_VAR(p):
    '''DEC_VAR              : VAR DEC_VAR_ONE SEMICOLON'''

def p_DEC_VAR_ONE(p):
    '''DEC_VAR_ONE          : COMPLEX_TYPE ID addComplexVar DEC_V_O_COMPLEX
                            | SIMPLE_TYPE ID addVar DEC_ARR DEC_V_O_SIMPLE'''

def p_DEC_V_O_SIMPLE(p):
    '''DEC_V_O_SIMPLE       : COMMA ID addVar DEC_ARR DEC_V_O_SIMPLE
                            | empty'''
                    
def p_DEC_ARR(p):
    '''DEC_ARR              : LSBRACKET CTEI addDimVar RSBRACKET DEC_ARR_ONE arrDeclarationCalc
                            | empty'''

def p_DEC_ARR_ONE(p):
    '''DEC_ARR_ONE          : LSBRACKET CTEI addDimVar RSBRACKET
                            | empty'''

def p_DEC_V_O_COMPLEX(p):
    '''DEC_V_O_COMPLEX      : COMMA ID DEC_V_O_COMPLEX
                            | empty'''

def p_SIMPLE_TYPE(p):
    '''SIMPLE_TYPE          : INT 
                            | FLOAT 
                            | CHAR'''
    if p[-1] == 'func':
        global currTypeFunc
        currTypeFunc = p[1]
    #elif p[-1] == 'var':
    #    global currTypeVar
    #    currTypeVar = p[1]
    else:
        global currTypeVar
        currTypeVar = p[1]

def p_COMPLEX_TYPE(p):
    '''COMPLEX_TYPE         : ID checkClassName'''

#------------------------------------ EXPRESSIONS SYNTAX ------------------------------------

def p_EXP(p):
    '''EXP          : T_EXP logicalOrOperation EXP_ONE'''

def p_EXP_ONE(p):
    '''EXP_ONE      : OR pushOperador EXP
                    | empty'''

def p_T_EXP(p):
    '''T_EXP        : G_EXP logicalAndOperation T_EXP_ONE'''

def p_T_EXP_ONE(p):
    '''T_EXP_ONE    : AND pushOperador T_EXP
                    | empty'''

def p_G_EXP(p):
    '''G_EXP        : MID_EXP relationalOperation G_EXP_ONE'''

def p_G_EXP_ONE(p):
    '''G_EXP_ONE    : G_EXP_TWO G_EXP
                    | empty'''

def p_G_EXP_TWO(p):
    '''G_EXP_TWO    : LT pushOperador
                    | GT pushOperador
                    | NE pushOperador
                    | EQ pushOperador
                    | GTE pushOperador
                    | LTE pushOperador'''

def p_MID_EXP(p):
    '''MID_EXP      : TERM plusMinusExp MID_EXP_ONE'''

def p_MID_EXP_ONE(p):
    '''MID_EXP_ONE  : PLUS pushOperador MID_EXP
                    | MINUS pushOperador MID_EXP
                    | empty'''

def p_TERM(p):
    '''TERM         : FACT timesDivideExp TERM_ONE'''

def p_TERM_ONE(p):
    '''TERM_ONE     : TIMES pushOperador TERM
                    | DIVIDE pushOperador TERM
                    | empty'''
    

def p_FACT(p):
    '''FACT         : CONST 
                    | VARIABLE 
                    | OBJECT_ACCESS
                    | FUNCTION_CALL
                    | LPAREN EXP RPAREN'''


def p_CONST(p):
    '''CONST        : CTEI pushInt
                    | CTEF pushFloat
                    | CTECH pushChar'''



#------------------------------------ CODE BLOCK SYNTAX------------------------------------

def p_BLOCK(p):
    '''BLOCK        : LBRACE BLOCK_ONE RBRACE'''

def p_BLOCK_ONE(p):
    '''BLOCK_ONE    : BLOCK_STMT BLOCK_ONE
                    | empty'''

def p_BLOCK_STMT(p):
    '''BLOCK_STMT   : STMT
                    | DEC_VAR'''

def p_STMT(p):
    '''STMT         : ASSIGN_OP 
                    | OBJECT_ACCESS SEMICOLON
                    | FUNCTION_CALL SEMICOLON
                    | READ_FUNC 
                    | PRINT_FUNC 
                    | COND 
                    | WHILE_LOOP
                    | RETURN_FUNC stopFunc''' #TODO: MISSING FOR_LOOP

def p_stopFunc(p):
    '''stopFunc     : '''
    quadGenerator.generateQuad('stopFunc', None, None, None)

def p_RETURN(p):
    '''RETURN_FUNC      : RETURN RETURN_F_ONE SEMICOLON'''
    term = pOperandos.pop()
    termTipo = pTipos.pop()
    if currClass != None:
        funcTipo = objDirectory.directorio[currClass]['funcDirectory'].directorio[currFunc]['type']
    else: 
        funcTipo = funcDirectory.directorio[currFunc]['type']
    if funcTipo == 'void':
        print('No se pueder regresar un valor en func del tipo void')
        sys.exit()
    if funcTipo != termTipo:
        print('Tipo de retorno incorrecto para funcion ', currFunc)
        sys.exit()
    if currClass != None:
        objDirectory.directorio[currClass]['funcDirectory'].setReturnFlag(currFunc)
    else:
        funcDirectory.setReturnFlag(currFunc)
    vAddress = term
    if type(term) != int:
        if currClass != None:
            vAddress = objDirectory.directorio[currClass]['funcDirectory'].getVarVirtualAddress(currFunc, term)
    
        else:
            vAddress = funcDirectory.getVarVirtualAddress(currFunc, term)
    
    if currClass != None:
        quadGenerator.generateQuad('returnObj', currFunc, currClass, vAddress)
    else:
        quadGenerator.generateQuad('return', currFunc, None, vAddress)

def p_RETURN_F_ONE(p):
    '''RETURN_F_ONE     : VARIABLE
                        | EXP'''



def p_PRINT(p):
    '''PRINT_FUNC       : PRINT LPAREN EXP RPAREN SEMICOLON'''
    temp = pOperandos.pop()
    tempType = pTipos.pop()
    if type(temp) != int:
        if currClass != None:
            temp = objDirectory.directorio[currClass]['funcDirectory'].getVarVirtualAddress(currFunc, temp)
        else:
            temp = funcDirectory.getVarVirtualAddress(currFunc, temp)
    quadGenerator.generateQuad('print', None, None, temp)

def p_READ_FUNC(p):
    '''READ_FUNC        : READ LPAREN VARIABLE RPAREN SEMICOLON'''
    temp = pOperandos.pop()
    tempType = pTipos.pop()
    if type(temp) != int:
        if currClass != None:
            temp = objDirectory.directorio[currClass]['funcDirectory'].getVarVirtualAddress(currFunc, temp)
        else:
            temp = funcDirectory.getVarVirtualAddress(currFunc, temp)
    quadGenerator.generateQuad('read', None, None, temp)


def p_WHILE_LOOP(p):
    '''WHILE_LOOP     : WHILE whilePreExp LPAREN EXP RPAREN whilePostExp NESTED_BLOCK endWhile'''

def p_COND(p):
    '''COND             : IF LPAREN EXP RPAREN condExp NESTED_BLOCK COND_ONE condEnd'''

def p_COND_ONE(p):
    '''COND_ONE         : condElse ELSE NESTED_BLOCK
                        | empty'''

def p_NESTED_BLOCK(p):
    '''NESTED_BLOCK     : LBRACE NESTED_B_ONE RBRACE'''

def p_NESTED_B_ONE(p):
    '''NESTED_B_ONE     : STMT NESTED_B_ONE
                        | empty'''


#------------------------------------ NEURAL POINTS ------------------------------------

#------------------------------------ PROGRAM NEURAL POINTS ----------------------------

def p_startProgram(p):
    '''startProgram     :'''
    quadGenerator.generateQuad('gotoM', 'main', None, None)
    pSaltos.append(quadGenerator.counter)
    funcDirectory.addFunction('program', None)

def p_endProgram(p):
    '''endProgram       :'''
    funcDirectory.setNumVars('program', counterGlobales)
    funcDirectory.setNumTemp('program', counterConstantes) #en este caso son las constantes
    quadGenerator.generateQuad('END', None, None, None)

#------------------------------------ VARIABLES NEURAL POINTS ----------------------------

def p_addVar(p):
    '''addVar           : '''
    varName = p[-1]
    global currVar
    currVar = varName
    if currScope == 'local':
        vAddress = localVirtualAddress(currTypeVar)
        if currClass != None:
            objDirectory.directorio[currClass]['funcDirectory'].addVar(currFunc, varName, currTypeVar, vAddress)
        else:
            funcDirectory.addVar(currFunc, varName, currTypeVar, vAddress)
    elif currScope == 'global':
        globalVirtualAddress(varName, currTypeVar)
    
def p_pushVar(p):
    '''pushVar              : '''
    varId = p[-1]
    #get type using function name
    if currClass != None:
        varInfo = objDirectory.directorio[currClass]['funcDirectory'].getVar(currFunc, varId)
    else:
        varInfo = funcDirectory.getVar(currFunc, varId)
    pOperandos.append(varId)
    pTipos.append(varInfo['type'])
#------------------------------------ EXP NEURAL POINTS ----------------------------

def p_pushOperador(p):
    '''pushOperador     : '''
    oper = p[-1]
    pOperadores.append(oper)

def p_pushInt(p):
    '''pushInt         :'''
    const = p[-1]
    constType = 'int'
    constantVirtualAddress(const, constType, typesIndex[constType])

def p_pushFloat(p):
    '''pushFloat        :'''
    const = p[-1]
    constType = 'float'
    constantVirtualAddress(const, constType, typesIndex[constType])

def p_pushChar(p):
    '''pushChar         :'''
    const = p[-1]
    constType = 'char'
    constantVirtualAddress(const, constType, typesIndex[constType])

def expQuad():
    rOperand = pOperandos.pop()
    rType = pTipos.pop()
    lOperand = pOperandos.pop()
    lType = pTipos.pop()
    oper = pOperadores.pop()
    resultType = cubo.getType(lType, rType, oper)
    if resultType == 'error':
        print('type mismatch')
        sys.exit()
    res = temporalVirtualAddress(resultType)
    if type(lOperand) != int:
        if currClass != None:
            lOperand = objDirectory.directorio[currClass]['funcDirectory'].getVarVirtualAddress(currFunc, lOperand)
        else:
            lOperand = funcDirectory.getVarVirtualAddress(currFunc, lOperand)
    if type(rOperand) != int:
        if currClass != None:
            rOperand = objDirectory.directorio[currClass]['funcDirectory'].getVarVirtualAddress(currFunc, rOperand)
        else:
            rOperand = funcDirectory.getVarVirtualAddress(currFunc, rOperand)
    quadGenerator.generateQuad(oper, lOperand, rOperand, res)
    pOperandos.append(res)
    pTipos.append(resultType)

def p_plusMinusExp(p):
    '''plusMinusExp      : '''
    if len(pOperadores) == 0: 
        return
    if pOperadores[-1] == '+' or pOperadores[-1] == '-':
        expQuad()

def p_timesDivideExp(p):
    '''timesDivideExp      : '''
    if len(pOperadores) == 0: 
        return
    if pOperadores[-1] == '*' or pOperadores[-1] == '/':
        expQuad()
    
def p_relationalOperation(p):
    '''relationalOperation  :'''
    if len(pOperadores) == 0:
        return
    if pOperadores[-1] in relationalOperators:
        expQuad()

def p_logicalOrOperation(p):
    '''logicalOrOperation     :'''
    if len(pOperadores) == 0:
        return
    if pOperadores[-1] == '||':
        expQuad()

def p_logicalAndOperation(p):
    '''logicalAndOperation     :'''
    if len(pOperadores) == 0:
        return
    if pOperadores[-1] == '&&':
        expQuad()

#------------------------------------ COND NEURAL POINTS ----------------------------     

def quadGoToF():
    expType = pTipos.pop()
    if expType != 'bool':
        print('Type mismatch in expression condition, must be a bool!')
        sys.exit()
    res = pOperandos.pop()
    if type(res) != int:
        if currClass != None:
            res = objDirectory.directorio[currClass]['funcDirectory'].getVarVirtualAddress(currFunc, res)
        else:
            res = funcDirectory.getVarVirtualAddress(currFunc, res)
    quadGenerator.generateQuad('gotoF', res, None, -1)
    pSaltos.append(quadGenerator.counter)

def p_condExp(p):
    '''condExp          :'''
    quadGoToF()

def p_condElse(p):
    '''condElse         :'''
    quadGenerator.generateQuad('goto', None, None, -1)
    false = pSaltos.pop()
    pSaltos.append(quadGenerator.counter)
    quadGenerator.updateJump(false)

def p_condEnd(p):
    '''condEnd          :'''
    end = pSaltos.pop()
    quadGenerator.updateJump(end)

#------------------------------------ WHILE NEURAL POINTS ---------------------------- 

def p_whilePreExp(p):
    '''whilePreExp          :'''
    pSaltos.append(quadGenerator.counter + 1)

def p_whilePostExp(p):
    '''whilePostExp         :'''
    quadGoToF()

def p_endWhile(p):
    '''endWhile             :'''
    end = pSaltos.pop()
    ret = pSaltos.pop() #return to evaluate expression
    quadGenerator.generateQuad('goto', None, None, ret)
    quadGenerator.updateJump(end)

#------------------------------------ FUNCTION NEURAL POINTS ----------------------------

def p_addFunc(p):
    '''addFunc          : '''
    global currFunc 
    functionName = p[-1]
    if currClass != None:
        if not objDirectory.directorio[currClass]['funcDirectory'].functionExists(functionName):
            objDirectory.directorio[currClass]['funcDirectory'].addFunction(functionName, currTypeFunc)
            #añadimos variable global con mismo nombre si no es void
            if currTypeFunc != 'void':
                address = globalVirtualAddress(functionName, currTypeFunc)
                objDirectory.directorio[currClass]['funcDirectory'].setGlobalReturnAddress(functionName, address)
            
            currFunc = functionName
    else:
        if not funcDirectory.functionExists(functionName):
            funcDirectory.addFunction(functionName, currTypeFunc)
            #añadimos variable global con mismo nombre si no es void
            if currTypeFunc != 'void':
                address = globalVirtualAddress(functionName, currTypeFunc)
                funcDirectory.setGlobalReturnAddress(functionName, address) 
            currFunc = functionName
            global currScope
            currScope = 'local'

def p_addMain(p):
    '''addMain          : '''
    funcDirectory.addFunction('main', 'void')
    mainGoto = pSaltos.pop()
    quadGenerator.updateJump(mainGoto)
    global currFunc
    currFunc = 'main'
    global currScope
    currScope = 'local'

def p_addParam(p):
    '''addParam         : '''
    varName = p[-1]
    vAddress = localVirtualAddress(currTypeVar)
    if currClass != None:
        objDirectory.directorio[currClass]['funcDirectory'].addVar(currFunc, varName, currTypeVar, vAddress)
        objDirectory.directorio[currClass]['funcDirectory'].addParam(currFunc, currTypeVar, varName)
    else:
        funcDirectory.addVar(currFunc, varName, currTypeVar, vAddress)
        funcDirectory.addParam(currFunc, currTypeVar, varName)

def p_setNumParams(p):
    '''setNumParams     : '''
    if currClass != None:
        objDirectory.directorio[currClass]['funcDirectory'].setNumParams(currFunc)
    else:
        funcDirectory.setNumParams(currFunc)

def p_setFuncCounter(p):
    '''setFuncCounter   : '''
    nextQuad = quadGenerator.counter + 1
    if currClass != None:
        objDirectory.directorio[currClass]['funcDirectory'].setStartCounter(currFunc, nextQuad)
    else:
        funcDirectory.setStartCounter(currFunc, nextQuad)

def p_endFunc(p):
    '''endFunc          : '''
    #globales a usar
    global currFunc, counterLocales, dirBasePointers, counterTemporales
    if currClass != None:
        funcTipo = objDirectory.directorio[currClass]['funcDirectory'].directorio[currFunc]['type']
        returnFlag = objDirectory.directorio[currClass]['funcDirectory'].directorio[currFunc]['return']
    else:
        funcTipo = funcDirectory.directorio[currFunc]['type']
        returnFlag = funcDirectory.directorio[currFunc]['return']
    if funcTipo != 'void' and not returnFlag:
        print('Falta valor de retorno para funcion ', currFunc)
        sys.exit()
    if currFunc != 'main':
        quadGenerator.generateQuad('ENDFUNC', None, None, None)
        #Set number for memory use
    if currClass != None:
        objDirectory.directorio[currClass]['funcDirectory'].setNumTemp(currFunc, counterTemporales)
        objDirectory.directorio[currClass]['funcDirectory'].setNumVars(currFunc, counterLocales)
        objDirectory.directorio[currClass]['funcDirectory'].setNumPointer(currFunc, dirBasePointers - 30000)
    else:
        funcDirectory.setNumTemp(currFunc, counterTemporales)
        funcDirectory.setNumVars(currFunc, counterLocales)
        funcDirectory.setNumPointer(currFunc, dirBasePointers - 30000)
    counterTemporales = [0,0,0,0] #reset temporales
    counterLocales = [0,0,0,0] #reset locales
    dirBasePointers = 30000 # reset pointers
    currFunc = 'program'
    global currScope
    currScope = 'global'



def p_verifyFunction(p):
    '''verifyFunction   : '''
    if subFunc:
        funcName = currVarObj
        if not objDirectory.directorio[currTypeVar]['funcDirectory'].functionExists(funcName):
            print('Metodo de objeto', funcName, ' no existe')
            sys.exit()
        quadGenerator.generateQuad('ERAOBJ', currTypeVar, None, funcName)
    else:
        funcName = p[-1]
        if not funcDirectory.functionExists(funcName):
            print('Metodo ', funcName, ' no existe')
            sys.exit()
        quadGenerator.generateQuad('ERA', None, None, funcName)
    global currFuncCall
    currFuncCall = funcName
    global kParam
    kParam = 0

def p_verifyParam(p):
    '''verifyParam      : '''
    global kParam
    operando = pOperandos.pop()
    tipo = pTipos.pop()
    if subFunc:
        tipoParam = objDirectory.directorio[currTypeVar]['funcDirectory'].getParamType(currFuncCall, kParam)
        paramName = objDirectory.directorio[currTypeVar]['funcDirectory'].getParamName(currFuncCall, kParam)
    else:
        tipoParam = funcDirectory.getParamType(currFuncCall, kParam)
        paramName = funcDirectory.getParamName(currFuncCall, kParam)
    if tipo != tipoParam:
        print('Error en el param ', kParam + 1, ' de la funcion ', currFuncCall)
        sys.exit()
    if type(operando) != int:
        if subFunc:
            operando = objDirectory.directorio[currTypeVar]['funcDirectory'].getVarVirtualAddress(currFunc, operando)
        else:    
            operando = funcDirectory.getVarVirtualAddress(currFunc, operando)
    if subFunc:
        vAddress = objDirectory.directorio[currTypeVar]['funcDirectory'].getVarVirtualAddress(currFuncCall, paramName)
    else:        
        vAddress = funcDirectory.getVarVirtualAddress(currFuncCall, paramName)
    kParam = kParam + 1
    quadGenerator.generateQuad('PARAM', operando, None, vAddress)

def p_verifyNumParams(p):
    '''verifyNumParams      : '''
    if subFunc:
        numParam = objDirectory.directorio[currTypeVar]['funcDirectory'].directorio[currFuncCall]['numParams']
    else:
        numParam = funcDirectory.directorio[currFuncCall]['numParams']
    if not kParam == numParam:
        print('Numero de parametros incorrecto en funcion ', currFuncCall)
        sys.exit()

def p_gosubFunc(p):
    '''gosubFunc        : '''
    global subFunc
    if subFunc:
        quadNum = objDirectory.directorio[currTypeVar]['funcDirectory'].directorio[currFuncCall]['startCounter']
        funcTipo = objDirectory.directorio[currTypeVar]['funcDirectory'].directorio[currFuncCall]['type']
    else:
        quadNum = funcDirectory.directorio[currFuncCall]['startCounter']
        funcTipo = funcDirectory.directorio[currFuncCall]['type']
    quadGenerator.generateQuad('GOSUB', currFuncCall, None, quadNum)
    if funcTipo != 'void':
        res = temporalVirtualAddress(funcTipo)
        if subFunc:
            vAddress = objDirectory.directorio[currTypeVar]['funcDirectory'].getVarVirtualAddress('program', currFuncCall)    
        else:
            vAddress = funcDirectory.getVarVirtualAddress('program', currFuncCall)
        
        quadGenerator.generateQuad('=', vAddress, None, res)
        pOperandos.append(res)
        pTipos.append(funcTipo)
    subFunc = False

#------------------------------------ ARRAYS NEURAL POINTS ----------------------------

def p_addDimVar(p):
    '''addDimVar       : '''
    funcName = 'program'
    if currScope != 'global':
        funcName = currFunc
    dimSize = p[-1]
    if currClass != None:
        objDirectory.directorio[currClass]['funcDirectory'].addDimToVar(funcName, currVar, dimSize)
    else:
        funcDirectory.addDimToVar(funcName, currVar, dimSize)

def p_arrDeclarationCalc(p):
    '''arrDeclarationCalc   : '''
    '''addDimVar       : '''
    funcName = 'program'
    if currScope != 'global':
        funcName = currFunc
    if currClass != None:
        objDirectory.directorio[currClass]['funcDirectory'].dimPostDeclarationCalc(funcName, currVar)
        sizeDimVar = objDirectory.directorio[currClass]['funcDirectory'].getVarSize(funcName, currVar)
    else:
        funcDirectory.dimPostDeclarationCalc(funcName, currVar)
        sizeDimVar = funcDirectory.getVarSize(funcName, currVar)
    index = typesIndex[currTypeVar]
    if currScope != 'global':
        global counterLocales
        counterLocales[index] = counterLocales[index] + sizeDimVar - 1
    else:
        global counterGlobales
        counterGlobales[index] = counterGlobales[index] + sizeDimVar - 1

def p_arrVarCall(p):
    '''verifyArray          : '''
    varName = pOperandos.pop()
    _ = pTipos.pop()
    global currVar
    currVar = varName
    funcName = 'program'
    if currScope != 'global':
        funcName = currFunc
    if currClass != None:
        if not objDirectory.directorio[currClass]['funcDirectory'].checkVarIsDim(funcName, varName):
            print('La variable', varName, 'no tiene dimensiones')
            sys.exit()
        node = objDirectory.directorio[currClass]['funcDirectory'].getVarDimNode(currFunc, currVar)
    else:
        if not funcDirectory.checkVarIsDim(funcName, varName):
            print('La variable', varName, 'no tiene dimensiones')
            sys.exit()
        node = funcDirectory.getVarDimNode(currFunc, currVar)
    dim = 1
    pNodos.append(node)
    pDims.append((varName, dim))
    pOperadores.append('fB') #pushing fake bottom

def p_createArrayQuads(p):
    '''createArrayQuads     : '''
    node = pNodos[-1]
    val = pOperandos[-1]
    if type(val) != int:
        if currClass != None:
            val = objDirectory.directorio[currClass]['funcDirectory'].getVarVirtualAddress(currFunc, val)
        else:
            val = funcDirectory.getVarVirtualAddress(currFunc, val)
    quadGenerator.generateQuad('verify', val, node.lInf, node.lSup)
    if node.next:
        aux = pOperandos.pop()
        _ = pTipos.pop()
        temp = temporalVirtualAddress('int')
        if type(aux) != int:
            if currClass != None:
                aux = objDirectory.directorio[currClass]['funcDirectory'].getVarVirtualAddress(currFunc, aux)
            else:
                aux = funcDirectory.getVarVirtualAddress(currFunc, aux)
        vAddress = constantVirtualAddress(int(node.m), 'int', typesIndex['int'])
        pOperandos.pop()
        pTipos.pop()
        quadGenerator.generateQuad('*', aux, vAddress, temp)
        pOperandos.append(temp)
        pTipos.append('int')
    dim = pDims[-1]
    dim = dim[1]
    if dim > 1:
        aux2 = pOperandos.pop()
        _ = pTipos.pop()
        aux1 = pOperandos.pop()
        _ = pTipos.pop()
        temp2 = temporalVirtualAddress('int')
        if type(aux1) != int:
            if currClass != None:
                aux1 = objDirectory.directorio[currClass]['funcDirectory'].getVarVirtualAddress(currFunc, aux1)
            else:
                aux1 = funcDirectory.getVarVirtualAddress(currFunc, aux1)
        if type(aux2) != int:
            if currClass != None:
                aux2 = objDirectory.directorio[currClass]['funcDirectory'].getVarVirtualAddress(currFunc, aux2)
            else:
                aux2 = funcDirectory.getVarVirtualAddress(currFunc, aux2)
        quadGenerator.generateQuad('+', aux1, aux2, temp2)
        pOperandos.append(temp2)
        pTipos.append('int')
    
def p_updateDimArray(p):
    '''updateDimArray       : '''
    node = pNodos.pop()
    dim = pDims.pop()
    if node.next == None:
        print('Indexacion incorrecta verifique dimensiones en variable', dim[0])
        sys.exit()
    dim = (dim[0], dim[1] + 1)
    pDims.append(dim)
    pNodos.append(node.next)

def p_createLastArrayQuads(p):
    '''createLastArrayQuads     : '''
    aux1 = pOperandos.pop()
    temp = temporalVirtualAddress('int')
    node = pNodos.pop()
    if type(aux1) != int:
        if currClass != None:
            aux1 = objDirectory.directorio[currClass]['funcDirectory'].getVarVirtualAddress(currFunc, aux1)
        else:
            aux1 = funcDirectory.getVarVirtualAddress(currFunc, aux1)
    global dirBasePointers
    temp2 = dirBasePointers
    dirBasePointers = dirBasePointers + 1
    #Obtener direccion base usando var de pila de dims
    varName = pDims[-1]
    varName = varName[0] 
    if currClass != None:
        baseAddress = objDirectory.directorio[currClass]['funcDirectory'].getVarVirtualAddress(currFunc, varName)
    else:
        baseAddress = funcDirectory.getVarVirtualAddress(currFunc, varName)
    quadGenerator.generateQuad('addBaseAdd', aux1, baseAddress, temp2)
    pOperandos.append(temp2)
    pOperadores.pop()#remove fake bottom
    #Verify correct dims
    dims = pDims.pop()
    if currClass != None:
        trueDims = objDirectory.directorio[currClass]['funcDirectory'].getVar(currFunc, dims[0])['dim']
    else:
        trueDims = funcDirectory.getVar(currFunc, dims[0])['dim']
    if trueDims != dims[1]:
        print('Indexacion incorrecta verifique dimensiones en variable', dims[0])
        sys.exit()

#------------------------------------ VIRTUAL ADDRESES ----------------------------     

def constantVirtualAddress(const, constType, index):
    global counterConstantes, constants
    offset = counterConstantes[index]
    baseAddress = dirBasesConstantes[constType]
    address = baseAddress + offset
    counterConstantes[index] = offset + 1
    pOperandos.append(address)
    pTipos.append(constType)
    constInfo = (const, address)
    constants.append(constInfo)
    return address


def globalVirtualAddress(varName, varType):
    global counterGlobales
    index = typesIndex[varType]
    offset = counterGlobales[index]
    baseAddress = dirBasesGlobales[varType]
    address = baseAddress + offset
    counterGlobales[index] = offset + 1
    if currClass != None:
        objDirectory.directorio[currClass]['funcDirectory'].addVar('program', varName, varType, address)
    else:
        funcDirectory.addVar('program', varName, varType, address)
    return address

def temporalVirtualAddress(termType):
    global counterTemporales
    index = typesIndex[termType]
    offset = counterTemporales[index]
    baseAddress = dirBasesTemporales[termType]
    address = baseAddress + offset
    counterTemporales[index] = offset + 1
    return address

def localVirtualAddress(termType):
    global counterLocales
    index = typesIndex[termType]
    offset = counterLocales[index]
    baseAddress = dirBasesLocales[termType]
    address = baseAddress + offset
    counterLocales[index] = offset + 1
    return address

#------------------------------------ MANAGE OF STACKS ----------------------------
def printPOperandos():
    print('Pila de operandos ', pOperandos)

def printPOperadores():
    print('Pila de operadores', pOperadores)

def printPTipos():
    print('Pila de tipos', pTipos)

#------------------------------------ CLASS NEURAL POINTS ----------------------------

def p_addClass(p):
    '''addClass         : '''
    #guardamos las variables globales actuales
    global currClass, counterConstantes, counterGlobales, auxCounterGlobales
    funcDirectory.setNumVars('program', counterGlobales)
    funcDirectory.setNumTemp('program', counterConstantes)
    auxCounterGlobales = counterGlobales
    counterGlobales = [0,0,0,0]
    className = p[-1]
    currClass = className
    objDirectory.addObject(className)
    objDirectory.directorio[currClass]['funcDirectory'].addFunction('program', None)
    

def p_addClassConstructor(p):
    '''addClassConstructor      : '''
    funcType = 'void'
    funcName = currClass
    objDirectory.directorio[currClass]['funcDirectory'].addFunction(funcName, funcType)
    global currFunc 
    currFunc = funcName
    global currScope
    currScope = 'local'

def p_constructorParam(p):
    '''constructorParam         : '''
    objDirectory.directorio[currClass]['funcDirectory'].setNumParams(currFunc)

def p_endClass(p):
    '''endClass         : '''
    global currScope, currClass, counterConstantes, counterGlobales
    currScope = 'global'
    objDirectory.directorio[currClass]['funcDirectory'].setNumVars('program', counterGlobales)
    objDirectory.directorio[currClass]['funcDirectory'].setNumTemp('program', counterConstantes)
    currClass = None
    counterGlobales = auxCounterGlobales

def p_checkClassName(p):
    '''checkClassName   : '''
    className = p[-1]
    if className not in objDirectory.directorio.keys():
        print('Clase',className, 'no existe')
        sys.exit()
    global currTypeVar
    currTypeVar = className

def p_addComplexVar(p):
    '''addComplexVar    : '''
    #TODO: Allow complex types in Classes
    objName = p[-1]
    funcDirectory.addComplexVar(currFunc, objName, currTypeVar)
    objVarTable = objDirectory.getObjectVars(currTypeVar)
    for var in objVarTable.table.keys():
        varType = objVarTable.table[var]['type']
        vAddress = localVirtualAddress(varType)
        funcDirectory.addObjectVar(currFunc, objName, var, varType, vAddress)
    

#EMPTY
def p_empty(p):
    'empty :'
    pass

#ERROR
def p_error(p):
    print('error de sintaxis')
    print(p)
    sys.exit()

#BUILD THE PARSER
parser = yacc.yacc()


#Function to create the object code
#We destroy all var tables and mantain function names and some info; 
#constants and all quads

def createObjCode():
    f = open('interCode.txt', 'w')
    quads = quadGenerator.quadsTable
    f.write('QUADS-START')
    f.write('\n')
    for quad in quads:
        f.write(str(quad))
        f.write('\n')
    f.write('QUADS-END')
    f.write('\n')
    f.write('FUNC-INFO-START')
    f.write('\n')
    for func in funcDirectory.directorio.keys():
        f.write(str(funcDirectory.interCodeInfo(func)))
        f.write('\n')
    f.write('FUNC-INFO-END')
    f.write('\n')
    f.write('OBJ-INFO-START')
    f.write('\n')
    for obj in objDirectory.directorio.keys():
        f.write(str(objDirectory.getObjectInfo(obj)))
        f.write('\n')
    f.write('OBJ-INFO-END')
    f.write('\n')
    f.write('CONST-INFO-START')
    f.write('\n')
    for constInfo in constants:
        f.write(str(constInfo))
        f.write('\n')
    f.write('CONST-INFO-END')
    f.close()



if __name__ == '__main__':
    if (len(sys.argv) > 1):
        file = sys.argv[1]
        with open(file, 'r') as f:
            input = f.read()
            #parser.parse(input)
            parser.parse(input)
            print('apropiado')
            createObjCode()
            #print(funcDirectory.directorio['num'])
            #print(funcDirectory.directorio['num']['vars'].table)
            #print(funcDirectory.directorio['num']['vars'].table['t1']['vars'].table)
    else:
        print('File missing')