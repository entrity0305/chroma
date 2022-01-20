from dataclasses import dataclass


@dataclass
class Token:
    token_type: str = ''
    value: str = ''
    original: str = ''
    line_count: int = 0
    

IDENTIFIERS = {
    '{': 'begin',
    '}': 'end',
    ';': 'end_of_line',
    '=': 'assign'
}

OPERATORS = {
    '+': 'add',
    '-': 'sub',
    '*': 'mul',
    '/': 'div',
    '%': 'mod',
    '^': 'pow',
    '>': 'greater',
    '<': 'less',
    '>=': 'greater_equal',
    '<=': 'less_equal',
    '==': 'equal',
    '!=': 'not_equal',
    '||': 'or',
    '&&': 'and',
    '.': 'dot',
    ',': 'comma'
}

KEYWORDS = {
    'var': 'var',
    'if': 'if',
    'elif': 'elif',
    'else': 'else',
    'while': 'while',
    'break': 'break',
    'function': 'function',
    'return': 'return'
}


class Lexer:
    def __init__(self, code: str = ''):
        self.current_pos = 0
        code += '\n'
        self.current_char = code[0]

        self.value = ''

        self.is_comment = False

        self.code = code

        self.line_count = 0
    
    def advance(self):
        self.current_pos += 1
        self.current_char = self.code[self.current_pos]
    
    def next_char(self):
        if self.current_pos + 1 < len(self.code):
            return self.code[self.current_pos + 1]
        
        else:
            return ''
    
    def get_token(self):
        if self.value in KEYWORDS:
            tok = Token(KEYWORDS[self.value], value=self.value, original=self.value, line_count=self.line_count)
        
        else:
            tok = Token('value',value=self.value, original=self.value, line_count=self.line_count)

        self.value = ''
        return tok

    def lex(self):
        result = []

        while True:
            if self.current_pos >= len(self.code) - 1: break
            if not self.is_comment:
                if self.current_char == '\t': pass
                elif self.current_char == '\n':
                    if self.value != '':
                        result.append(self.get_token())

                    self.line_count += 1
                
                elif self.current_char == '#':
                    if self.value != '':
                        result.append(self.get_token())
                    
                    self.is_comment = True
                
                elif self.current_char == ' ':
                    if self.value != '':
                        result.append(self.get_token())
                
                elif self.current_char == '(':
                    if self.value != '':
                        result.append(self.get_token())
                        result.append(Token('operator', value='invoke', original='(', line_count=self.line_count))

                    result.append(Token('operator', value='l_paren', original='(', line_count=self.line_count))
                
                elif self.current_char == ')':
                    if self.value != '':
                            result.append(self.get_token())
                    
                    if self.next_char() == '(': #to check cases like f(1)(2)
                        result.append(Token('operator', value='r_paren', original=')', line_count=self.line_count))
                        result.append(Token('operator', value='invoke', original='(', line_count=self.line_count))
                        result.append(Token('operator', value='l_paren', original='(', line_count=self.line_count))
                        self.advance()
                    
                    else:
                        result.append(Token('operator', value='r_paren', original=')', line_count=self.line_count))

                
                elif self.current_char + self.next_char() in OPERATORS:
                    if self.value != '':
                        result.append(self.get_token())
                    
                    result.append(Token('operator', value=OPERATORS[self.current_char + self.next_char()], original=self.current_char + self.next_char(), line_count=self.line_count))
                    self.advance()
                
                elif self.current_char in OPERATORS:
                    if self.value != '':
                        result.append(self.get_token())
                    
                    result.append(Token('operator', value=OPERATORS[self.current_char], original=self.current_char, line_count=self.line_count))
                
                elif self.current_char in IDENTIFIERS:
                    if self.value != '':
                        result.append(self.get_token())
                    
                    result.append(Token(IDENTIFIERS[self.current_char], value=self.current_char, original=self.current_char, line_count=self.line_count))
                
                else:
                    self.value += self.current_char
            
            else:
                if self.current_char == '\n': 
                    self.is_comment = False

            self.advance()
        
        return result      