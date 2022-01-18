from chroma.lex import *
from chroma.parse import *
from chroma.compile import *

code = '''
function is_prime(N) {
    var k = 0;

    while k < N 
    {
        if N % k == 0 {
            return 0;
        }

        k = k + 1;
    }

    return 1;
}


println(is_prime(37));
'''

lex_test = Lexer(code)
lex_result = lex_test.lex()
print(lex_result)
parse_test = Parser(lex_result, code.split('\n'))
parse_result = parse_test.parse()
print(parse_result)
#compile_result = compile_statements(parse_result)
#print(compile_result)