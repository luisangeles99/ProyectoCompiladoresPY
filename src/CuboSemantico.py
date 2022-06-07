"""
..######..########.##.....##.....######..##.....##.########..########
.##....##.##.......###...###....##....##.##.....##.##.....##.##......
.##.......##.......####.####....##.......##.....##.##.....##.##......
..######..######...##.###.##....##.......##.....##.########..######..
.......##.##.......##.....##....##.......##.....##.##.....##.##......
.##....##.##.......##.....##....##....##.##.....##.##.....##.##......
..######..########.##.....##.....######...#######..########..########

Clase que contiene la estrucutra del cubo semantico, donde se pueden 
hacer consultas para determinar si una operacion entre diferentes 
operadores el posible o se genera un error.
"""
class SemanticCube():
    def __init__(self):
        self.cube = { 
            'int': {
                'int': {
                    '+': 'int', '-': 'int', '*': 'int', '/':'int', '=': 'int', 
                    '<': 'bool', '>': 'bool', '<=': 'bool', '>=': 'bool', '==': 'bool', '!=': 'bool',
                    '||': 'error', '&&': 'error'
                },
                'float': {
                    '+': 'float', '-': 'float', '*': 'float', '/':'float', '=': 'int', 
                    '<': 'bool', '>': 'bool', '<=': 'bool', '>=': 'bool', '==': 'bool', '!=': 'bool',
                    '||': 'error', '&&': 'error'
                },
                'char': {
                    '+': 'error', '-': 'error', '*': 'error', '/':'error', '=': 'error', 
                    '<': 'error', '>': 'error', '<=': 'error', '>=': 'error', '==': 'error', '!=': 'error',
                    '||': 'error', '&&': 'error'
                },
                'bool': {
                    '+': 'error', '-': 'error', '*': 'error', '/':'error', '=': 'error', 
                    '<': 'error', '>': 'error', '<=': 'error', '>=': 'error', '==': 'error', '!=': 'error',
                    '||': 'error', '&&': 'error'
                },
                'complex': {
                    '+': 'error', '-': 'error', '*': 'error', '/':'error', '=': 'error', 
                    '<': 'error', '>': 'error', '<=': 'error', '>=': 'error', '==': 'error', '!=': 'error',
                    '||': 'error', '&&': 'error'
                }
            },
            'float': {
                'int': {
                    '+': 'float', '-': 'float', '*': 'float', '/':'float', '=': 'float', 
                    '<': 'bool', '>': 'bool', '<=': 'bool', '>=': 'bool', '==': 'bool', '!=': 'bool',
                    '||': 'error', '&&': 'error'
                },
                'float': {
                    '+': 'float', '-': 'float', '*': 'float', '/':'float', '=': 'float', 
                    '<': 'bool', '>': 'bool', '<=': 'bool', '>=': 'bool', '==': 'bool', '!=': 'bool',
                    '||': 'error', '&&': 'error'
                },
                'char': {
                    '+': 'error', '-': 'error', '*': 'error', '/':'error', '=': 'error', 
                    '<': 'error', '>': 'error', '<=': 'error', '>=': 'error', '==': 'error', '!=': 'error',
                    '||': 'error', '&&': 'error'
                },
                'bool': {
                    '+': 'error', '-': 'error', '*': 'error', '/':'error', '=': 'error', 
                    '<': 'error', '>': 'error', '<=': 'error', '>=': 'error', '==': 'error', '!=': 'error',
                    '||': 'error', '&&': 'error'
                },
                'complex': {
                    '+': 'error', '-': 'error', '*': 'error', '/':'error', '=': 'error', 
                    '<': 'error', '>': 'error', '<=': 'error', '>=': 'error', '==': 'error', '!=': 'error',
                    '||': 'error', '&&': 'error'
                }
            },
            'char': {
                'int': {
                    '+': 'error', '-': 'error', '*': 'error', '/':'error', '=': 'error', 
                    '<': 'error', '>': 'error', '<=': 'error', '>=': 'error', '==': 'error', '!=': 'error',
                    '||': 'error', '&&': 'error'
                },
                'float': {
                    '+': 'error', '-': 'error', '*': 'error', '/':'error', '=': 'error', 
                    '<': 'error', '>': 'error', '<=': 'error', '>=': 'error', '==': 'error', '!=': 'error',
                    '||': 'error', '&&': 'error'
                },
                'char': {
                    '+': 'error', '-': 'error', '*': 'error', '/':'error', '=': 'char', 
                    '<': 'error', '>': 'error', '<=': 'error', '>=': 'error', '==': 'bool', '!=': 'bool',
                    '||': 'error', '&&': 'error'
                },
                'bool': {
                    '+': 'error', '-': 'error', '*': 'error', '/':'error', '=': 'error', 
                    '<': 'error', '>': 'error', '<=': 'error', '>=': 'error', '==': 'error', '!=': 'error',
                    '||': 'error', '&&': 'error'
                },
                'complex': {
                    '+': 'error', '-': 'error', '*': 'error', '/':'error', '=': 'error', 
                    '<': 'error', '>': 'error', '<=': 'error', '>=': 'error', '==': 'error', '!=': 'error',
                    '||': 'error', '&&': 'error'
                }
            },
            'bool': {
                'int': {
                    '+': 'error', '-': 'error', '*': 'error', '/':'error', '=': 'error', 
                    '<': 'error', '>': 'error', '<=': 'error', '>=': 'error', '==': 'bool', '!=': 'bool',
                    '||': 'error', '&&': 'error'
                },
                'float': {
                    '+': 'error', '-': 'error', '*': 'error', '/':'error', '=': 'error', 
                    '<': 'error', '>': 'error', '<=': 'error', '>=': 'error', '==': 'bool', '!=': 'bool',
                    '||': 'error', '&&': 'error'
                },
                'char': {
                    '+': 'error', '-': 'error', '*': 'error', '/':'error', '=': 'error', 
                    '<': 'error', '>': 'error', '<=': 'error', '>=': 'error', '==': 'error', '!=': 'error',
                    '||': 'error', '&&': 'error'
                },
                'bool': {
                    '+': 'error', '-': 'error', '*': 'error', '/':'error', '=': 'error', 
                    '<': 'error', '>': 'error', '<=': 'error', '>=': 'error', '==': 'error', '!=': 'error',
                    '||': 'bool', '&&': 'bool'
                },
                'complex': {
                    '+': 'error', '-': 'error', '*': 'error', '/':'error', '=': 'error', 
                    '<': 'error', '>': 'error', '<=': 'error', '>=': 'error', '==': 'error', '!=': 'error',
                    '||': 'error', '&&': 'error'
                }
            },
            'complex': {
                'int': {
                    '+': 'error', '-': 'error', '*': 'error', '/':'error', '=': 'error', 
                    '<': 'error', '>': 'error', '<=': 'error', '>=': 'error', '==': 'bool', '!=': 'bool',
                    '||': 'error', '&&': 'error'
                },
                'float': {
                    '+': 'error', '-': 'error', '*': 'error', '/':'error', '=': 'error', 
                    '<': 'error', '>': 'error', '<=': 'error', '>=': 'error', '==': 'bool', '!=': 'bool',
                    '||': 'error', '&&': 'error'
                },
                'char': {
                    '+': 'error', '-': 'error', '*': 'error', '/':'error', '=': 'error', 
                    '<': 'error', '>': 'error', '<=': 'error', '>=': 'error', '==': 'error', '!=': 'error',
                    '||': 'error', '&&': 'error'
                },
                'bool': {
                    '+': 'error', '-': 'error', '*': 'error', '/':'error', '=': 'error', 
                    '<': 'error', '>': 'error', '<=': 'error', '>=': 'error', '==': 'error', '!=': 'error',
                    '||': 'bool', '&&': 'bool'
                },
                'complex': {
                    '+': 'error', '-': 'error', '*': 'error', '/':'error', '=': 'error', 
                    '<': 'error', '>': 'error', '<=': 'error', '>=': 'error', '==': 'error', '!=': 'error',
                    '||': 'error', '&&': 'error'
                }
            }
        }

    def getType(self, leftType, rightType, oper):
        if leftType in self.cube.keys():
            if rightType in self.cube[leftType].keys():
                return self.cube[leftType][rightType][oper]
        return 'Error bad operation or type'
    
#cubo = SemanticCube()
#print(cubo.getType('int', 'char', '+'))