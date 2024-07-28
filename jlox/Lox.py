import argparse
from pathlib import Path

class Lox:
    def __init__(self):
        self.hadError = False

    def main(self):
        parser = argparse.ArgumentParser(usage="Usage: python Lox.py -f [script]")
        parser.add_argument('-f', type=str, help="Provide a valid file path")
        args = parser.parse_args()
        if (args.f):
            self.runFile(args.f)
        else:
            self.runPrompt()
    
    def runFile(self, file_path):
        p = Path(file_path)
        if not p.exists() and not p.is_file():
            raise SystemExit("Invalid file path: " + file_path)
        
        with p.open() as f:
            file = f.read()
        self.run(file)

        if self.hadError:
            SystemExit("There was an error in the code")
    
    def runPrompt(self):
        while True:
            line = input("> ")
            if line == "exit()":
                break
            self.run(line)
            self.hadError = False
        return
    
    def run(self, file):
        # scanner = Scanner(source)
        # tokens = scanner.scanTokens()

        # for token in tokens:
        #     print(token)
        return
    
    def error(self, line_number, message):
        self.report(line_number, "", message)
    
    def report(self, line_number, where, message):
        SystemError("[line " + str(line_number + "] Error" + where + ": " + message))
        self.hadError = True


if __name__ == '__main__':
    Lox().main()