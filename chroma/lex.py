from dataclasses import dataclass


@dataclass
class Token:
    token_type: str = ''
    value: str = ''
    original: str = ''
    line_count: int = 0
    

operators = {
    '+': 'add',
    '-': 'sub',
    '*': 'mul',
    '/': 'div',
    '%': 'mod',
    '^': 'pow',
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
    '!=': 'not_equal',
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
        'else': 'else',
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
        code += '\n'
        self.current_char = code[0]

        self.value = ''

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
    
    def lex(self):
        result = []

        while True:
            if self.current_pos >= len(self.code) - 1: break
            if self.current_char == '\t': pass
            elif self.current_char == '\n':
                if self.value != '':
                    result.append(Token('value', self.value, self.value, line_count=self.line_count))
                    self.value = ''

                self.line_count += 1
            
            elif self.current_char == '(':
                if self.value != '':
                    result.append(Token('value', self.value, self.value, line_count=self.line_count))
                    result.append(Token('operator', 'invoke', line_count=self.line_count))
                    self.value = ''

                result.append(Token('operator', 'l_paren', '(', line_count=self.line_count))

            elif self.current_char in keywords:
                if self.value in keywords[self.current_char]:
                    result.append(Token(keywords[self.current_char][self.value], self.value, self.value, line_count=self.line_count))
                    self.value = ''
                
                else:
                    if self.value != '':
                        result.append(Token('value', self.value, self.value, line_count=self.line_count))
                        self.value = ''
                
                if self.current_char in single_chars:
                    result.append(Token(single_chars[self.current_char], self.current_char, self.current_char, line_count=self.line_count))
            
            elif self.current_char + self.next_char() in double_chars:
                if self.value != '':
                    result.append(Token('value', self.value, self.value, line_count=self.line_count))
                    self.value = ''
                
                result.append(Token('operator', double_chars[self.current_char + self.next_char()], self.current_char + self.next_char(), line_count=self.line_count))
                self.advance()
            
            elif self.current_char in single_chars:
                if self.value != '':
                    result.append(Token('value', self.value, self.value, line_count=self.line_count))
                    self.value = ''
                
                result.append(Token(single_chars[self.current_char], self.current_char, self.current_char, line_count=self.line_count))
            
            elif self.current_char in operators:
                if self.value != '':
                    result.append(Token('value', self.value, self.value, line_count=self.line_count))
                    self.value = ''
                
                result.append(Token('operator', operators[self.current_char], self.current_char, line_count=self.line_count))

            
            else:
                self.value += self.current_char

            self.advance()
        
        return result      