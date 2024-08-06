from abc import ABC, abstractmethod
from Environment import Environment
from Stmt import Function

class LoxCallable(ABC):
    @abstractmethod
    def call(self, interpreter, arguments):
        pass

    @abstractmethod
    def arity(self):
        pass

class LoxFunction(LoxCallable):
    def __init__(self, declaration: Function):
        self.declaration = declaration

    def call(self, interpreter, arguments):
        environment = Environment(interpreter.global_scope)
        for i in range(len(self.declaration.params)):
            environment.define(self.declaration.params[i].lexeme, arguments[i])
        
        interpreter.executeBlock(self.declaration.body, environment)
        return None
    
    def arity(self):
        return len(self.declaration.params)
    
    def __str__(self):
        return "<fn " + self.declaration.name.lexeme + ">"