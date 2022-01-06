from chroma.lex import *
from chroma.parse import *

code = '''
function f(x, y, z) {
    var w = (x * z);

    return w + y / x;
}
'''

lex_test = Lexer(code)
lex_result = lex_test.lex()
print(lex_result)
parse_test = Parser(lex_result)
parse_result = parse_test.parse()
print(parse_result)