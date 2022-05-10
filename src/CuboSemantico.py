# DESCRIPCION DEL CUBO SEMANTICO Y DE SUS METODOS

class SemanticCube():
    def __init__(self):
        self.cube = { #TODO: Verify if we are using symbols or the token ex. + or PLUS; ALSO CHECK IF WE ARE ALLOWING COMPARISON OF 1 AND '1'
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
                }
            }
        }

        self.typesMapping = {
            'int': 1,
            'float': 2,
            'char': 3,
            'bool': 4,
            'error': 0
        }

    def getType(self, leftType, rightType, oper):
        if leftType in self.cube.keys():
            if rightType in self.cube[leftType].keys():
                return self.cube[leftType][rightType][oper]
        return 'Error bad operation or type'
    
#cubo = SemanticCube()
#print(cubo.getType('int', 'char', '+'))