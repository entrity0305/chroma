from dataclasses import dataclass
from .lex import *


class InvalidSyntax(Exception):
    def __init__(self, message: str = '', lines: list = [], line_count: int = 0):
        super().__init__(f'At line {line_count+1},\n{lines[line_count]}\nInvalid Syntax: {message}')


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
                            result.append(VarDefine(name, Expression(expr).parse()))
                        
                        else:
                            raise InvalidSyntax('\'=\'', self.lines, self.current_token.line_count)

                    else:
                        if self.next_token().token_type == 'end_of_line': #when value is not initiallized
                            result.append(VarDefine(name, []))

                        else:
                            InvalidSyntax(f'\'{self.next_token().value}\'', self.lines, self.next_token().line_count)

                else:
                    raise InvalidSyntax(f'\'{name.value}\'', self.lines, name.line_count)
            
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
                        result.append(Assign(buffer, Expression(expr).parse()))
                        
                    else: 
                        raise InvalidSyntax('\'=\'', self.lines, self.current_token.line_count)

                    buffer = []

                else:
                    raise InvalidSyntax('\'=\'', self.lines, self.current_token.line_count)
            
            elif self.current_token.token_type == 'if':
                self.advance() #check for index

                expr = []

                while True: #get expr
                    if self.current_token.token_type == 'begin': break
                    expr.append(self.current_token)

                    self.advance() #check for index ==> missing '{'
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

                    self.advance() #check for index ==> missing '}'
                
                body_parser = Parser(body)
                prev = If(Expression(expr).parse(), body_parser.parse(), [])

                main_if = prev
                
                while self.next_token().token_type == 'elif' or self.next_token().token_type == 'else':
                    if self.next_token().token_type == 'elif':
                        self.advance() #check for index
                        self.advance() #check for index

                        expr = []

                        while True: #get expr
                            if self.current_token.token_type == 'begin': break
                            expr.append(self.current_token)

                            self.advance() #check for index ==> missing '{'
                        
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

                            self.advance() #check for index ==> missing '}'
                        
                        body_parser = Parser(body)
                        new = If(Expression(expr).parse(), body_parser.parse(), [])

                        prev.else_body = new
                        prev = new
                    
                    if self.next_token().token_type == 'else':
                        self.advance() #check for index
                        self.advance() #check for index

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

                            self.advance() #check for index ==> missing '}'
                        
                        body_parser = Parser(body)
                        new = body_parser.parse()
                        prev.else_body = new

                        break
                
                result.append(main_if)
            
            elif self.current_token.token_type == 'while':
                self.advance() #check for index

                expr = []

                while True: #get expr
                    if self.current_token.token_type == 'begin': break
                    expr.append(self.current_token)

                    self.advance() #check for index ==> missing '{'
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

                    self.advance() #check for index ==> missing '}'
                
                body_parser = Parser(body)
                result.append(While(Expression(expr).parse(), body_parser.parse()))
            
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
                        self.advance() #check for index ==> invalid '('

                        param_buffer = []
                        param = []

                        while True:
                            if self.current_token.token_type == 'operator' and self.current_token.value == 'r_paren':
                                if len(param_buffer) == 1:
                                    param.append(param_buffer[0])
                                    param_buffer = []
                                
                                else:
                                    if len(param_buffer) == 0:
                                        pass #syntax error: invalid ','
                                    else:
                                        pass #syntax error: missing ','
                                break

                            elif self.current_token.token_type == 'operator' and self.current_token.value == 'comma':
                                if len(param_buffer) == 1:
                                    param.append(param_buffer[0])
                                    param_buffer = []
                                
                                else:
                                    if len(param_buffer) == 0:
                                        pass #syntax error: invalid ','
                                    else:
                                        pass #syntax error: missing ','
                                
                            elif self.current_token.token_type == 'value':
                                param_buffer.append(self.current_token)
                            
                            else:
                                pass #invalid syntax

                            self.advance() #check for index ==> missing ')'

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
                                self.advance() #check for index ==> missing '}'
                            
                            body_parser = Parser(body)
                            result.append(FunctionDefine(name, param, body_parser.parse()))

                        else:
                            pass #syntax error: missing '{'
                    
                    else:
                        pass #syntax error: missing '('
                
                else:
                    pass #invalid syntax
            
            elif self.current_token.token_type == 'return':
                self.advance() #check for index

                expr = []

                while True:
                    if self.current_token.token_type == 'end_of_line': break
                    expr.append(self.current_token)

                    self.advance() #check for index ==> missing ';'
                
                result.append(Return(Expression(expr).parse()))
            
            else:
                if self.current_token.token_type == 'end_of_line':
                    if len(buffer) != 0:
                        result.append(Expr(Expression(buffer).parse()))
                        buffer = []
                    
                    else:
                        raise InvalidSyntax('\';\'', self.lines, self.current_token.line_count)

                elif self.current_token.token_type == 'value' or self.current_token.token_type == 'operator':
                    buffer.append(self.current_token)
                
                else:
                    raise InvalidSyntax(f'\'{self.current_token.value}\'', self.lines, self.current_token.line_count)

            
            if self.current_pos < len(self.tokens) - 1: self.advance()
            else: break
        
        if len(buffer) != 0:
            pass #syntax error: missing ';'
        
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

class NegativeValueNode:
    def __init__(self, value):
        self.value = value
    
    def __repr__(self):
        return f'-({self.value})'


class Expression:
    def __init__(self, tokens: list):
        self.current_token = None
        self.tokens = iter(tokens)

        self.advance()

        self.opened = []
    
    def advance(self):
        try:
            self.current_token = next(self.tokens)
        
        except StopIteration:
            self.current_token = None
    
    def parse(self):
        if self.current_token == None:
            return None
        
        result = self.array_operators()

        if self.current_token != None:
            pass #invalid syntax
        
        return result
    
    def array_operators(self):
        result = self.logical_operators()

        while self.current_token != None and self.current_token.token_type == 'operator' and self.current_token.value == 'comma':
            self.advance()
            result = BinaryOperation(result, 'array', self.logical_operators())
        
        return result
    
    def logical_operators(self):
        result = self.low_binary_operators()

        while self.current_token != None and self.current_token.token_type == 'operator' and self.current_token.value in ('equal', 'not_equal', 'greater_equal', 'less_equal', 'or', 'and'):
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

        while self.current_token != None and self.current_token.token_type == 'operator' and self.current_token.value in ('mul', 'div'):
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

        if current_token.token_type == 'operator':
            if current_token.value == 'l_paren':
                self.opened.append(current_token)
                self.advance()
                result = self.array_operators()

                if self.current_token != 'r_paren':
                    pass #unclosed '('

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
        



