import argparse
from pathlib import Path

class Lox:
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
    
    def runPrompt(self):
        while True:
            line = input("> ")
            if line == "exit()":
                break
            self.run(line)
        return
    
    def run(self, file):
        return


if __name__ == '__main__':
    Lox().main()