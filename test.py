from chroma.lex import *
from chroma.parse import *

code = '''
var x = 5 + 4;

x = 2 + 3;
'''

lex_test = Lexer(code)
lex_result = lex_test.lex()
print(lex_result)
parse_test = Parser(lex_result, code.split('\n'))
parse_result = parse_test.parse()
print(parse_result)