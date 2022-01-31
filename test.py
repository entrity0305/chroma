from chroma.lex import *
from chroma.parse import *
from chroma.compile import *

code = '''
var PI = 3.141592;

var r = toint(input("반지름: "));

println(PI * r^2);
'''

lex_test = Lexer(code)
lex_result = lex_test.lex()
#print(lex_result)
parse_test = Parser(lex_result, code.split('\n'))
parse_result = parse_test.parse()
print(parse_result)
compile_result = compile_statements(parse_result)

print('\n-----------------------------------------------------------------')
for line_num in range(len(compile_result)):
    print(line_num, compile_result[line_num])
print('-----------------------------------------------------------------')