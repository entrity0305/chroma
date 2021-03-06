class InvalidSyntax(Exception):
    def __init__(self, message: str = '', lines: list = [], line_count: int = 0):
        super().__init__(f'At line {line_count+1},\n{lines[line_count]}\nInvalid Syntax: {message}')

class UndefinedName(Exception):
    def __init__(self, message: str = '', lines: list = [], line_count: int = 0):
        super().__init__(f'At line {line_count+1},\n{lines[line_count]}\nUndefined Name: {message}')

class ZeroDivision(Exception):
    def __init__(self, message: str = '', lines: list = [], line_count: int = 0):
        super().__init__(f'At line {line_count+1},\n{lines[line_count]}\nZero Division: {message}')