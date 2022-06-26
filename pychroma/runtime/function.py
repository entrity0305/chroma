class Function:
    def __init__(self, lines, name: str = '', param: list = [], variables: list = [], commands: list = []):
        self.name = name
        self.param = param

        self.variables = variables
        self.commands = commands

        self.lines = lines
    
    def __repr__(self):
        return f'(function {self.name})'