from chroma.lex import *
from chroma.parse import *
from chroma.compile import *
from chroma.runnable import *

import time

code = '''
var const_num = 56;

function add2(x) {
    const_num = 10;

    return x + const_num;
}


var y = add2(4);
var z = add2(6);


function fib(N) {
    if N == 0 || N == 1 {
        return 1;
    } else {
        return fib(N - 1) + fib(N - 2);
    }
}

var n1 = fib(1);
var n2 = fib(2);
var n3 = fib(3);
var n4 = fib(4);
var n5 = fib(5);
var n6 = fib(6);
var n7 = fib(7);

var a;


function geta() {
    return a;
}

function seta(x) {
    a = x;

    var b;

    function getb() {
        return b;
    }

    function setb(x) {
        b = x;
    }

    setb(72);

    return a + b;
}

var val = geta();
var val2 = seta(50);

var val3 = geta();


function is_prime(N) {
    var k = 2;

    while k < N {
        if N % k == 0 {
            return 0;
        }

        k = k + 1;
    }

    return 1;
}


var isp1 = is_prime(50);
var isp2 = is_prime(17);
var isp3 = is_prime(20);
var isp4 = is_prime(41);

'''
s = time.time()
lex_test = Lexer(code)
lex_result = lex_test.lex()
print(lex_result)
parse_test = Parser(lex_result, code.split('\n'))
parse_result = parse_test.parse()
print(parse_result)
compile_result = compile_statements(parse_result, code.split('\n'))

print('\n-----------------------------------------------------------------')
for line_num in range(len(compile_result)):
    if isinstance(compile_result[line_num], FunctionDef):
        curr = compile_result[line_num]
        print(f'function {curr.name}{tuple(curr.param)}', '{')
        for fline_num in range(len(curr.body)):
            print('    ', fline_num, curr.body[fline_num])
        print('}')

    else:
        print(line_num, compile_result[line_num])
print('-----------------------------------------------------------------')


print(f'took {time.time() - s} seconds')

main = Runnable(code.split('\n'), 'module', 'main', commands=compile_result)
main.run()

print(main.variables)
