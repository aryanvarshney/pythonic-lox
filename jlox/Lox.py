import argparse
from pathlib import Path
from Scanner import Scanner

class Lox:
    hadError = False

    @staticmethod
    def main():
        parser = argparse.ArgumentParser(usage="Usage: python Lox.py -f [script]")
        parser.add_argument('-f', type=str, help="Provide a valid file path")
        args = parser.parse_args()
        if (args.f):
            Lox.runFile(args.f)
        else:
            Lox.runPrompt()
    
    @staticmethod
    def runFile(file_path):
        p = Path(file_path)
        if not p.exists() and not p.is_file():
            raise SystemExit("Invalid file path: " + file_path)
        
        with p.open() as f:
            file = f.read()
        Lox.run(file)

        if Lox.hadError:
            SystemExit("There was an error in the code")
    
    @staticmethod
    def runPrompt():
        while True:
            line = input("> ")
            if line == "exit()":
                break
            Lox.run(line)
            Lox.hadError = False
        return
    
    @staticmethod
    def run(self, source):
        scanner = Scanner(source)
        tokens = scanner.scanTokens()

        for token in tokens:
            print(token.toString())
        return
    
    @staticmethod
    def error(line_number, message):
        Lox.report(line_number, "", message)
    
    @staticmethod
    def report(line_number, where, message):
        SystemError("[line " + str(line_number + "] Error" + where + ": " + message))
        Lox.hadError = True


if __name__ == '__main__':
    Lox.main()