from chroma.lex import *
from chroma.parse import *

code = '''
var k = 0;
var N = 100;

while k < N {
    println(k);

    this.k = k + 1;
}
'''

lex_test = Lexer(code)
lex_result = lex_test.lex()
#print(lex_result)
parse_test = Parser(lex_result)
parse_result = parse_test.parse()
print(parse_result)