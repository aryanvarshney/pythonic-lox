from Token import Token

class RuntimeErr(RuntimeError):
    token = None

    def __init__(self, token: Token, message: str):
        self.message = message
        self.token = token
    
    def getMessage(self):
        return self.message