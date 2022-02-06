from chroma.lex import *
from chroma.parse import *
from chroma.compile import *
from chroma.runnable import *

import time

code = '''
var test_array = (1, (2, 3), 4, (5, (7, 8)));

function add2(x, y) 
{
    return x + y;
}

var x = add2; #function reference


var y = add2(
    add2(
        add2(
            4, 7
        ),
        add2(
            3, 6
        )
    ),
    8
);

var val = add2(5, add2(3, 5));



function triangle(a, h) { return 1/2 * a * h; }

var s = triangle(4, triangle(3, 4));

var test_str = "Hello, world!";


function op(x, y, z) {
    var const = 3;

    function add2(x, y) {
        return x + y + const;
    }

    return add2(x, y) * z;
}


var val2 = op(2, 3, 4);
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
