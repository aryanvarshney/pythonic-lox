from Token import Token, TokenType
from Expr import Binary, Unary, Literal, Grouping
from Stmt import Expression, Print
from LoxError import LoxError

class Parser():
    class ParseError(Exception):
        pass

    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        statements = []
        while not self.isAtEnd():
            statements.append(self.statement())
        
        return statements

    def expression(self):
        return self.equality()
    
    def statement(self):
        if self.match([TokenType.PRINT]):
            return self.printStatement()
        return self.expressionStatement()
    
    def printStatement(self):
        value = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ':' after value.")
        return Print(value)
    
    def expressionStatement(self):
        expr = self.expression()
        self.consume(TokenType.SEMICOLON, "Expect ':' after value")
        return Expression(expr)
    
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
        
        return self.primary()
    
    def primary(self):
        if self.match([TokenType.FALSE]):
            return Literal(False)
        if self.match([TokenType.TRUE]):
            return Literal(True)
        if self.match([TokenType.NIL]):
            return Literal(None)
        if self.match([TokenType.NUMBER, TokenType.STRING]):
            return Literal(self.previous().literal)
        if self.match([TokenType.LEFT_PAREN]):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expect ')' after expression")
            return Grouping(expr)
        
        raise self.errorToken(self.peek(), "Expected Expression")
    
    def match(self, types):
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False
    
    def consume(self, type: TokenType, message: str):
        if self.check(type):
            return self.advance()
        raise self.errorToken(self.peek(), message)
    
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
            
