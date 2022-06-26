import argparse

from pychroma.lexer.lex import *
from pychroma.parser.parse import *
from pychroma.compiler.compile import *
from pychroma.runtime.object import *

argument_parser = argparse.ArgumentParser(description='chroma standard runtime')
argument_parser.add_argument('file')

args = argument_parser.parse_args()

file_name = args.file

try:
    with open(file_name, 'r', encoding='UTF-8') as file:
        code = ''.join(file.readlines())

except:
    print(f'something went wrong opening \'{file_name}\'')
    exit()

try:
    lex_result = Lexer(code).lex()
    parse_result = Parser(lex_result, code.split('\n')).parse()
    compile_result = compile_statements(parse_result, code.split('\n'))


    main = Object(code.split('\n'), 'module', 'main', commands=compile_result)
    main.run()
    print(main.variables)

except Exception as e:
    print(e)
    exit()

