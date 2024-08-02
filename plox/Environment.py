from Token import Token
from RuntimeErr import RuntimeErr

class Environment:
    value_map = {}

    def define(self, name: str, value):
        self.value_map[name] = value
    
    def get(self, name: Token):
        if name.lexeme in Token:
            return self.map[name.lexeme]
        
        raise RuntimeErr(name, "Undefined variable '" + name.lexeme + "'.")
    
    def assign(self, name: Token, value):
        if (name.lexeme in self.value_map):
            self.value_map[name.lexeme] = value
        
        raise RuntimeErr(name, "Undefined variable '" + name.lexeme + "'.")
    