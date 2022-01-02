class VarDefine:
    def __init__(self, name, expr: list = []):
        self.name = name
        self.expr = expr
    
    def __repr__(self):
        return f'VarDefine(name={self.name}, expr={self.expr})'

class If:
    def __init__(self, expr, body: list = [], else_body: list = []):
        self.expr = expr
        self.body = body
        self.else_body = else_body
    
    def __repr__(self):
        return f'If(expr={self.expr}, body={self.body}, else={self.else_body})'

class Function:
    def __init__(self, name, param: list = [], body: list = []):
        self.name = name
        self.param = param
        self.body = body
    
    def __repr__(self):
        return f'Function(name={self.name}, param={self.param}, body={self.body})'