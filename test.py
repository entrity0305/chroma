from chroma.lex import *
from chroma.parse import *

code = '''

function checkNum(N) {
    if N == 1 {
        return 1;
    } elif N == 2 {
        return 2;
    } 
    else
    {
        return 3;
    }

}

function add2Num(x, y) {
    return x + y;
}



var a_number = add2Num(add2Num(1, 2), 5) / 6;

var pi = 3.14;

var area = pi * 4^2;

a_number = 5;

checkNum(4 ^ 8);

var z = 1 == 5 && 4 != 2;

'''

lex_test = Lexer(code)
lex_result = lex_test.lex()
print(lex_result)
parse_test = Parser(lex_result, code.split('\n'))
parse_result = parse_test.parse()
print(parse_result)