from .exception import *

#TODO:
#   1. add function & return
#   2. add invoke
#   3. add array
#   4. add none

class Runnable:
    def __init__(self, lines, runnable_type: str = '', name: str = '', variables: list = [], commands: list = []):
        self.name = name
        self.runnable_type = runnable_type
        self.variables = variables
        variables.append({}) #local variables

        self.commands = commands
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
        for variable_scope in list(reversed(self.variables)):
            if var in variable_scope:
                return variable_scope[var]
        
        return

    def set_variable(self, var, value):
        for variable_scope in list(reversed(self.variables)):
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
            
            self.current_pos += 1

            
class Function:
    def __init__(self, lines, name: str = '', param: list = [], variables: list = [], commands: list = []):
        self.name = name
        self.param = param

        self.variables = variables
        self.commands = commands

        self.lines = lines
    
    def __repr__(self):
        return f'(function {self.name})'