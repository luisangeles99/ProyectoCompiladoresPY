from tkinter.messagebox import NO
import ply.yacc as yacc
from Avail import Avail
from lexer import tokens
from DirectorioFunciones import DirectorioFunciones
from QuadGenerator import QuadGenerator
from CuboSemantico import SemanticCube
import Memoria
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
currTypeFunc = None
currFunc = None
currScope = 'global'

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
relationalOperators = [
    '>', '<', '>=', '<=', '==', '!='
]

#------------------------------------ PROGRAM SYNTAX ------------------------------------

#TODO: Remove import rules from language and from diagram

def p_PROGRAM(p):
    '''P            : PROGRAM ID startProgram SEMICOLON P_STRUCTURE endProgram'''

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

def p_FUNCTION_CALL(p):
    '''FUNCTION_CALL        : ID LPAREN EXP FUNCTION_C_ONE RPAREN'''

def p_FUNCTION_C_ONE(p):
    '''FUNCTION_C_ONE       : COMMA EXP FUNCTION'''

def p_FUNCTION_DEC(p): #CHECK IF SET CURR IS OK THERE
    '''FUNCTION_DEC         : FUNC FUNCTION_D_ONE ID addFunc LPAREN FUNCTION_D_TWO RPAREN'''


def p_FUNCTION(p):
    '''FUNCTION             : FUNCTION_DEC BLOCK'''

def p_FUNCTION_D_ONE(p):
    '''FUNCTION_D_ONE       : SIMPLE_TYPE
                            | VOID'''
    if p[1] == 'void':
        global currTypeFunc 
        print('añadimos tipo void')
        currTypeFunc = p[1]

def p_FUNCTION_D_TWO(p):
    '''FUNCTION_D_TWO       : PARAM
                            | empty'''

def p_PARAM(p):
    '''PARAM                : SIMPLE_TYPE ID PARAM_ONE'''


def p_PARAM_ONE(p):
    '''PARAM_ONE            : COMMA PARAM
                            | empty'''

#------------------------------------ VARIABLES SYNTAX ------------------------------------

def p_VARIABLE(p): #TODO: Check if braces for access is there
    '''VARIABLE             : ID VARIABLE_ONE
                            | FIELD_ACCESS'''
    varId = p[1]
    pOperandos.append(varId)
    #get type using function name
    varInfo = funcDirectory.getVar(currFunc, varId)
    pTipos.append(varInfo['type'])

def p_VARIABLE_ONE(p):
    '''VARIABLE_ONE         : LSBRACKET EXP RSBRACKET VARIABLE_ONE
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
    funcDirectory.updateVarValue(currFunc, varId, temp)
    quadGenerator.generateQuad(p[2], temp, None, varId)
    

def p_DEC_VAR(p):
    '''DEC_VAR              : VAR DEC_VAR_ONE SEMICOLON'''

def p_DEC_VAR_ONE(p):
    '''DEC_VAR_ONE          : COMPLEX_TYPE ID DEC_V_O_COMPLEX
                            | SIMPLE_TYPE ID addVar DEC_ARR DEC_V_O_SIMPLE'''

def p_DEC_V_O_SIMPLE(p):
    '''DEC_V_O_SIMPLE       : COMMA ID addVar DEC_ARR DEC_V_O_SIMPLE
                            | empty'''
                    
def p_DEC_ARR(p):
    '''DEC_ARR              : LSBRACKET CTEI RSBRACKET DEC_ARR_ONE
                            | empty'''

def p_DEC_ARR_ONE(p):
    '''DEC_ARR_ONE          : LSBRACKET CTEI RSBRACKET
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
    elif p[-1] == 'var':
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
                    | FUNCTION_CALL 
                    | READ_FUNC 
                    | PRINT_FUNC 
                    | COND 
                    | WHILE_LOOP
                    | RETURN_FUNC''' #TODO: MISSING RETURN AND FOR_LOOP

def p_RETURN(p):
    '''RETURN_FUNC      : RETURN RETURN_F_ONE SEMICOLON'''
    term = pOperandos.pop()
    termTipo = pTipos.pop()
    quadGenerator.generateQuad('return', None, None, term)

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

def p_endProgram(p):
    '''endProgram       :'''
    quadGenerator.generateQuad('END', None, None, None)

#------------------------------------ VARIABLES NEURAL POINTS ----------------------------

def p_addVar(p):
    '''addVar           : '''
    varName = p[-1]
    if currScope == 'local':
        funcDirectory.addVar(currFunc, varName, currTypeVar, None)
    elif currScope == 'global':
        pass
    
#------------------------------------ EXP NEURAL POINTS ----------------------------

def p_pushOperador(p):
    '''pushOperador     : '''
    oper = p[-1]
    pOperadores.append(oper)

def p_pushInt(p):
    '''pushInt         :'''
    const = p[-1]
    pOperandos.append(const)
    pTipos.append('int')

def p_pushFloat(p):
    '''pushFloat        :'''
    const = p[-1]
    pOperandos.append(const)
    pTipos.append('float')

def p_pushChar(p):
    '''pushChar         :'''
    const = p[-1]
    pOperandos.append(const)
    pTipos.append('char')

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
    res = avail.next()
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
    print(pTipos)
    print(pOperadores)
    print(pOperandos)
    quadGenerator.printQuads()
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
        print('Func added to directory')
        print(funcDirectory.directorio)
        global currFunc 
        currFunc = functionName
        global currScope
        currScope = 'local'

#------------------------------------ STMT NEURAL POINTS ----------------------------

def p_readFunc(p):
    '''readFunc         :'''
    pass

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
    print('apropiado')
    quadGenerator.printQuads()
    quadGenerator.printQuadsWithCount()

