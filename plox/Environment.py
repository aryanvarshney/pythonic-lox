from Token import Token
from RuntimeErr import RuntimeErr

class Environment:
    Map = {}

    def define(self, name: str, value):
        self.Map[name] = value
    
    def get(self, name: Token):
        if name.lexeme in Token:
            return self.map[name.lexeme]
        
        raise RuntimeErr(name, "Undefined variable '" + name.lexeme + "'.")
    
    