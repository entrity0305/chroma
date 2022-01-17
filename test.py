from chroma.lex import *
from chroma.parse import *
from chroma.compile import *

code = '''
var x = f(
    1, g(
        3, 1 + 4
    )
);


if x == 1 {
    var y = 2 * x;
} elif (x == 2) {
    var y = 3 * x;
} else {
    var y = 4 * x;
}


function f(x) {
    return 2* +x ^ 3;
}
'''

lex_test = Lexer(code)
lex_result = lex_test.lex()
print(lex_result)
parse_test = Parser(lex_result, code.split('\n'))
parse_result = parse_test.parse()
print(parse_result)
#compile_result = compile_statements(parse_result)
#print(compile_result)