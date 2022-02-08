from chroma.lex import *
from chroma.parse import *
from chroma.compile import *
from chroma.runnable import *

import time


with open('test.chr', 'r', encoding='UTF-8') as file:
    code = ''.join(file.readlines())

s = time.time()
lex_test = Lexer(code)
lex_result = lex_test.lex()
#print(lex_result)
parse_test = Parser(lex_result, code.split('\n'))
parse_result = parse_test.parse()
#print(parse_result)
compile_result = compile_statements(parse_result, code.split('\n'))




main = Runnable(code.split('\n'), 'module', 'main', commands=compile_result)
main.run()

print(main.variables)
print(f'took {time.time() - s} seconds')
