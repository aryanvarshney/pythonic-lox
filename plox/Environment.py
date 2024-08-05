from Token import Token
from RuntimeErr import RuntimeErr

class Environment:
    def __init__(self, enclosing: 'Environment'=None):
        self.enclosing = enclosing
        self.value_map = {}

    def define(self, name: str, value):
        self.value_map[name] = value
    
    def get(self, name: Token):
        if name.lexeme in self.value_map:
            return self.value_map[name.lexeme]
        if self.enclosing is not None:
            return self.enclosing.get(name)
        
        raise RuntimeErr(name, "Undefined variable '" + name.lexeme + "'.")
    
    def assign(self, name: Token, value):
        if (name.lexeme in self.value_map):
            self.value_map[name.lexeme] = value
            return
        elif self.enclosing is not None:
            self.enclosing.assign(name, value)
            return
        
        raise RuntimeErr(name, "Undefined variable '" + name.lexeme + "'.")
    