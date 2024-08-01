from Expr import Expr, Grouping, Literal, Unary, Binary
from Token import Token, TokenType
from RuntimeErr import RuntimeErr
from LoxError import LoxError

class Interpreter(Expr.Visitor):
    hadRuntimeError = False

    def interpret(self, expression: Expr):
        try:
            value = self.evaluate(expression)
            print(self.stringify(value))
        except RuntimeErr as err:
            LoxError.runtimeError(err)
    
    def visitLiteralExpr(self, Expr: Literal):
        return Expr.value
    
    def visitGroupingExpr(self, Expr: Grouping):
        return self.evaluate(Expr.expression)
    
    def visitUnaryExpr(self, Expr: Unary):
        right = self.evaluate(Expr.right)

        if Expr.operator.type == TokenType.MINUS:
            self.checkNumberOperand(Expr.operator, right)
            return -float(right)
        elif Expr.operator.type == TokenType.BANG:
            return not self.isTruthy(right)

        return None
    
    def visitBinaryExpr(self, Expr: Binary):
        left = self.evaluate(Expr.left)
        right = self.evaluate(Expr.right)

        if Expr.operator.type == TokenType.MINUS:
            self.checkNumberOperands(Expr.operator, left, right)
            return float(left) - float(right)
        if Expr.operator.type == TokenType.PLUS:
            if type(left) == float and type(right) == float:
                return float(left) + float(right)
            if type(left) == str and type(right) == str:
                return str(left) + str(right)
            raise RuntimeErr(Expr.operator, "Operands must be 2 numbers or 2 strings")
        if Expr.operator.type == TokenType.SLASH:
            self.checkNumberOperands(Expr.operator, left, right)
            return float(left) / float(right)
        if Expr.operator.type == TokenType.STAR:
            self.checkNumberOperands(Expr.operator, left, right)
            return float(left) * float(right)
        
        if Expr.operator.type == TokenType.GREATER:
            self.checkNumberOperands(Expr.operator, left, right)
            return float(left) > float(right)
        if Expr.operator.type == TokenType.GREATER_EQUAL:
            self.checkNumberOperands(Expr.operator, left, right)
            return float(left) >= float(right)
        if Expr.operator.type == TokenType.LESS:
            self.checkNumberOperands(Expr.operator, left, right)
            return float(left) < float(right)
        if Expr.operator.type == TokenType.LESS_EQUAL:
            self.checkNumberOperands(Expr.operator, left, right)
            return float(left) <= float(right)
        
        if Expr.operator.type == TokenType.BANG_EQUAL:
            return not self.isEqual(left, right)
        if Expr.operator.type == TokenType.EQUAL_EQUAL:
            return self.isEqual(left, right)
        
        return None
    
    def isTruthy(self, object):
        if object is None:
            return False
        if type(object) == bool:
            return object
        return True
    
    def isEqual(self, a, b):
        if a is None and b is None:
            return True
        if a is None:
            return False
        return a == b
    
    def stringify(self, object):
        if object is None:
            return "nil"
        if type(object) == float:
            text = str(object)
            if text.endswith('.0'):
                text = text[:-2]
            return text
        return str(object)
    
    def checkNumberOperand(self, operator: Token, operand):
        if type(operand) == float:
            return
        self.hadRuntimeError = True
        raise RuntimeErr(operator, "Operand must be a number")
    
    def checkNumberOperands(self, operator: Token, left, right):
        if type(left) == float and type(right) == float:
            return
        self.hadRuntimeError = True
        raise RuntimeErr(operator, "Operands must be a number")
    
    def evaluate(self, Expr: Expr):
        return Expr.accept(self)
    

     
