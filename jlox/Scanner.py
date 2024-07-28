from Token import Token, TokenType, KEYWORDS
from Lox import Lox

DIGITS = '0123456789'

class Scanner:
    def __init__(self, source: str):
        self.source = source
        self.tokens = []
        self.start = 0
        self.current = 0
        self.line = 1

    def scanTokens(self):
        while not self.isAtEnd():
            self.start = self.current
            self.scanToken()
        
        self.tokens.append(Token(TokenType.EOF, "", None, self.line))
        return self.tokens
    
    def scanToken(self):
        c = self.advance()
        if c in "()}{,.-+;*":
            self.addToken(TokenType(c))
        elif c in "!=<>":
            if self.match('='):
                self.addToken(TokenType(c + '='))
            else:
                self.addToken(TokenType(c))
        elif c == '/':
            if self.match('/'):
                while self.peek() != '\n' and not self.isAtEnd():
                    self.advance()
            else:
                self.addToken(TokenType(c))
        elif c == ' ' or c == '\r' or c == '\t':
            pass
        elif c == '\n':
            self.line += 1
        elif c == '"':
            self.string()
        elif c in DIGITS:
            self.number()
        elif self.isAlpha(c):
            self.identifier()
        else:
            Lox.error(self.line, "Unexpecter Character.")

    def advance(self):
        c = self.source[self.current]
        self.current += 1
        return c
    
    def match(self, expected):
        if self.isAtEnd():
            return False
        if (self.source[self.current] != expected):
            return False
        
        self.current += 1
        return True
    
    def peek(self):
        if self.isAtEnd():
            return '\0'
        return self.source[self.current]

    def peekNext(self):
        if self.current + 1 >= len(self.source):
            return '\0'
        return self.source[self.current+1]
    
    def string(self):
        while self.peek() != '"' and not self.isAtEnd():
            if self.peek() == '\n':
                self.line += 1
            self.advance()
        if self.isAtEnd():
            Lox.error(self.line, "Unterminated string.")
            return
        self.advance()
        
        val = self.source[self.start+1:self.current-1]
        self.addToken(TokenType.STRING, val)
    
    def number(self):
        while self.peek() in DIGITS:
            self.advance()
        if self.peek() == '.' and self.peekNext() in DIGITS:
            self.advance()
            while self.peek() in DIGITS:
                self.advance()
        
        self.addToken(TokenType.NUMBER, float(self.source[self.start:self.current]))
    
    def identifier(self):
        while self.isAlphaNumeric(self.peek()):
            self.advance()
        
        text = self.source[self.start:self.current]
        if text in KEYWORDS:
            self.addToken(KEYWORDS[text])
        else:
            self.addToken(TokenType.IDENTIFIER)
    
    def addToken(self, type: TokenType):
        self.addToken(type, None)
    
    def addToken(self, type: TokenType, literal):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))
    
    def isAlpha(self, c):
        return (c >= 'a' and c <= 'z') or (c >= 'A' and c <= 'Z') or c == '_'
    
    def isAlphaNumeric(self, c):
        return self.isAlpha() or c in DIGITS
    
    def isAtEnd(self):
        return self.current >= len(self.source)