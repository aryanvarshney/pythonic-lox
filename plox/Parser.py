from Token import Token, TokenType
from Expr import Expr, Binary, Unary, Literal, Grouping, Variable, Assign, Logical, Call
from Stmt import Expression, Print, Var, Block, If, While, Function, Return
from LoxError import LoxError

class Parser():
    class ParseError(Exception):
        pass
    
    counter = 0

    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
        self.hadError = False

    def parse(self):
        statements = []
        while not self.isAtEnd():
            statements.append(self.declaration())
        
        return statements

    def expression(self):
        return self.assignment()
    
    def declaration(self):
        try:
            if self.match([TokenType.FUN]):
                return self.function("function")
            if self.match([TokenType.VAR]):
                return self.varDeclaration()
            return self.statement()
        except self.ParseError:
            self.synchronize()
            return None
    
    def statement(self):
        if self.match([TokenType.FOR]):
            return self.forStatement()
        if self.match([TokenType.IF]):
            return self.ifStatement()
        if self.match([TokenType.PRINT]):
            return self.printStatement()
        if self.match([TokenType.RETURN]):
            return self.returnStatement()
        if self.match([TokenType.WHILE]):
            return self.whileStatement()
        if self.match([TokenType.LEFT_BRACE]):
            return Block(self.block())
        return self.expressionStatement()
    
    def forStatement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'for'.")

        initializer = None
        if self.match([TokenType.SEMICOLON]):
            initializer = None
        elif self.match([TokenType.VAR]):
            initializer = self.varDeclaration()
        else:
            initializer = self.expressionStatement()
        
        condition = None
        if not self.check(TokenType.SEMICOLON):
            condition = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ';' after loop condition.")

        increment = None
        if not self.check(TokenType.RIGHT_PAREN):
            increment = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after for clause.")

        body = self.statement()

        if increment is not None:
            body = Block([body, Expression(increment)])
        
        if condition is None:
            condition = Literal(True)
        body = While(condition, body)

        if initializer is not None:
            body = Block([initializer, body])
        
        return body
    
    def ifStatement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'if'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after if condition.")

        thenBranch = self.statement()
        elseBranch = None
        if self.match([TokenType.ELSE]):
            elseBranch = self.statement()
        
        return If(condition, thenBranch, elseBranch)
    
    def printStatement(self):
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ':' after value.")
        return Print(value)
    
    def returnStatement(self):
        keyword = self.previous()
        value = None
        if not self.check(TokenType.SEMICOLON):
            value = self.expression()
        
        self.consume(TokenType.SEMICOLON, "Expect ';' after return value.")
        return Return(keyword, value)
    
    def whileStatement(self):
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after 'while'.")
        condition = self.expression()
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after while condition.")
        body = self.statement()

        return While(condition, body)
    
    def varDeclaration(self):
        name = self.consume(TokenType.IDENTIFIER, "Expect variable name.")

        initializer = None
        if self.match([TokenType.EQUAL]):
            initializer = self.expression()

        self.consume(TokenType.SEMICOLON, "Expect ';' after variable declaration")
        return Var(name, initializer)
    
    def expressionStatement(self):
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ':' after value")
        return Expression(expr)
    
    def function(self, kind: str):
        name = self.consume(TokenType.IDENTIFIER, "Expect " + kind + " name.")
        self.consume(TokenType.LEFT_PAREN, "Expect '(' after " + kind + " name.")
        parameters = []
        if not self.check(TokenType.RIGHT_PAREN):
            parameters.append(self.consume(TokenType.IDENTIFIER, "Expect parameter name"))
            while self.match([TokenType.COMMA]):
                if len(parameters) >= 255:
                    self.error(self.peek(), "Can't have more than 255 parameters")
                parameters.append(self.consume(TokenType.IDENTIFIER, "Expect parameter name"))
        self.consume(TokenType.RIGHT_PAREN, "Expect ')' after parameters")

        self.consume(TokenType.LEFT_BRACE, "Expect '{' before " + kind + " body.")
        body = self.block()
        return Function(name, parameters, body)
    
    def block(self):
        statements = []

        while not self.check(TokenType.RIGHT_BRACE) and not self.isAtEnd():
            statements.append(self.declaration())
        
        self.consume(TokenType.RIGHT_BRACE, "Expect '}' after block")
        return statements
    
    def assignment(self):
        expr = self.orExpr()
        if self.match([TokenType.EQUAL]):
            equals = self.previous()
            value = self.assignment()

            if type(expr) == Variable:
                name = expr.name
                return Assign(name, value)
            
            self.error(equals, "Invalid assignment target")
        
        return expr
    
    def orExpr(self):
        expr = self.andExpr()

        while self.match([TokenType.OR]):
            operator = self.previous()
            right = self.andExpr()
            expr = Logical(expr, operator, right)
        
        return expr
    
    def andExpr(self):
        expr = self.equality()

        while self.match([TokenType.AND]):
            operator = self.previous()
            right = self.equality()
            expr = Logical(expr, operator, right)
        
        return expr
    
    def equality(self):
        expr = self.comparison()

        while self.match([TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL]):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)
        
        return expr
    
    def comparison(self):
        expr = self.term()

        while self.match([TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL]):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)
        
        return expr
    
    def term(self):
        expr = self.factor()

        while self.match([TokenType.MINUS, TokenType.PLUS]):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
        
        return expr
    
    def factor(self):
        expr = self.unary()

        while self.match([TokenType.SLASH, TokenType.STAR]):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)
        
        return expr
    
    def unary(self):
        if self.match([TokenType.BANG, TokenType.MINUS]):
            operator = self.previous()
            right = self.unary()
            return Unary(operator, right)
        
        return self.call()
    
    def call(self):
        expr = self.primary()

        while True:
            if self.match([TokenType.LEFT_PAREN]):
                expr = self.finishCall(expr)
            else:
                break
        
        return expr
    
    def finishCall(self, callee: Expr):
        arguments = []
        if not self.check(TokenType.RIGHT_PAREN):
            arguments.append(self.expression())
            while self.match([TokenType.COMMA]):
                if len(arguments) >= 255:
                    self.error(self.peek(), "Can't have more than 255 arguments.")
                arguments.append(self.expression())
        
        paren = self.consume(TokenType.RIGHT_PAREN, "Expect '(' after arguments.")
        return Call(callee, paren, arguments)
    
    def primary(self):
        if self.match([TokenType.FALSE]):
            return Literal(False)
        if self.match([TokenType.TRUE]):
            return Literal(True)
        if self.match([TokenType.NIL]):
            return Literal(None)
        if self.match([TokenType.NUMBER, TokenType.STRING]):
            return Literal(self.previous().literal)
        if self.match([TokenType.IDENTIFIER]):
            return Variable(self.previous())
        if self.match([TokenType.LEFT_PAREN]):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression")
            return Grouping(expr)
        
        raise self.error(self.peek(), "Expected Expression")
    
    def match(self, types):
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False
    
    def consume(self, type: TokenType, message: str):
        if self.check(type):
            return self.advance()
        raise self.error(self.peek(), message)
    
    def check(self, type: TokenType):
        if self.isAtEnd():
            return False
        return self.peek().type == type
    
    def advance(self):
        if not self.isAtEnd():
            self.current += 1
        return self.previous()
    
    def isAtEnd(self):
        return self.peek().type == TokenType.EOF
    
    def peek(self):
        return self.tokens[self.current]
    
    def previous(self):
        return self.tokens[self.current - 1]
    
    def error(self, token: Token, message: str):
        self.hadError = True
        LoxError.errorToken(token, message)
        return self.ParseError()
    
    def synchronize(self):
        self.advance()

        while not self.isAtEnd():
            if self.previous().type == TokenType.SEMICOLON:
                return
            
            if self.peek().type in set([TokenType.CLASS, TokenType.FUN, TokenType.VAR, TokenType.FOR, TokenType.IF, TokenType.WHILE, TokenType.PRINT, TokenType.RETURN]):
                return
            
            self.advance()
            
