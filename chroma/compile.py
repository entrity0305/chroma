from dataclasses import dataclass
from .exception import *


#operators
@dataclass
class Add:
    line_count: int = 0
    command_type: str = 'add'

@dataclass
class Sub:
    line_count: int = 0
    command_type: str = 'sub'

@dataclass
class Neg:
    line_count: int = 0
    command_type: str = 'neg'

@dataclass
class Mul:
    line_count: int = 0
    command_type: str = 'mul'

@dataclass
class Div:
    line_count: int = 0
    command_type: str = 'div'

@dataclass
class Mod:
    line_count: int = 0
    command_type: str = 'mod'

@dataclass
class Pow:
    line_count: int = 0
    command_type: str = 'pow'

@dataclass
class Greater:
    line_count: int = 0
    command_type: str = 'greater'

@dataclass
class Less:
    line_count: int = 0
    command_type: str = 'less'

@dataclass
class Greater_equal:
    line_count: int = 0
    command_type: str = 'greater_equal'

@dataclass
class Less_equal:
    line_count: int = 0
    command_type: str = 'less_equal'

@dataclass
class Equal:
    line_count: int = 0
    command_type: str = 'equal'

@dataclass
class Not_equal:
    line_count: int = 0
    command_type: str = 'not_equal'

@dataclass
class Or:
    line_count: int = 0
    command_type: str = 'or'

@dataclass
class And:
    line_count: int = 0
    command_type: str = 'and'

@dataclass
class Attr:
    line_count: int = 0
    command_type: str = 'attr'

@dataclass
class Array:
    line_count: int = 0
    command_type: str = 'array'

@dataclass
class Invoke:
    line_count: int = 0
    command_type: str = 'invoke'

#commands
@dataclass
class Pushi:
    value: str

    line_count: int = 0
    command_type: str = 'pushi'

@dataclass
class Pushf:
    value: str

    line_count: int = 0
    command_type: str = 'pushf'

@dataclass
class Pushstr:
    value: str

    line_count: int = 0
    command_type: str = 'pushstr'

@dataclass
class Pushnone:
    line_count: int = 0
    command_type: str = 'pushnone'

@dataclass
class Pushvoid:
    line_count: int = 0
    command_type: str = 'pushvoid'

@dataclass
class Load:
    name: str

    line_count: int = 0
    command_type: str = 'load'

@dataclass
class Var:
    name: str

    line_count: int = 0
    command_type: str = 'var'

@dataclass
class Assign:
    name: str

    line_count: int = 0
    command_type: str = 'assign'

@dataclass
class Ifzero:
    pos: int

    line_count: int = 0
    command_type: str = 'ifzero'

@dataclass
class Goto:
    pos: int

    line_count: int = 0
    command_type: str = 'goto'

#function
@dataclass
class FunctionDef:
    name: str
    param: list
    body: list

    line_count: int = 0
    command_type: str = 'function'

@dataclass
class Return:
    line_count: int = 0
    command_type: str = 'return'

#end
@dataclass
class End:
    command_type: str = 'end'

def compile_expression(expr, lines: list = []):
    if expr.node_type == 'operator':
        if expr.operator == 'dot':
            if expr.left.node_type == 'value':
                if expr.left.value.isdigit():
                    if expr.right.node_type == 'value':
                        if expr.right.value.isdigit(): #when float
                            return [Pushf(expr.left.value + '.' + expr.right.value, expr.left.line_count)]
            
            if expr.right.node_type == 'value':
                if expr.right.value.isdigit():
                    raise InvalidSyntax(f'\'{expr.right.value}\'', lines, expr.right.line_count)

            return compile_expression(expr.left, expr.left.line_count) + compile_expression(expr.right, expr.right.line_count) + [Attr(expr.line_count)]

        elif expr.operator == 'add':
            return compile_expression(expr.left, expr.left.line_count) + compile_expression(expr.right, expr.right.line_count) + [Add(expr.line_count)]

        elif expr.operator == 'sub':
            return compile_expression(expr.left, expr.left.line_count) + compile_expression(expr.right, expr.right.line_count) + [Sub(expr.line_count)]

        elif expr.operator == 'mul':
            return compile_expression(expr.left, expr.left.line_count) + compile_expression(expr.right, expr.right.line_count) + [Mul(expr.line_count)]
        
        elif expr.operator == 'div':
            return compile_expression(expr.left, expr.left.line_count) + compile_expression(expr.right, expr.right.line_count) + [Div(expr.line_count)]
        
        elif expr.operator == 'mod':
            return compile_expression(expr.left, expr.left.line_count) + compile_expression(expr.right, expr.right.line_count) + [Mod(expr.line_count)]
        
        elif expr.operator == 'pow':
            return compile_expression(expr.left, expr.left.line_count) + compile_expression(expr.right, expr.right.line_count) + [Pow(expr.line_count)]
        
        elif expr.operator == 'greater':
            return compile_expression(expr.left, expr.left.line_count) + compile_expression(expr.right, expr.right.line_count) + [Greater(expr.line_count)]
        
        elif expr.operator == 'less':
            return compile_expression(expr.left, expr.left.line_count) + compile_expression(expr.right, expr.right.line_count) + [Less(expr.line_count)]
        
        elif expr.operator == 'greater_equal':
            return compile_expression(expr.left, expr.left.line_count) + compile_expression(expr.right, expr.right.line_count) + [Greater_equal(expr.line_count)]
        
        elif expr.operator == 'less_equal':
            return compile_expression(expr.left, expr.left.line_count) + compile_expression(expr.right, expr.right.line_count) + [Less_equal(expr.line_count)]

        elif expr.operator == 'equal':
            return compile_expression(expr.left, expr.left.line_count) + compile_expression(expr.right, expr.right.line_count) + [Equal(expr.line_count)]
        
        elif expr.operator == 'not_equal':
            return compile_expression(expr.left, expr.left.line_count) + compile_expression(expr.right, expr.right.line_count) + [Not_equal(expr.line_count)]

        elif expr.operator == 'or':
            return compile_expression(expr.left, expr.left.line_count) + compile_expression(expr.right, expr.right.line_count) + [Or(expr.line_count)]
        
        elif expr.operator == 'and':
            return compile_expression(expr.left, expr.left.line_count) + compile_expression(expr.right, expr.right.line_count) + [And(expr.line_count)]

        elif expr.operator == 'array':
            return compile_expression(expr.left, expr.left.line_count) + compile_expression(expr.right, expr.right.line_count) + [Array(expr.line_count)]
        
        elif expr.operator == 'invoke':
            return compile_expression(expr.left, expr.left.line_count) + compile_expression(expr.right, expr.right.line_count) + [Invoke(expr.line_count)]
    else:
        if expr.node_type == 'none':
            return [Pushnone(expr.line_count)]
        
        elif expr.node_type == 'void':
            return [Pushvoid(expr.line_count)]

        elif expr.node_type == 'value':
            if expr.value.isdigit():
                return [Pushi(expr.value, expr.line_count)]
            
            return [Load(expr.value, expr.line_count)]
        
        elif expr.node_type == 'string':
            return [Pushstr(expr.value, expr.line_count)]
        
        elif expr.node_type == 'negative_value':
            return compile_expression(expr.value, expr.line_count) + [Neg(expr.line_count)]


def compile_statements(statements, lines: list = [], start: int = 0, break_pos: int = 0, in_while: bool = False, in_function: bool = False):
    result = []

    current_pos = start
    for current_statement in statements:
        if current_statement.statement_type == 'var':
            expr = compile_expression(current_statement.expr, lines)
            result += expr
            result.append(Var(current_statement.name.value, current_statement.line_count))

            current_pos += len(expr) + 1
        
        elif current_statement.statement_type == 'assign':
            expr = compile_expression(current_statement.expr, lines)

            if len(current_statement.name) == 1:
                result += expr
                result.append(Assign(current_statement.name[0].value, current_statement.line_count))

                current_pos += len(expr) + 1

        elif current_statement.statement_type == 'if':
            expr = compile_expression(current_statement.expr, lines)
            result += expr
            current_pos += len(expr)
            body = compile_statements(current_statement.body, lines, current_pos + 1, break_pos, in_while, in_function)
            else_body = compile_statements(current_statement.else_body, lines, current_pos + len(body) + 2, break_pos, in_while, in_function)
            zero_jump_pos = current_pos + len(body) + 2
            not_zero_jump_pos = zero_jump_pos + len(else_body)

            statement = [Ifzero(zero_jump_pos, current_statement.line_count)] + body + [Goto(not_zero_jump_pos, current_statement.line_count)] + else_body
            result += statement

            current_pos += len(statement)
        
        elif current_statement.statement_type == 'while':
            loop_start_pos = current_pos
            expr = compile_expression(current_statement.expr, lines)
            result += expr
            current_pos += len(expr)
            body = compile_statements(current_statement.body, lines, current_pos + 1, current_pos, True, in_function)
            zero_jump_pos = current_pos + len(body) + 2

            statement = [Ifzero(zero_jump_pos, current_statement.line_count)] + body + [Goto(loop_start_pos, current_statement.line_count)]
            result += statement

            current_pos += len(statement)
        
        elif current_statement.statement_type == 'break':
            if in_while:
                result += [Pushi('0', current_statement.line_count)] + [Goto(break_pos, current_statement.line_count)]
                current_pos += 2

            else:
                raise InvalidSyntax(f'\'break\' outside loop', lines, current_statement.line_count)
        
        elif current_statement.statement_type == 'function':
            name = current_statement.name.value
            param = [p.value for p in current_statement.param]

            body = compile_statements(current_statement.body, lines, in_function=True)

            current_pos += 1

            result += [FunctionDef(name, param, body, current_statement.line_count)]
        
        elif current_statement.statement_type == 'return':
            if in_function:
                expr = compile_expression(current_statement.expr, lines)
                result += expr
                result.append(Return(current_statement.line_count))

                current_pos += len(expr) + 1

            else:
                raise InvalidSyntax(f'\'return\' outside function', lines, current_statement.line_count)
        
        elif current_statement.statement_type == 'expr':
            expr = compile_expression(current_statement.expr, lines)
            result += expr
            current_pos += len(expr)

    return result