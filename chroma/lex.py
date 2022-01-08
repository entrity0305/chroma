from dataclasses import dataclass


@dataclass
class Token:
    token_type: str = ''
    value: str = ''
    

operators = {
    '+': 'add',
    '-': 'sub',
    '*': 'mul',
    '/': 'div',
    '^': 'pow',
    '%': 'mod',
    '>': 'greater',
    '<': 'less',
    '.': 'dot',
    ',': 'comma',
    ')': 'r_paren'
}

single_chars = {
    '{': 'begin',
    '}': 'end',
    ';': 'end_of_line',
    '=': 'assign'
}

double_chars = {
    '==': 'equal',
    '>=': 'greater_equal',
    '<=': 'less_equal',
    '||': 'or',
    '&&': 'and'
}

keywords = {
    ' ': {
        'var': 'var',
        'function': 'function',
        'return': 'return',
        'if': 'if',
        'elif': 'elif',
        'while': 'while'
    },
    '{': {
        'else': 'else'
    },
    ';': {
        'break': 'break'
    }
}


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
            
            elif self.current_char == '(':
                if self.value != '':
                    result.append(Token('value', self.value))
                    result.append(Token('operator', 'invoke'))
                    self.value = ''

                result.append(Token('operator', 'l_paren'))

            elif self.current_char in keywords:
                if self.value in keywords[self.current_char]:
                    result.append(Token(keywords[self.current_char][self.value]))
                    self.value = ''
                
                else:
                    if self.value != '':
                        result.append(Token('value', self.value))
                        self.value = ''
                
                if self.current_char in single_chars:
                    result.append(Token(single_chars[self.current_char]))
            
            elif self.current_char + self.next_char() in double_chars:
                if self.value != '':
                    result.append(Token('value', self.value))
                    self.value = ''
                
                result.append(Token(double_chars[self.current_char + self.next_char()]))
                self.advance()
            
            elif self.current_char in single_chars:
                if self.value != '':
                    result.append(Token('value', self.value))
                    self.value = ''
                
                result.append(Token(single_chars[self.current_char]))
            
            elif self.current_char in operators:
                if self.value != '':
                    result.append(Token('value', self.value))
                    self.value = ''
                
                result.append(Token('operator', operators[self.current_char]))

            
            else:
                self.value += self.current_char

            self.advance()
            self.line_pos += 1
        
        return result      