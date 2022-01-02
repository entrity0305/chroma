from chroma.lex import *
from chroma.parse import *

code = '''
function add2num(x, y)
{
    function nested(p, q, r, k) {
        var w = (p + q + r) * k;
    }

    var k = nested(1, 2, 3, 4) + 1;
}
'''

lex_test = Lexer(code)
lex_result = lex_test.lex()
print(lex_result)
parse_test = Parser(lex_result)
parse_result = parse_test.parse()
print(parse_result)