import argparse
from pathlib import Path
from Scanner import Scanner
from Parser import Parser
from AstPrinter import AstPrinter

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
    def runFile(file_path: str):
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
    def run(source: str):
        scanner = Scanner(source)
        tokens = scanner.scanTokens()

        parser = Parser(tokens)
        expression = parser.parse()

        if Lox.hadError:
            return
        
        print(AstPrinter().print(expression))


if __name__ == '__main__':
    Lox.main()