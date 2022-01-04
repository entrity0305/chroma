from collections import namedtuple

Add = namedtuple('Add', ())
Sub = namedtuple('Sub', ())
Mul = namedtuple('Mul', ())
Div = namedtuple('Div', ())
Pow = namedtuple('Pow', ())
Assign = namedtuple('Assign', ('name'), defaults=(''))
Var = namedtuple('Var', ('name'), defaults=(''))
Goto = namedtuple('Goto', ('pos'), defaults=(0))
Ifzero = namedtuple('IfZero', ('pos'), defaults=(0))
Push = namedtuple('Push', ('value'), defaults=(0))
