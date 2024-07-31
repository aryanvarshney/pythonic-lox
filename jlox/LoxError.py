from Token import Token, TokenType

class LoxError():
    @staticmethod
    def error(line_number: int, message: str):
        LoxError.report(line_number, "", message)

    @staticmethod
    def errorToken(token: Token, message: str):
        if token.type == TokenType.EOF:
            LoxError.report(token.line, " at end", message)
        else:
            LoxError.report(token.line, " at '" + token.lexeme + "'", message)
    
    @staticmethod
    def report(line_number: int, where: str, message: str):
        SystemError("[line " + str(line_number + "] Error" + where + ": " + message))