from dataclasses import dataclass
from tokenize import String
from turtle import st
from .lex import *
from .exception import *


@dataclass
class VarDefine:
    name: Token
    expr: list
    statement_type = 'VarDefine'

@dataclass
class Assign:
    name: list
    expr: list
    statement_type = 'Assign'

@dataclass
class If:
    expr: list
    body: list
    else_body: list
    statement_type = 'If'

@dataclass
class While:
    expr: list
    body: list
    statement_type = 'While'

@dataclass
class Break:
    statement_type = 'Break'

@dataclass
class FunctionDefine:
    name: Token
    param: list
    body: list
    statement_type = 'Function'

@dataclass
class Return:
    expr: list
    statement_type = 'Return'

@dataclass
class Expr:
    expr: list
    statement_type = 'Expr'


class Parser:
    def __init__(self, tokens: list = [], lines: list = []):
        self.current_pos = 0
        if len(tokens) != 0:
            self.current_token = tokens[0]
        
        else:
            self.current_token = Token('none')

        self.tokens = tokens
        self.lines = lines
    
    def advance(self):
        self.current_pos += 1
        self.current_token = self.tokens[self.current_pos]
    
    def next_token(self):
        if self.current_pos + 1 < len(self.tokens):
            return self.tokens[self.current_pos + 1]
        
        else:
            return Token('none')
    
    def parse(self):
        result = []
        buffer = []

        while self.current_pos < len(self.tokens):
            if self.current_token.token_type == 'var':
                name = self.next_token()
                if name.token_type == 'value': #check if name is valid
                    self.advance()
                    if self.next_token().token_type == 'assign':
                        self.advance() #now '='

                        try:
                            self.advance()
                        
                        except IndexError:
                            raise InvalidSyntax('\'=\'', self.lines, self.current_token.line_count)

                        expr = []

                        while True:
                            if self.current_token.token_type == 'end_of_line': break
                            expr.append(self.current_token)

                            try:
                                self.advance()
                            
                            except IndexError:
                                raise InvalidSyntax('Missing \';\'', self.lines, self.current_token.line_count)
                        
                        if len(expr) != 0:
                            result.append(VarDefine(name, Expression(expr, self.lines).parse()))
                        
                        else:
                            raise InvalidSyntax('\'=\'', self.lines, self.current_token.line_count)

                    else:
                        if self.next_token().token_type == 'end_of_line': #when value is not initiallized
                            result.append(VarDefine(name, []))

                        else:
                            raise InvalidSyntax(f'\'{self.next_token().original}\'', self.lines, self.next_token().line_count)

                else:
                    raise InvalidSyntax(f'\'{name.original}\'', self.lines, name.line_count)
            
            elif self.current_token.token_type == 'assign':
                if len(buffer) != 0:
                    try:
                        self.advance()
                        
                    except IndexError:
                        raise InvalidSyntax('\'=\'', self.lines, self.current_token.line_count)

                    expr = []

                    while True:
                        if self.current_token.token_type == 'end_of_line': break
                        expr.append(self.current_token)

                        try:
                            self.advance()
                            
                        except IndexError:
                            raise InvalidSyntax('Missing \';\'', self.lines, self.current_token.line_count)
                    
                    if len(expr) != 0: 
                        result.append(Assign(buffer, Expression(expr, self.lines).parse()))
                        
                    else: 
                        raise InvalidSyntax('\'=\'', self.lines, self.current_token.line_count)

                    buffer = []

                else:
                    raise InvalidSyntax('\'=\'', self.lines, self.current_token.line_count)
            
            elif self.current_token.token_type == 'if':
                try:
                    self.advance()
                
                except IndexError:
                    raise InvalidSyntax('\'if\'', self.lines, self.current_token.line_count)

                expr = []

                while True: #get expr
                    if self.current_token.token_type == 'begin': break
                    expr.append(self.current_token)
                    try:
                        self.advance() 
                    
                    except IndexError:
                        raise InvalidSyntax('Missing \'{\'', self.lines, self.current_token.line_count)
                
                if len(expr) == 0:
                    raise InvalidSyntax('\'{\'', self.lines, self.current_token.line_count)
                
                body = []
                opened = []
                opened.append(self.current_token)

                try:
                    self.advance()

                except IndexError:
                    raise InvalidSyntax('Unclosed \'{\'', self.lines, opened.pop().line_count)

                while True: #get body
                    if self.current_token.token_type == 'begin':
                        opened.append(self.current_token)
                    if self.current_token.token_type == 'end':
                        opened.pop()

                    if len(opened) == 0: 
                        break

                    body.append(self.current_token)
                    try:
                        self.advance() 
                    
                    except IndexError:
                        raise InvalidSyntax('Unclosed \'{\'', self.lines, opened.pop().line_count)
                
                body_parser = Parser(body, self.lines)
                prev = If(Expression(expr, self.lines).parse(), body_parser.parse(), [])

                main_if = prev
                
                while self.next_token().token_type == 'elif' or self.next_token().token_type == 'else':
                    if self.next_token().token_type == 'elif':
                        self.advance() #check for index
                        try:
                            self.advance()
                        
                        except IndexError:
                            raise InvalidSyntax('\'elif\'', self.lines, self.current_token.line_count)

                        expr = []

                        while True: #get expr
                            if self.current_token.token_type == 'begin': break
                            expr.append(self.current_token)

                            try:
                                self.advance()
                            
                            except IndexError:
                                raise InvalidSyntax('Missing \'{\'', self.lines, self.current_token.line_count)
                        
                        if len(expr) == 0:
                            raise InvalidSyntax('\'{\'', self.lines, self.current_token.line_count)
                        
                        body = []
                        opened = []
                        opened.append(self.current_token)

                        try:
                            self.advance()

                        except IndexError:
                            raise InvalidSyntax('Unclosed \'{\'', self.lines, opened.pop().line_count)

                        while True: #get body
                            if self.current_token.token_type == 'begin':
                                opened.append(self.current_token)
                            if self.current_token.token_type == 'end':
                                opened.pop()

                            if len(opened) == 0: 
                                break

                            body.append(self.current_token)

                            try:
                                self.advance()
                            
                            except IndexError:
                                raise InvalidSyntax('Unclosed \'{\'', self.lines, opened.pop().line_count)
                        
                        body_parser = Parser(body, self.lines)
                        new = If(Expression(expr, self.lines).parse(), body_parser.parse(), [])

                        prev.else_body = new
                        prev = new
                    
                    if self.next_token().token_type == 'else':
                        self.advance() #check for index
                        self.advance() #check for index

                        body = []
                        opened = []
                        opened.append(self.current_token)

                        try:
                            self.advance()

                        except IndexError:
                            raise InvalidSyntax('Unclosed \'{\'', self.lines, opened.pop().line_count)

                        while True: #get body
                            if self.current_token.token_type == 'begin':
                                opened.append(self.current_token)
                            if self.current_token.token_type == 'end':
                                opened.pop()

                            if len(opened) == 0: 
                                break

                            body.append(self.current_token)

                            try:
                                self.advance()
                            
                            except IndexError:
                                raise InvalidSyntax('Unclosed \'{\'', self.lines, opened.pop().line_count)
                        
                        body_parser = Parser(body, self.lines)
                        new = body_parser.parse()
                        prev.else_body = new

                        break
                
                result.append(main_if)
            
            elif self.current_token.token_type == 'while':
                try:
                    self.advance()

                except IndexError:
                    raise InvalidSyntax('\'while\'', self.lines, self.current_token.token_type)

                expr = []

                while True: #get expr
                    if self.current_token.token_type == 'begin': break
                    expr.append(self.current_token)

                    try:
                        self.advance()
                    
                    except IndexError:
                        raise InvalidSyntax('Missing \'{\'', self.lines, self.current_token.token_type)
                
                if len(expr) == 0:
                    raise InvalidSyntax('\'{\'', self.lines, self.current_token.line_count)
                    
                #now '{'
                body = []
                opened = []
                opened.append(self.current_token)

                self.advance()

                while True: #get body
                    if self.current_token.token_type == 'begin':
                        opened.append(self.current_token)
                    if self.current_token.token_type == 'end':
                        opened.pop()

                    if len(opened) == 0: 
                        break

                    body.append(self.current_token)

                    try:
                        self.advance()
                    
                    except IndexError:
                        raise InvalidSyntax('Unclosed \'{\'', self.lines, opened.pop().line_count)
                
                body_parser = Parser(body, self.lines)
                result.append(While(Expression(expr, self.lines).parse(), body_parser.parse()))
            
            elif self.current_token.token_type == 'break':
                self.advance()
                result.append(Break())
            
            elif self.current_token.token_type == 'function':
                name = self.next_token() 
                if name.token_type == 'value': #check if name is valid
                    self.advance()
                    if self.next_token().token_type == 'operator' and self.next_token().value == 'invoke':
                        self.advance()
                        self.advance() #now '('
                        try:
                            self.advance()
                        
                        except IndexError:
                            raise InvalidSyntax('\'(\'', self.lines, self.current_token.line_count)

                        param_buffer = []
                        param = []

                        while True:
                            if self.current_token.token_type == 'operator' and self.current_token.value == 'r_paren':
                                if len(param_buffer) == 1:
                                    param.append(param_buffer[0])
                                    param_buffer = []
                                
                                else:
                                    if len(param_buffer) == 0:
                                        raise InvalidSyntax('\',\'', self.lines, self.current_token.line_count)
                                    else:
                                        raise InvalidSyntax('Missing \',\'', self.lines, self.current_token.line_count)
                                break

                            elif self.current_token.token_type == 'operator' and self.current_token.value == 'comma':
                                if len(param_buffer) == 1:
                                    param.append(param_buffer[0])
                                    param_buffer = []
                                
                                else:
                                    if len(param_buffer) == 0:
                                        raise InvalidSyntax('\',\'', self.lines, self.current_token.line_count)
                                    else:
                                        raise InvalidSyntax('Missing \',\'', self.lines, self.current_token.line_count)
                                
                            elif self.current_token.token_type == 'value':
                                param_buffer.append(self.current_token)
                            
                            else:
                                raise InvalidSyntax(f'\'{self.current_token.original}\'', self.lines, self.current_token.line_count)

                            try:
                                self.advance()
                            
                            except IndexError:
                                raise InvalidSyntax('Missing \')\'', self.lines, self.current_token.line_count)

                        if self.next_token().token_type == 'begin':
                            self.advance() #now '{'
                            body = []
                            opened = []
                            opened.append(self.current_token)

                            self.advance()

                            while True: #get body
                                if self.current_token.token_type == 'begin':
                                    opened.append(self.current_token)
                                if self.current_token.token_type == 'end':
                                    opened.pop()

                                if len(opened) == 0: 
                                    break

                                body.append(self.current_token)
                                try:
                                    self.advance()
                                
                                except IndexError:
                                    raise InvalidSyntax('Unclosed \'{\'', self.lines, opened.pop().line_count)
                            
                            body_parser = Parser(body, self.lines)
                            result.append(FunctionDefine(name, param, body_parser.parse()))

                        else:
                            raise InvalidSyntax('Missing \'{\'', self.lines, self.current_token.line_count)
                    
                    else:
                        raise InvalidSyntax('Missing \'(\'', self.lines, self.current_token.line_count)
                
                else:
                    raise InvalidSyntax(f'\'{self.current_token.original}\'', self.lines, self.current_token.line_count)
            
            elif self.current_token.token_type == 'return':
                self.advance() #check for index

                expr = []

                while True:
                    if self.current_token.token_type == 'end_of_line': break
                    expr.append(self.current_token)

                    try:
                        self.advance()

                    except IndexError:
                        raise InvalidSyntax('Missing \';\'', self.lines, self.current_token.line_count)
                
                if len(expr) == 0:
                    raise InvalidSyntax('\';\'', self.lines, self.current_token.line_count)
                
                result.append(Return(Expression(expr, self.lines).parse()))
            
            else:
                if self.current_token.token_type == 'end_of_line':
                    if len(buffer) != 0:
                        result.append(Expr(Expression(buffer, self.lines).parse()))
                        buffer = []
                    
                    else:
                        raise InvalidSyntax('\';\'', self.lines, self.current_token.line_count)

                elif self.current_token.token_type == 'value' or self.current_token.token_type == 'operator' or self.current_token.token_type == 'string':
                    buffer.append(self.current_token)
                
                else:
                    raise InvalidSyntax(f'\'{self.current_token.original}\'', self.lines, self.current_token.line_count)

            
            if self.current_pos < len(self.tokens) - 1: self.advance()
            else: break
        
        if len(buffer) != 0:
            try:
                self.advance()

            except IndexError:
                raise InvalidSyntax('Missing \';\'', self.lines, self.current_token.line_count)
        
        return result
        

class BinaryOperation:
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
    
    def __repr__(self):
        return f'({self.left} {self.operator} {self.right})'

@dataclass
class ValueNode:
    value: str

@dataclass
class StringNode:
    value: str

class NegativeValueNode:
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return f'-({self.value})'


class Expression:
    def __init__(self, tokens: list, lines: list):
        self.current_token = None
        self.previous_token = None
        self.tokens = iter(tokens)

        self.lines = lines

        self.advance()

        self.opened = []
    
    def advance(self):
        try:
            self.previous_token = self.current_token
            self.current_token = next(self.tokens)
        
        except StopIteration:
            self.current_token = None
    
    def parse(self):
        if self.current_token == None:
            return None
        
        result = self.array_operators()

        if self.current_token != None:
            raise InvalidSyntax(f'\'{self.current_token.original}\'', self.lines, self.current_token.line_count)
        
        return result
    
    def array_operators(self):
        result = self.logical_operators()

        while self.current_token != None and self.current_token.token_type == 'operator' and self.current_token.value == 'comma':
            self.advance()
            result = BinaryOperation(result, 'array', self.logical_operators())
        
        return result
    
    def logical_operators(self):
        result = self.low_binary_operators()

        while self.current_token != None and self.current_token.token_type == 'operator' and self.current_token.value in ('equal', 'not_equal', 'greater', 'less', 'greater_equal', 'less_equal', 'or', 'and'):
            op_type = self.current_token.value
            self.advance()
            result = BinaryOperation(result, op_type, self.low_binary_operators())
        
        return result
    
    def low_binary_operators(self):
        result = self.high_binary_operators()
        
        while self.current_token != None and self.current_token.token_type == 'operator' and self.current_token.value in ('add', 'sub'):
            op_type = self.current_token.value
            self.advance()
            result = BinaryOperation(result, op_type, self.high_binary_operators())
        
        return result
    
    def high_binary_operators(self):
        result = self.powered_operators()

        while self.current_token != None and self.current_token.token_type == 'operator' and self.current_token.value in ('mul', 'div', 'mod'):
            op_type = self.current_token.value
            self.advance()
            result = BinaryOperation(result, op_type, self.powered_operators())
        
        return result
    
    def powered_operators(self):
        result = self.invoke_operators()

        while self.current_token != None and self.current_token.token_type == 'operator' and self.current_token.value == 'pow':
            self.advance()
            result = BinaryOperation(result, 'pow', self.invoke_operators())
        
        return result
    
    def invoke_operators(self):
        result = self.factor()

        while self.current_token != None and self.current_token.token_type == 'operator' and self.current_token.value == 'invoke':
            self.advance()
            result = BinaryOperation(result, 'invoke', self.factor())
        
        return result
    
    def factor(self):
        current_token = self.current_token
        
        if current_token != None:
            if current_token.token_type == 'operator':
                if current_token.value == 'l_paren':
                    self.opened.append(current_token)
                    self.advance()

                    if self.current_token != None:
                        result = self.array_operators()
                    
                    else:
                        raise InvalidSyntax('Unclosed \'(\'', self.lines, self.opened.pop().line_count)

                    if not(self.current_token != None and self.current_token.token_type == 'operator' and self.current_token.value == 'r_paren'):
                        if self.current_token == None:
                            raise InvalidSyntax('Unclosed \'(\'', self.lines, self.opened.pop().line_count)

                        elif self.current_token.token_type == 'value':
                            raise InvalidSyntax(f'\'{self.current_token.original}\'', self.lines, self.current_token.line_count)
                        
                        raise InvalidSyntax('Unclosed \'(\'', self.lines, self.opened.pop().line_count)

                    self.advance()
                    
                    return result
                
                elif current_token.value == 'add':
                    self.advance()

                    return self.array_operators()
                
                elif current_token.value == 'sub':
                    self.advance()

                    return NegativeValueNode(self.array_operators())
            
            elif current_token.token_type == 'value':
                self.advance()

                return ValueNode(current_token.value)
            
            elif current_token.token_type == 'string':
                self.advance()

                return StringNode(current_token.value)

            if self.previous_token != None:
                if self.previous_token.token_type == 'operator' and self.previous_token.value == 'l_paren':
                    pass
                else:
                    raise InvalidSyntax(f'\'{self.previous_token.original}\'', self.lines, self.previous_token.line_count)
            
            else:
                if self.current_token != None:
                    raise InvalidSyntax(f'\'{self.current_token.original}\'', self.lines, self.current_token.line_count)

        else:
            raise InvalidSyntax(f'\'{self.previous_token.original}\'', self.lines, self.previous_token.line_count)