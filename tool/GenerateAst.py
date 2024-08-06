import argparse
from pathlib import Path

class GenerateAst:
    
    @staticmethod
    def main():
        parser = argparse.ArgumentParser(usage="Usage: python GenerateAst.py <output directory>")
        parser.add_argument('f', type=str, help="Provide a valid directory path")
        args = parser.parse_args()
        outputDir = args.f
        GenerateAst.defineAst(outputDir, "Expr", [
            "Assign     -> name: Token, value: Expr",
            "Binary     -> left: Expr, operator: Token, right: Expr",
            "Call       -> callee: Expr, paren: Token, arguments",
            "Grouping   -> expression: Expr",
            "Literal    -> value",
            "Logical    -> left: Expr, operator: Token, right: Expr",
            "Unary      -> operator: Token, right: Expr",
            "Variable   -> name: Token"
        ])

        GenerateAst.defineAst(outputDir, "Stmt", [
            "Block      -> statements",
            "Expression -> expression: Expr",
            "Function   -> name: Token, params, body",
            "If         -> condition: Expr, thenBranch: Stmt, elseBranch: Stmt",
            "Print      -> expression: Expr",
            "Var        -> name: Token, initializer: Expr",
            "While      -> condition: Expr, body: Stmt"
        ])
    
    @staticmethod
    def defineAst(outputDir: str, baseName: str, types):
        path = Path(outputDir).resolve() / (baseName + '.py')

        with open(path, 'w') as file:
            file.write("# Generated by tool/GenerateAst.py\n")
            file.write("from abc import ABC, abstractmethod\n")
            if baseName != "Expr":
                file.write("from Expr import Expr\n")
            file.write("from Token import Token\n\n")
            file.write("class " + baseName + "(ABC):\n")
            GenerateAst.defineVisitor(file, baseName, types)

            for type in types:
                parts = type.split('->')
                className = parts[0].strip()
                fields = parts[1].strip()
                GenerateAst.defineType(file, baseName, className, fields)
    
    @staticmethod
    def defineType(file, baseName: str, className: str, fieldList: str):
        file.write("class " + className + "(" + baseName + "):\n")

        fields = fieldList.split(', ')
        # Fields initialize
        for field in fields:
            end = field.find(':')
            name = field
            if end != -1:
                name = field[:end]
            file.write("    " + name + " = " + "None\n")

        # Constructor initialize
        file.write("    def __init__(self, " + fieldList + "):\n")
        for field in fields:
            end = field.find(':')
            name = field
            if end != -1:
                name = field[:end]
            file.write("        self." + name + " = " + name + "\n")
        file.write("\n")
        file.write("    def accept(self, visitor):\n")
        file.write("        return visitor.visit" + className + baseName + "(self)\n")
        file.write("\n")
    
    @staticmethod
    def defineVisitor(file, baseName: str, types):
        file.write("    class Visitor(ABC):\n")
        for type in types:
            typeName = type.split('->')[0].strip()
            file.write("        @abstractmethod\n")
            file.write("        def visit" + typeName + baseName + "(self, " + baseName + ": '" + typeName + "'):\n")
            file.write("            pass\n\n")
        


if __name__ == '__main__':
    GenerateAst.main()