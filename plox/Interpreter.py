from Expr import Expr, Grouping, Literal, Unary, Binary, Assign, Variable, Logical
from Stmt import Stmt, Print, Expression, Block, Var, If
from Token import Token, TokenType
from RuntimeErr import RuntimeErr
from LoxError import LoxError
from Environment import Environment

class Interpreter(Expr.Visitor, Stmt.Visitor):
    hadRuntimeError = False
    environment = Environment()

    def interpret(self, statements):
        try:
            for statement in statements:
                self.execute(statement)
        except RuntimeErr as err:
            self.hadRuntimeError = True
            LoxError.runtimeError(err)
    
    def visitLiteralExpr(self, Expr: Literal):
        return Expr.value
    
    def visitLogicalExpr(self, Expr: Logical):
        left = self.evaluate(Expr.left)

        if Expr.operator.type == TokenType.OR:
            if self.isTruthy(left):
                return left
        else:
            if not self.isTruthy(left):
                return left
        
        return self.evaluate(Expr.left)
    
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
    
    def visitVariableExpr(self, Expr: Variable):
        return self.environment.get(Expr.name)
    
    def visitExpressionStmt(self, Stmt: Expression):
        self.evaluate(Stmt.expression)

    def visitIfStmt(self, Stmt: If):
        if self.isTruthy(self.evaluate(Stmt.condition)):
            self.execute(Stmt.thenBranch)
        elif Stmt.elseBranch is not None:
            self.execute(Stmt.elseBranch)
    
    def visitPrintStmt(self, Stmt: Print):
        value = self.evaluate(Stmt.expression)
        print(self.stringify(value))
    
    def visitVarStmt(self, Stmt: Var):
        value = None
        if Stmt.initializer is not None:
            value = self.evaluate(Stmt.initializer)
        
        self.environment.define(Stmt.name.lexeme, value)

    def visitAssignExpr(self, Expr: Assign):
        value = Expr.value
        self.environment.assign(Expr.name, value)
        return value
    
    def visitBlockStmt(self, Stmt: Block):
        self.executeBlock(Stmt.statements, Environment(self.environment))
    
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
        raise RuntimeErr(operator, "Operand must be a number")
    
    def checkNumberOperands(self, operator: Token, left, right):
        if type(left) == float and type(right) == float:
            return
        raise RuntimeErr(operator, "Operands must be a number")
    
    def evaluate(self, Expr: Expr):
        return Expr.accept(self)
    
    def execute(self, stmt: Stmt):
        stmt.accept(self)
    
    def executeBlock(self, statements, environment: Environment):
        previous = self.environment
        try:
            self.environment = environment
            for statement in statements:
                self.execute(statement)
        finally:
            self.environment = previous
    
