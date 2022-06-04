import ply.yacc as yacc
from Avail import Avail
from lexer import tokens
from DirectorioFunciones import DirectorioFunciones
from QuadGenerator import QuadGenerator
from CuboSemantico import SemanticCube
from Memoria import dirBasesConstantes, dirBasesGlobales, dirBasesLocales, dirBasesTemporales
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
currTypeFunc = None
currFunc = None
currFuncCall = None
currScope = 'global'
currNode = None
kParam = 0
counterConstantes = [0,0,0,0]
counterGlobales = [0,0,0,0]
counterLocales = [0,0,0,0]
counterTemporales = [0,0,0,0]

start = 'P'

#------------------------------------ INSTANTIATE NEEDED DATA STR ------------------------------------

funcDirectory = DirectorioFunciones()
quadGenerator = QuadGenerator()
cubo = SemanticCube()
avail = Avail()
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

#TODO: Remove import rules from language and from diagram

def p_PROGRAM(p):
    '''P            : PROGRAM ID startProgram SEMICOLON P_STRUCTURE MAIN_FUNC endProgram'''

def p_P_STRUCTURE(p):
    '''P_STRUCTURE  : P_STR_ONE PROG_MEMBERS PROG_M_ONE'''

def p_P_STR_ONE(p): #tal vez quitar
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
    '''CLASS_STR    : CLASS_DEC LBRACE CLASS_BODY RBRACE'''

def p_CLASS_DEC(p):
    '''CLASS_DEC    : CLASS ID CLASS_DEC_ONE'''

def p_CLASS_DEC_ONE(p):
    '''CLASS_DEC_ONE    : CLASS_INHERITS
                        | empty'''

def p_CLASS_INHERITS(p):
    '''CLASS_INHERITS   : DERIVES ID'''

def p_CLASS_BODY(p):
    '''CLASS_BODY       : CLASS_CONSTRUCTOR CLASS_BODY_MEMBER CLASS_B_M_ONE'''

def p_CLASS_B_M_ONE(p):
    '''CLASS_B_M_ONE    : CLASS_BODY_MEMBER CLASS_B_M_ONE
                        | empty'''

def p_CLASS_BODY_MEMBER(p):
    '''CLASS_BODY_MEMBER    : FUNCTION
                            | DEC_VAR'''

def p_CLASS_CONSTRUCTOR(p):
    '''CLASS_CONSTRUCTOR    : ID LPAREN CLASS_C_ONE RPAREN BLOCK'''

def p_CLASS_C_ONE(p):
    '''CLASS_C_ONE          : PARAM
                            | empty'''

def p_FIELD_ACCESS(p):
    '''FIELD_ACCESS         : ID POINT ID'''

#------------------------------------ FUNCTION SYNTAX ------------------------------------

def p_FUNCTION_ACCESS(p):
    '''FUNCTION_ACCESS      : ID POINT FUNCTION_CALL'''

def p_FUNCTION_CALL(p): #TODO ANALYZE CREATING ONE FOR VOID ONLY
    '''FUNCTION_CALL        : ID verifyFunction LPAREN FUNCTION_C_ONE verifyNumParams RPAREN gosubFunc'''

def p_FUNCTION_C_ONE(p):
    '''FUNCTION_C_ONE       : EXP verifyParam FUNCTION_C_TWO
                            | empty'''

def p_FUNCTION_C_TWO(p):
    '''FUNCTION_C_TWO       : COMMA EXP verifyParam FUNCTION_C_TWO
                            | empty'''

def p_FUNCTION_DEC(p): #CHECK IF SET CURR IS OK THERE
    '''FUNCTION_DEC         : FUNC FUNCTION_D_ONE ID addFunc LPAREN FUNCTION_D_TWO RPAREN setNumParams'''

def p_MAIN_FUNC(p):
    '''MAIN_FUNC            : MAIN addMain LPAREN RPAREN BLOCK'''

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

def p_VARIABLE(p): #TODO: Check if braces for access is there
    '''VARIABLE             : ID pushVar VARIABLE_ONE
                            | FIELD_ACCESS'''
#TODO move to correct area
def p_pushVar(p):
    '''pushVar              : '''
    varId = p[-1]
    
    #get type using function name
    varInfo = funcDirectory.getVar(currFunc, varId)
    pOperandos.append(varId)
    pTipos.append(varInfo['type'])

def p_VARIABLE_ONE(p): #TODO: this allows multiple index, more than matrix check
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
        vAddress = funcDirectory.getVarVirtualAddress(currFunc, temp)
    if type(varId) != int:
        vAddress2 = funcDirectory.getVarVirtualAddress(currFunc, varId)
    quadGenerator.generateQuad(p[2], vAddress, None, vAddress2)
    

def p_DEC_VAR(p):
    '''DEC_VAR              : VAR DEC_VAR_ONE SEMICOLON'''

def p_DEC_VAR_ONE(p):
    '''DEC_VAR_ONE          : COMPLEX_TYPE ID DEC_V_O_COMPLEX
                            | SIMPLE_TYPE ID addVar DEC_ARR DEC_V_O_SIMPLE'''

def p_DEC_V_O_SIMPLE(p):
    '''DEC_V_O_SIMPLE       : COMMA ID addVar DEC_ARR DEC_V_O_SIMPLE
                            | empty'''
                    
def p_DEC_ARR(p):
    '''DEC_ARR              : LSBRACKET CTEI addDimVar RSBRACKET DEC_ARR_ONE arrDeclarationCalc
                            | empty'''
#TODO: Analyze using more dims than two
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
    '''COMPLEX_TYPE         : ID'''

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
                    | FUNCTION_CALL 
                    | LPAREN EXP RPAREN''' #TODO: MISSING CHARS IN LEXER

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
                    | FUNCTION_CALL SEMICOLON
                    | READ_FUNC 
                    | PRINT_FUNC 
                    | COND 
                    | WHILE_LOOP
                    | RETURN_FUNC''' #TODO: MISSING RETURN AND FOR_LOOP

def p_RETURN(p):
    '''RETURN_FUNC      : RETURN RETURN_F_ONE SEMICOLON'''
    term = pOperandos.pop()
    termTipo = pTipos.pop()
    funcTipo = funcDirectory.directorio[currFunc]['type']
    if funcTipo == 'void':
        print('No se pueder regresar un valor en func del tipo void')
        sys.exit()
    if funcTipo != termTipo:
        print('Tipo de retorno incorrecto para funcion ', currFunc)
        sys.exit()
    funcDirectory.setReturnFlag(currFunc)
    vAddress = term
    if type(term) != int:
        vAddress = funcDirectory.getVarVirtualAddress(currFunc, term)
    quadGenerator.generateQuad('return', None, None, vAddress)

def p_RETURN_F_ONE(p):
    '''RETURN_F_ONE     : VARIABLE
                        | EXP'''

def p_PRINT(p):
    '''PRINT_FUNC       : PRINT LPAREN EXP RPAREN SEMICOLON'''
    temp = pOperandos.pop()
    tempType = pTipos.pop()
    quadGenerator.generateQuad('print', None, None, temp)

def p_READ_FUNC(p):
    '''READ_FUNC        : READ VARIABLE SEMICOLON'''

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
    quadGenerator.generateQuad('goto', 'main', None, None)
    pSaltos.append(quadGenerator.counter)
    funcDirectory.addFunction('program', None)

def p_endProgram(p):
    '''endProgram       :'''
    quadGenerator.generateQuad('END', None, None, None)

#------------------------------------ VARIABLES NEURAL POINTS ----------------------------

def p_addVar(p):
    '''addVar           : '''
    varName = p[-1]
    global currVar
    currVar = varName
    if currScope == 'local':
        vAddress = localVirtualAddress(currTypeVar)
        funcDirectory.addVar(currFunc, varName, currTypeVar, vAddress)
    elif currScope == 'global':
        globalVirtualAddress(varName, currTypeVar)
    
#------------------------------------ EXP NEURAL POINTS ----------------------------

def p_pushOperador(p):
    '''pushOperador     : '''
    oper = p[-1]
    pOperadores.append(oper)

def p_pushInt(p):
    '''pushInt         :'''
    const = p[-1]
    constType = 'int'
    constantVirtualAddress(constType, typesIndex[constType])

def p_pushFloat(p):
    '''pushFloat        :'''
    const = p[-1]
    constType = 'float'
    constantVirtualAddress(constType, typesIndex[constType])

def p_pushChar(p):
    '''pushChar         :'''
    const = p[-1]
    constType = 'char'
    constantVirtualAddress(constType, typesIndex[constType])

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
    quadGenerator.generateQuad(oper, lOperand, rOperand, res)
    pOperandos.append(res)
    pTipos.append(resultType)
    #TODO: return to avail temps

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
    functionName = p[-1]
    if not funcDirectory.functionExists(functionName):
        funcDirectory.addFunction(functionName, currTypeFunc)
        #print('Func added to directory')
        #print(funcDirectory.directorio)
        global currFunc 
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
    funcDirectory.addVar(currFunc, varName, currTypeVar, vAddress)
    funcDirectory.addParam(currFunc, currTypeVar)

def p_setNumParams(p):
    '''setNumParams     : '''
    funcDirectory.setNumParams(currFunc)

def p_setFuncCounter(p):
    '''setFuncCounter   : '''
    nextQuad = quadGenerator.counter + 1
    funcDirectory.setStartCounter(currFunc, nextQuad)

def p_endFunc(p):
    '''endFunc          : '''
    global currFunc
    funcTipo = funcDirectory.directorio[currFunc]['type']
    returnFlag = funcDirectory.directorio[currFunc]['return']
    if funcTipo != 'void' and not returnFlag:
        print('Falta valor de retorno para funcion ', currFunc)
        sys.exit()
    quadGenerator.generateQuad('ENDFUNC', None, None, None)
    #TODO: Release var table
    global counterTemporales
    numTemps = counterTemporales
    funcDirectory.setNumTemp(currFunc, numTemps)
    counterTemporales = [0,0,0,0] #reset temporales
    currFunc = 'program'
    global currScope
    currScope = 'global'


def p_verifyFunction(p):
    '''verifyFunction   : '''
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
    tipoParam = funcDirectory.getParamType(currFuncCall, kParam)
    if tipo != tipoParam:
        print('Error en el param ', kParam + 1, ' de la funcion ', currFuncCall)
        sys.exit()
    paramKString = 'param' + str(kParam + 1)
    kParam = kParam + 1
    quadGenerator.generateQuad('PARAM', operando, None, paramKString)

def p_verifyNumParams(p):
    '''verifyNumParams      : '''
    if not kParam == funcDirectory.directorio[currFuncCall]['numParams']:
        print('Numero de parametros incorrecto en funcion ', currFuncCall)
        sys.exit()

def p_gosubFunc(p):
    '''gosubFunc        : '''
    quadNum = funcDirectory.directorio[currFuncCall]['startCounter']
    quadGenerator.generateQuad('GOSUB', currFuncCall, None, quadNum)

#------------------------------------ ARRAYS NEURAL POINTS ----------------------------

def p_addDimVar(p):
    '''addDimVar       : '''
    funcName = 'program'
    if currScope != 'global':
        funcName = currFunc
    dimSize = p[-1]
    funcDirectory.addDimToVar(funcName, currVar, dimSize)

def p_arrDeclarationCalc(p):
    '''arrDeclarationCalc   : '''
    '''addDimVar       : '''
    funcName = 'program'
    if currScope != 'global':
        funcName = currFunc
    funcDirectory.dimPostDeclarationCalc(funcName, currVar)
    #TODO: Store vAddress

def p_arrVarCall(p):
    '''verifyArray          : '''
    varName = pOperandos.pop()
    _ = pTipos.pop()
    global currVar
    currVar = varName
    funcName = 'program'
    if currScope != 'global':
        funcName = currFunc
    if not funcDirectory.checkVarIsDim(funcName, varName):
        print('La variable', varName, 'no tiene dimensiones')
        sys.exit()
    dim = 1
    node = funcDirectory.getVarDimNode(currFunc, currVar)
    pNodos.append(node)
    pDims.append((varName, dim))
    pOperadores.append('fB') #pushing fake bottom

def p_createArrayQuads(p):
    '''createArrayQuads     : '''
    node = pNodos[-1]
    val = pOperandos[-1]
    quadGenerator.generateQuad('verify', val, node.lInf, node.lSup)
    if node.next:
        aux = pOperandos.pop()
        _ = pTipos.pop()
        temp = temporalVirtualAddress('int')
        quadGenerator.generateQuad('*', aux, node.m, temp)
        pOperandos.append(temp)
    dim = pDims[-1]
    dim = dim[1]
    if dim > 1:
        aux2 = pOperandos.pop()
        #_ = pTipos.pop()
        aux1 = pOperandos.pop()
        #_ = pTipos.pop()
        temp2 = temporalVirtualAddress('int')
        quadGenerator.generateQuad('+', aux1, aux2, temp2)
        pOperandos.append(temp2)
    
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
    quadGenerator.generateQuad('+', aux1, node.m, temp)
    temp2 = '(' + avail.next() + ')' #TODO: put pointer here
    quadGenerator.generateQuad('+', temp, 1000, temp2)
    pOperandos.append(temp2)
    pOperadores.pop()#remove fake bottom
    #Verify correct dims
    dims = pDims.pop()
    trueDims = funcDirectory.getVar(currFunc, dims[0])['dim']
    if trueDims != dims[1]:
        print('Indexacion incorrecta verifique dimensiones en variable', dims[0])
        sys.exit()

#------------------------------------ STMT NEURAL POINTS ----------------------------

def p_readFunc(p):
    '''readFunc         : '''
    pass

#------------------------------------ VIRTUAL ADDRESES ----------------------------     

def constantVirtualAddress(constType, index):
    global counterConstantes
    offset = counterConstantes[index]
    baseAddress = dirBasesConstantes[constType]
    address = baseAddress + offset
    counterConstantes[index] = offset + 1
    pOperandos.append(address)
    pTipos.append(constType)

def globalVirtualAddress(varName, varType):
    global counterGlobales
    index = typesIndex[varType]
    offset = counterGlobales[index]
    baseAddress = dirBasesGlobales[varType]
    address = baseAddress + offset
    counterGlobales[index] = offset + 1
    funcDirectory.addVar('program', varName, varType, address)

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


#EMPTY
def p_empty(p):
    'empty :'
    pass

#ERROR
def p_error(p):
    print('error de sintaxis')
    sys.exit()

#BUILD THE PARSER
parser = yacc.yacc()

#test the parser
#
file = 'tests/entrada.txt'
#
with open(file, 'r') as f:
    input = f.read()
    parser.parse(input)
    #parser.parse(input, debug = 1)
    print('apropiado')
    quadGenerator.printQuads()
    quadGenerator.printQuadsWithCount()
    print(funcDirectory.directorio['program']['vars'].table)
    print('-------------------------------------------')
    print(funcDirectory.directorio['num']['vars'].table)
    print('-------------------------------------------')
    print(funcDirectory.directorio['main']['vars'].table)
