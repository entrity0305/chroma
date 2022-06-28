class BuiltinFunction:
    def __init__(self, name: str = ''):
        self.name = name
        self.args = []
    
    def __repr__(self):
        return f'(function {self.name})'

class Println(BuiltinFunction):
    def run(self):
        self.args = [str(i) for i in self.args]
        print(' '.join(self.args))

        return 0

class Input(BuiltinFunction):
    def run(self):
        self.args = [str(i) for i in self.args]
        return input(' '.join(self.args))

class Integer(BuiltinFunction):
    def run(self):
        return int(self.args[0])

class Float(BuiltinFunction):
    def run(self):
        return float(self.args[0])

class String(BuiltinFunction):
    def run(self):
        return str(self.args[0])