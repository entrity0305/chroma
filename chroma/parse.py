from dataclasses import dataclass
from .lex import *


@dataclass
class VarDefine:
    name: Token
    expr: list

@dataclass
class Assign:
    name: list
    expr: list

@dataclass
class If:
    expr: list
    body: list
    else_body: list

@dataclass
class While:
    expr: list
    body: list

@dataclass
class Break:
    pass

@dataclass
class FunctionDefine:
    name: Token
    param: list
    body: list

@dataclass
class Return:
    expr: list

@dataclass
class Expr:
    expr: list


class Parser:
    def __init__(self, tokens: list = []):
        self.current_pos = 0
        if tokens != []:
            self.current_token = tokens[0]
        
        else:
            self.current_token = Token('none')

        self.tokens = tokens
    
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
                        self.advance() #check for index

                        expr = []

                        while True:
                            if self.current_token.token_type == 'end_of_line': break
                            expr.append(self.current_token)

                            self.advance() #check for index ==> missing ';'
                        
                        result.append(VarDefine(name, expr))

                    else:
                        if self.next_token().token_type == 'end_of_line': #when value is not initiallized
                            result.append(VarDefine(name, []))

                        else:
                            pass #invalid syntax

                else:
                    pass #invalid syntax
            
            elif self.current_token.token_type == 'assign':
                if len(buffer) != 0:
                    self.advance() #check for index

                    expr = []

                    while True:
                        if self.current_token.token_type == 'end_of_line': break
                        expr.append(self.current_token)

                        self.advance() #check for index ==> missing ';'
                    
                    result.append(Assign(buffer, expr))
                    buffer = []

                else:
                    pass #invalid syntax: invalid '='
            
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
                prev = If(expr, body_parser.parse(), [])

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
                        new = If(expr, body_parser.parse(), [])

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
                result.append(While(expr, body_parser.parse()))
            
            elif self.current_token.token_type == 'break':
                self.advance()
                result.append(Break())
            
            elif self.current_token.token_type == 'function':
                name = self.next_token() 
                if name.token_type == 'value': #check if name is valid
                    self.advance()
                    if self.next_token().token_type == 'invoke':
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
                
                result.append(Return(expr))
            
            else:
                if self.current_token.token_type == 'end_of_line':
                    if len(buffer) != 0:
                        result.append(Expr(buffer))
                        buffer = []
                    
                    else:
                        pass #syntax error: invalid ';'

                elif self.current_token.token_type == 'value' or self.current_token.token_type == 'operator':
                    buffer.append(self.current_token)
                
                else:
                    pass #invalid syntax 

            
            if self.current_pos < len(self.tokens) - 1: self.advance()
            else: break
        
        if len(buffer) != 0:
            pass #syntax error: missing ';'
        
        return result
        



class Expression:
    def __init__(self):
        pass


