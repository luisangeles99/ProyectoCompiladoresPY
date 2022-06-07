"""
.########..#######..##....##.########.##....##..######.
....##....##.....##.##...##..##.......###...##.##....##
....##....##.....##.##..##...##.......####..##.##......
....##....##.....##.#####....######...##.##.##..######.
....##....##.....##.##..##...##.......##..####.......##
....##....##.....##.##...##..##.......##...###.##....##
....##.....#######..##....##.########.##....##..######.

Dentro de este archivo se encunetran dos estrucutras fundamentales,
tokens y palabras reservadas, ambas son declaradas de esta manera
para que puedan ser utilizadas por PLY despues. 
"""
tokens = [
    'ID',
    'PLUS',
    'MINUS',
    'TIMES',
    'DIVIDE',
    'LT',
    'GT',
    'NE',
    'LPAREN',
    'RPAREN',
    'LBRACE',
    'RBRACE',
    'ASSIGN',
    'COMMA',
    'SEMICOLON',
    'CTEI',
    'CTEF',
    'CTECH',
    'LSBRACKET',
    'RSBRACKET',
    'AND',
    'OR',
    'POINT',
    'EQ',
    'NOT',
    'GTE',
    'LTE'
]

reserved = {
    'if' : 'IF',
    'else' : 'ELSE',
    'program' : 'PROGRAM',
    'int' : 'INT', 
    'float' : 'FLOAT',
    'char' : 'CHAR',
    'print' : 'PRINT',
    'var' : 'VAR', 
    ####### LINE
    'class' : 'CLASS',
    'while' : 'WHILE',
    'void' : 'VOID',
    'print' : 'PRINT',
    'read' : 'READ',
    'func' : 'FUNC',
    'import' : 'IMPORT',
    'derives' : 'DERIVES',
    'return' : 'RETURN',
    'main': 'MAIN'
}