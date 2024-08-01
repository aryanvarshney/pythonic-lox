from Token import Token

class RuntimeErr(RuntimeError):
    token = None

    def __init__(self, token: Token, message: str):
        super(message)
        self.token = token