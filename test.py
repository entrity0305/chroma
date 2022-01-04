from chroma.lex import *
from chroma.parse import *

code = '''
if x == 2 {

} elif x == 3 {

} elif x == 4 {

} else {
    var y;
    var z = 5;
}
'''

lex_test = Lexer(code)
lex_result = lex_test.lex()
print(lex_result)
parse_test = Parser(lex_result)
parse_result = parse_test.parse()
print(parse_result)