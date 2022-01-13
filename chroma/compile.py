from dataclasses import dataclass


class Var:
    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return f'VAR {self.name}\n'


def compile_statements(statements: list = []):
    result = []

    for current_pos in range(len(statements)):
        current_statement = statements[current_pos]

        current_statement_type = current_statement.statement_type

        if current_statement_type == 'VarDefine':
            result.append(Var(current_statement.name))
    
    return result
