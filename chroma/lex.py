from collections import namedtuple

Token = namedtuple('Token', ('token_type', 'value'), defaults=('', ''))


class Lexer:
    def __init__(self, code: str = ''):
        self.current_pos = 0
        self.current_char = code[0]

        self.value = ''

        self.code = code

        self.line_count = 0
        self.line_pos = 0
    
    def advance(self):
        self.current_pos += 1
        self.current_char = self.code[self.current_pos]
    
    def next_char(self):
        if self.current_pos + 1 < len(self.code):
            return self.code[self.current_pos + 1]
        
        else:
            return ''
    
    def lex(self):
        result = []

        while True:
            if self.current_pos >= len(self.code) - 1: break
            if self.current_char == '\t': pass
            elif self.current_char == '\n':
                self.line_count += 1
                self.line_pos = 0

            elif self.current_char == ';':
                if self.value != '':
                    result.append(Token('value', self.value))
                    self.value = ''
                
                result.append(Token('end_of_line'))

            elif self.current_char == '+':
                if self.value != '':
                    result.append(Token('value', self.value))
                    self.value = ''
                
                result.append(Token('add'))

            elif self.current_char == '-':
                if self.value != '':
                    result.append(Token('value', self.value))
                    self.value = ''
                
                result.append(Token('sub'))
            
            elif self.current_char == '*':
                if self.value != '':
                    result.append(Token('value', self.value))
                    self.value = ''
                
                result.append(Token('mul'))
            
            elif self.current_char == '/':
                if self.value != '':
                    result.append(Token('value', self.value))
                    self.value = ''
                
                result.append(Token('div'))
            
            elif self.current_char == '^':
                if self.value != '':
                    result.append(Token('value', self.value))
                    self.value = ''
                
                result.append(Token('pow'))
            
            elif self.current_char == '%':
                if self.value != '':
                    result.append(Token('value', self.value))
                    self.value = ''
                
                result.append(Token('mod'))
            
            elif self.current_char == ',':
                if self.value != '':
                    result.append(Token('value', self.value))
                    self.value = ''
                
                result.append(Token('comma'))
            
            elif self.current_char == '.':
                if self.value != '':
                    result.append(Token('value', self.value))
                    self.value = ''
                
                result.append(Token('dot'))
            
            elif self.current_char == '<':
                if self.value != '':
                    result.append(Token('value', self.value))
                    self.value = ''
                
                if self.next_char() == '=':
                    self.advance()
                    result.append(Token('less_equal'))
                
                else:
                    result.append(Token('less'))
            
            elif self.current_char == '>':
                if self.value != '':
                    result.append(Token('value', self.value))
                    self.value = ''
                
                if self.next_char() == '=':
                    self.advance()
                    result.append(Token('greater_equal'))
                
                else:
                    result.append(Token('greater'))
            
            elif self.current_char == '=':
                if self.value != '':
                    result.append(Token('value', self.value))
                    self.value = ''
                
                if self.next_char() == '=':
                    self.advance()
                    result.append(Token('equal'))
                
                else:
                    result.append(Token('assign'))
            
            elif self.current_char == '(':
                if self.value != '':
                    result.append(Token('value', self.value))
                    self.value = ''
                    result.append(Token('invoke'))
                
                result.append(Token('lparen'))
            
            elif self.current_char == ')':
                if self.value != '':
                    result.append(Token('value', self.value))
                    self.value = ''

                result.append(Token('rparen'))
            
            elif self.current_char == '{':
                if self.value == 'else':
                    result.append(Token('else'))
                    self.value = ''
                else:
                    if self.value != '':
                        result.append(Token('value', self.value))
                        self.value = ''
                
                result.append(Token('begin'))
            
            elif self.current_char == '}':
                if self.value != '':
                    result.append(Token('value', self.value))
                    self.value = ''
                
                result.append(Token('end'))
                                
            elif self.current_char == ' ':
                if self.value == 'var':
                    result.append(Token('var'))
                    self.value = ''
                
                elif self.value == 'function':
                    result.append(Token('function'))
                    self.value = ''
                
                elif self.value == 'if':
                    result.append(Token('if'))
                    self.value = ''
                
                elif self.value == 'elif':
                    result.append(Token('elif'))
                    self.value = ''
                
                elif self.value == 'while':
                    result.append(Token('while'))
                    self.value = ''
            
            else:
                self.value += self.current_char

            self.advance()
            self.line_pos += 1
        
        return result      