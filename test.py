from chroma.lex import *
from chroma.parse import *
from chroma.compile import *

code = '''
###############
#comment test
############### 


var y = g() + 3; #this is how a variable is declared

#this is a comment
var z = g(
    f(
        4,
        5
    )(),
    3 + (1 * 2)
);
'''

lex_test = Lexer(code)
lex_result = lex_test.lex()
print(lex_result)
parse_test = Parser(lex_result, code.split('\n'))
parse_result = parse_test.parse()
print(parse_result)