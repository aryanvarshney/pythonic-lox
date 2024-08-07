from Expr import Expr, Grouping, Literal, Unary, Binary, Assign, Variable, Logical, Call
from Stmt import Stmt, Print, Expression, Block, Var, If, While, Function, Return
from Token import Token
from LoxError import LoxError
from Interpreter import Interpreter
from enum import Enum

class FunctionType(Enum):
    NONE = "nil"
    FUNCTION = "function"

class Resolver(Expr.Visitor, Stmt.Visitor):
    def __init__(self, interpreter: Interpreter):
        self.interpreter = interpreter
        self.scopes = []
        self.currentFunction = FunctionType.NONE
        self.hadError = False

    def resolveStmts(self, statements):
        for statement in statements:
            self.resolveStmt(statement)
    
    def resolveStmt(self, Stmt: Stmt):
        Stmt.accept(self)
    
    def resolveExpr(self, Expr: Expr):
        Expr.accept(self)
    
    def resolveFunction(self, function: Function, type: FunctionType):
        enclosingFunction = self.currentFunction
        self.currentFunction = type
        
        self.beginScope()
        for param in function.params:
            self.declare(param)
            self.define(param)
        self.resolveStmts(function.body)
        self.endScope()
        self.currentFunction = enclosingFunction
    
    def beginScope(self):
        self.scopes.append({})
    
    def endScope(self):
        self.scopes.pop()

    def declare(self, name: Token):
        if len(self.scopes) == 0:
            return
        scope = self.scopes[-1]
        if name.lexeme in scope:
            self.hadError = True
            LoxError.errorToken(name, "Already a variable with this in this scope.")
        scope[name.lexeme] = False

    def resolveLocal(self, Expr: Expr, name: Token):
        for i in reversed(range(len(self.scopes))):
            if name.lexeme in self.scopes[i]:
                self.interpreter.resolve(Expr, len(self.scope) - 1 - i)
                return
    
    def define(self, name: Token):
        if len(self.scopes) == 0:
            return
        
        self.scopes[-1][name.lexeme] = True
    
    def visitBlockStmt(self, Stmt: Block):
        self.beginScope()
        self.resolveStmts(Stmt.statements)
        self.endScope()
    
    def visitExpressionStmt(self, Stmt: Expression):
        self.resolveExpr(Stmt.expression)
    
    def visitFunctionStmt(self, Stmt: Function):
        self.declare(Stmt.name)
        self.define(Stmt.name)

        self.resolveFunction(Stmt, FunctionType.FUNCTION)

    def visitIfStmt(self, Stmt: If):
        self.resolveExpr(Stmt.condition)
        self.resolveStmt(Stmt.thenBranch)
        if Stmt.elseBranch is not None:
            self.resolveStmt(Stmt.elseBranch)
    
    def visitPrintStmt(self, Stmt: Print):
        self.resolveExpr(Stmt.expression)
    
    def visitReturnStmt(self, Stmt: Return):
        if self.currentFunction == FunctionType.NONE:
            self.hadError = True
            LoxError.errorToken(Stmt.keyword, "Can't return from top level code.")

        if Stmt.value is not None:
            self.resolveExpr(Stmt.value)
    
    def visitVarStmt(self, Stmt: Var):
        self.declare(Stmt.name)
        if Stmt.initializer is not None:
            self.resolveExpr(Stmt.initializer)
        self.define(Stmt.name)

    def visitWhileStmt(self, Stmt: While):
        self.resolveExpr(Stmt.condition)
        self.resolveStmt(Stmt.body)
    
    def visitVariableExpr(self, Expr: Variable):
        if len(self.scopes) != 0 and Expr.name.lexeme in self.scopes[-1] and self.scopes[-1][Expr.name.lexeme] == False:
            self.hadError = True
            LoxError.errorToken(Expr.name, "Can't read local variable in its own initializer")
        
        self.resolveLocal(Expr, Expr.name)
    
    def visitAssignExpr(self, Expr: Assign):
        self.resolveExpr(Expr.value)
        self.resolveLocal(Expr, Expr.name)
    
    def visitBinaryExpr(self, Expr: Binary):
        self.resolveExpr(Expr.left)
        self.resolveExpr(Expr.right)

    def visitCallExpr(self, Expr: Call):
        self.resolveExpr(Expr.callee)

        for argument in Expr.arguments:
            self.resolveExpr(argument)
    
    def visitGroupingExpr(self, Expr: Grouping):
        self.resolveExpr(Expr.expression)
    
    def visitLiteralExpr(self, Expr: Literal):
        return
    
    def visitLogicalExpr(self, Expr: Logical):
        self.resolveExpr(Expr.left)
        self.resolveExpr(Expr.right)
    
    def visitUnaryExpr(self, Expr: Unary):
        self.resolveExpr(Expr.right)