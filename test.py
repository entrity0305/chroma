from chroma.lex import *
from chroma.parse import *
from chroma.compile import *

import time

code = '''
function foo(x)
{
    while x == 4 {
        var y = g(
            1, 2
        );
        break;
    }
}
'''
s = time.time()
lex_test = Lexer(code)
lex_result = lex_test.lex()
print(lex_result)
parse_test = Parser(lex_result, code.split('\n'))
parse_result = parse_test.parse()
print(parse_result)
compile_result = compile_statements(parse_result, code.split('\n'))

print('\n-----------------------------------------------------------------')
for line_num in range(len(compile_result)):
    if isinstance(compile_result[line_num], FunctionDef):
        curr = compile_result[line_num]
        print(f'function {curr.name}{tuple(curr.param)}', '{')
        for fline_num in range(len(curr.body)):
            print('    ', fline_num, curr.body[fline_num])
        print('}')

    else:
        print(line_num, compile_result[line_num])
print('-----------------------------------------------------------------')


print(f'took {time.time() - s} seconds')