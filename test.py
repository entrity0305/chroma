from chroma.lex import *
from chroma.parse import *
from chroma.compile import *

code = '''
#this function checks if integer N is a prime number
function is_prime(N) {
    var k = 2;

    while k < N 
    {
        if N % k == 0 {
            return 0;
        }

        k = k + 1;
    }

    return 1;
}


var is_this_number_prime = is_prime(13);

var x = 1;
x = 2;

print("Hello, world!");
'''

lex_test = Lexer(code)
lex_result = lex_test.lex()
print(lex_result)
parse_test = Parser(lex_result, code.split('\n'))
parse_result = parse_test.parse()
print(parse_result)