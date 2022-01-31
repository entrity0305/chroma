from dataclasses import dataclass
from .exception import *


#operators
@dataclass
class Add:
    pass

@dataclass
class Sub:
    pass

@dataclass
class Neg:
    pass

@dataclass
class Mul:
    pass

@dataclass
class Div:
    pass

@dataclass
class Mod:
    pass

@dataclass
class Pow:
    pass

@dataclass
class Greater:
    pass

@dataclass
class Less:
    pass

@dataclass
class Greater_equal:
    pass

@dataclass
class Less_equal:
    pass

@dataclass
class Equal:
    pass

@dataclass
class Not_equal:
    pass

@dataclass
class Or:
    pass

@dataclass
class And:
    pass

@dataclass
class Attr:
    pass

@dataclass
class Array:
    pass

@dataclass
class Invoke:
    pass

#commands
@dataclass
class Pushi:
    value: str

@dataclass
class Pushf:
    value: str

@dataclass
class Pushstr:
    value: str

@dataclass
class Load:
    value: str

@dataclass
class Var:
    name: str

@dataclass
class Assign:
    name: str

@dataclass
class Ifzero:
    pos: int

@dataclass
class Goto:
    pos: int

#function
@dataclass
class FunctionDef:
    name: str
    param: list
    body: list

def compile_expression(expr):
    if expr.node_type == 'operator':
        if expr.operator == 'dot':
            if expr.left.node_type == 'value':
                if expr.left.value.isdigit():
                    if expr.right.node_type == 'value':
                        if expr.right.value.isdigit(): #when float
                            return [Pushf(expr.left.value + '.' + expr.right.value)]
            
            if expr.right.node_type == 'value':
                if expr.right.value.isdigit():
                    pass #invalid syntax

            return compile_expression(expr.left) + compile_expression(expr.right) + [Attr()]

        elif expr.operator == 'add':
            return compile_expression(expr.left) + compile_expression(expr.right) + [Add()]

        elif expr.operator == 'sub':
            return compile_expression(expr.left) + compile_expression(expr.right) + [Sub()]

        elif expr.operator == 'mul':
            return compile_expression(expr.left) + compile_expression(expr.right) + [Mul()]
        
        elif expr.operator == 'div':
            return compile_expression(expr.left) + compile_expression(expr.right) + [Div()]
        
        elif expr.operator == 'mod':
            return compile_expression(expr.left) + compile_expression(expr.right) + [Mod()]
        
        elif expr.operator == 'pow':
            return compile_expression(expr.left) + compile_expression(expr.right) + [Pow()]
        
        elif expr.operator == 'greater':
            return compile_expression(expr.left) + compile_expression(expr.right) + [Greater()]
        
        elif expr.operator == 'less':
            return compile_expression(expr.left) + compile_expression(expr.right) + [Less()]
        
        elif expr.operator == 'greater_equal':
            return compile_expression(expr.left) + compile_expression(expr.right) + [Greater_equal()]
        
        elif expr.operator == 'less_equal':
            return compile_expression(expr.left) + compile_expression(expr.right) + [Less_equal()]

        elif expr.operator == 'equal':
            return compile_expression(expr.left) + compile_expression(expr.right) + [Equal()]
        
        elif expr.operator == 'not_equal':
            return compile_expression(expr.left) + compile_expression(expr.right) + [Not_equal()]

        elif expr.operator == 'or':
            return compile_expression(expr.left) + compile_expression(expr.right) + [Or()]
        
        elif expr.operator == 'and':
            return compile_expression(expr.left) + compile_expression(expr.right) + [And()]
        
        elif expr.operator == 'array':
            return compile_expression(expr.left) + compile_expression(expr.right) + [Array()]
        
        elif expr.operator == 'invoke':
            return compile_expression(expr.left) + compile_expression(expr.right) + [Invoke()]

    else:
        if expr.node_type == 'value':
            if expr.value.isdigit():
                return [Pushi(expr.value)]
            
            return [Load(expr.value)]
        
        elif expr.node_type == 'string':
            return [Pushstr(expr.value)]
        
        elif expr.node_type == 'negative_value':
            return compile_expression(expr.value) + [Neg()]

#TODO:
#   Add return statement
#   Add while statement
#   Add error handling
def compile_statements(statements, start = 0):
    result = []

    current_pos = start
    for current_statement in statements:
        if current_statement.statement_type == 'var':
            expr = compile_expression(current_statement.expr)
            result += expr
            result.append(Var(current_statement.name.value))

            current_pos += len(expr) + 1
        
        elif current_statement.statement_type == 'assign':
            expr = compile_expression(current_statement.expr)

            if len(current_statement.name) == 1:
                result += expr
                result.append(Assign(current_statement.name[0].value))

                current_pos += len(expr) + 1

        elif current_statement.statement_type == 'if':
            expr = compile_expression(current_statement.expr)
            result += expr
            current_pos += len(expr)
            body = compile_statements(current_statement.body, current_pos + 1)
            else_body = compile_statements(current_statement.else_body, current_pos + len(body) + 2)
            zero_jump_pos = current_pos + len(body) + 2
            not_zero_jump_pos = zero_jump_pos + len(else_body)

            statement = [Ifzero(zero_jump_pos)] + body + [Goto(not_zero_jump_pos)] + else_body
            result += statement

            current_pos += len(statement)
        
        elif current_statement.statement_type == 'function':
            name = current_statement.name.value
            param = [p.value for p in current_statement.param]

            body = compile_statements(current_statement.body)

            current_pos += 1

            result += [FunctionDef(name, param, body)]
        
        elif current_statement.statement_type == 'expr':
            expr = compile_expression(current_statement.expr)
            result += expr
            current_pos += len(expr)

    return result