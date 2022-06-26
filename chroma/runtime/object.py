from ..utils.exception import *
from ..compiler.compile import *
from .function import *
from ..builtins.types import *

#TODO:
#   1. add function & return [v]
#   2. add invoke [v]
#   3. add array [v]
#   4. add typeerror
#   5. handle with void


class Object:
    def __init__(self, lines, runnable_type: str = '', name: str = '', variables: list = [], commands: list = []):
        self.name = name
        self.runnable_type = runnable_type
        self.variables = variables
        variables.append({}) #local variables

        self.commands = commands + [End()]
        self.current_pos = 0

        self.operand_stack = []
        self.invoke_stack = []

        self.lines = lines
    
    def pop(self):
        if len(self.operand_stack) != 0:
            return self.operand_stack.pop()
        
        else:
            pass #this cannot be done normally
    
    def define_variable(self, var, value):
        self.variables[-1][var] = value
    
    def get_variable(self, var):
        for scope_index in range(len(self.variables) - 1, -1, -1):
            variable_scope = self.variables[scope_index]
            if var in variable_scope:
                return variable_scope[var]
        
        return

    def set_variable(self, var, value):
        for scope_index in range(len(self.variables) - 1, -1, -1):
            variable_scope = self.variables[scope_index]
            if var in variable_scope:
                variable_scope[var] = value
                return value
        
        return

    def run(self):
        while True:
            command = self.commands[self.current_pos]

            if command.command_type == 'end':
                break

            elif command.command_type == 'goto':
                self.current_pos = command.pos - 1
            
            elif command.command_type == 'ifzero':
                if self.pop() == 0:
                    self.current_pos = command.pos - 1

            elif command.command_type == 'var':
                self.define_variable(command.name, self.pop())
            
            elif command.command_type == 'assign':
                if self.get_variable(command.name) != None:
                    self.set_variable(command.name, self.pop())
                
                else:
                    raise UndefinedName(f'\'{command.name}\'', self.lines, command.line_count)
            
            elif command.command_type == 'function':
                self.define_variable(command.name, Function(self.lines, command.name, command.param, self.variables, command.body))
            
            elif command.command_type == 'pushnone':
                self.operand_stack.append(NONE())
            
            elif command.command_type == 'pushvoid':
                self.operand_stack.append(VOID())

            elif command.command_type == 'pushi':
                self.operand_stack.append(int(command.value))
            
            elif command.command_type == 'pushf':
                self.operand_stack.append(float(command.value))
            
            elif command.command_type == 'pushstr':
                self.operand_stack.append(str(command.value))

            elif command.command_type == 'load':
                load_value = self.get_variable(command.name)

                if load_value != None:
                    self.operand_stack.append(load_value)
                
                else:
                    raise UndefinedName(f'\'{command.name}\'', self.lines, command.line_count)
            #x - y --> [x, y] --> val1 = y, val2 = x --> val2 - val1
            elif command.command_type == 'add':
                val1 = self.pop()
                val2 = self.pop()
                self.operand_stack.append(val2 + val1)
            
            elif command.command_type == 'sub':
                val1 = self.pop()
                val2 = self.pop()
                self.operand_stack.append(val2 - val1)
            
            elif command.command_type == 'neg':
                self.operand_stack.append(-self.pop())
            
            elif command.command_type == 'mul':
                val1 = self.pop()
                val2 = self.pop()
                self.operand_stack.append(val2 * val1)
            
            elif command.command_type == 'div':
                val1 = self.pop()
                val2 = self.pop()

                if val1 != 0:
                    self.operand_stack.append(val2 / val1)
                
                else:
                    raise ZeroDivision('division by zero', self.lines, command.line_count)
            
            elif command.command_type == 'mod':
                val1 = self.pop()
                val2 = self.pop()

                if val1 != 0:
                    self.operand_stack.append(val2 % val1)
                
                else:
                    raise ZeroDivision('division by zero', self.lines, command.line_count)
            
            elif command.command_type == 'pow':
                val1 = self.pop()
                val2 = self.pop()
                self.operand_stack.append(val2 ** val1)
            
            elif command.command_type == 'greater':
                val1 = self.pop()
                val2 = self.pop()
                self.operand_stack.append(int(val2 > val1))
            
            elif command.command_type == 'less':
                val1 = self.pop()
                val2 = self.pop()
                self.operand_stack.append(int(val2 < val1))
            
            elif command.command_type == 'greater_equal':
                val1 = self.pop()
                val2 = self.pop()
                self.operand_stack.append(int(val2 >= val1))
            
            elif command.command_type == 'less_equal':
                val1 = self.pop()
                val2 = self.pop()
                self.operand_stack.append(int(val2 <= val1))
            
            elif command.command_type == 'equal':
                val1 = self.pop()
                val2 = self.pop()
                self.operand_stack.append(int(val2 == val1))
            
            elif command.command_type == 'not_equal':
                val1 = self.pop()
                val2 = self.pop()
                self.operand_stack.append(int(val2 != val2))
            
            elif command.command_type == 'or':
                val1 = self.pop()
                val2 = self.pop()
                self.operand_stack.append(int(val2 or val1))
            
            elif command.command_type == 'and':
                val1 = self.pop()
                val2 = self.pop()
                self.operand_stack.append(int(val2 and val1))
            
            elif command.command_type == 'array':
                val1 = self.pop()
                val2 = self.pop()

                if isinstance(val2, list):
                    if isinstance(val1, list):
                        self.operand_stack.append(val2 + val1)

                    else:
                        self.operand_stack.append(val2 + [val1])
                else:
                    if isinstance(val1, list):
                        self.operand_stack.append([val2] + val1)
                    
                    else:
                        self.operand_stack.append([val2] + [val1])
            
            elif command.command_type == 'invoke':
                val1 = self.pop()
                val2 = self.pop()    
                
                new_invoke = invoke(val2, val1) #check if val2 is invokable
                self.operand_stack.append(new_invoke.run())
            
            elif command.command_type == 'return':
                return self.pop()

            
            self.current_pos += 1
        
        return NONE()


def format_args(args):
    if isinstance(args, VOID):
        return ()
    
    elif isinstance(args, list):
        return tuple(args)
    
    else:
        return tuple([args])

def invoke(func, args):
    #check args and param
    args = format_args(args)

    new_invoke_variable = []

    for variable_scope in func.variables:
        new_invoke_variable.append(variable_scope)
    
    new_invoke = Object(func.lines, 'function', func.name, new_invoke_variable, func.commands)
    
    local_from_args = {}

    for param_index in range(len(func.param)):
        local_from_args[func.param[param_index]] = args[param_index]
    
    new_invoke.variables[-1] = local_from_args

    return new_invoke