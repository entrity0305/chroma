from chroma.lex import *
from chroma.parse import *
from chroma.compile import *

code = '''
if a == 1 
{
    if a == 2
    {
    }
}


function f(x, y, z) { return x + y + z; }
'''

lex_test = Lexer(code)
lex_result = lex_test.lex()
print(lex_result)
parse_test = Parser(lex_result, code.split('\n'))
parse_result = parse_test.parse()
print(parse_result)
#compile_result = compile_statements(parse_result)
#print(compile_result)