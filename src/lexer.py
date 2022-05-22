import ply.lex as lex

from tokens import tokens, reserved

tokens = tokens + list(reserved.values())

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ASSIGN = r'='
t_LT = r'\<'
t_GT = r'\>'
t_NE = r'\!\='
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_COMMA = r'\,'
t_SEMICOLON = r'\;'
t_LSBRACKET = r'\['
t_RSBRACKET = r'\]'
t_AND = r'&&'
t_OR = r'\|\|'
t_POINT = r'\.'
t_EQ = r'\=\='
t_NOT = r'!'
t_GTE = r'\>\='
t_LTE = r'\<\='

t_ignore  = ' \t'

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    if t.value in reserved:
        t.type = reserved[ t.value ]
    return t

def t_CTEF(t):
    r'[-]?[0-9]+\.[0-9]+'
    t.value = float(t.value)
    return t

def t_CTEI(t):
    r'[-]?[0-9]+'
    t.value = int(t.value)
    return t

def t_CTECH(t): #TODO: CHECK NAME IN PARSER
    r'\'[A-Za-z]\''
    t.value = t.value[1]
    return t

def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

lexer = lex.lex()