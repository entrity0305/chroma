from chroma.lex import *
from chroma.parse import *

code = '''
if x == 2 {
var x = 3 + 2 / 3;
} 

function f(x, y ,z) {
}
'''

lex_test = Lexer(code)
lex_result = lex_test.lex()
print(lex_result)
parse_test = Parser(lex_result)
parse_result = parse_test.parse()
print(parse_result)