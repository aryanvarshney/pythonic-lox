from Expr import Expr, Binary, Grouping, Literal, Unary

class AstPrinter(Expr.Visitor):

    def print(self, expr: Expr):
        return expr.accept(self)

    def visitBinaryExpr(self, expr: Binary):
        return self.parenthisize(expr.operator.lexeme, [expr.left, expr.right])
    
    def visitGroupingExpr(self, expr: Grouping):
        return self.parenthisize("group", [expr.expression])
    
    def visitLiteralExpr(self, expr: Literal):
        if expr.value is None:
            return "nil"
        return str(expr.value)
    
    def visitUnaryExpr(self, expr: Unary):
        return self.parenthisize(expr.operator.lexeme, [expr.right])
    
    def parenthisize(self, name, expr_list):
        out = "(" + name
        for expr in expr_list:
            out += " " + expr.accept(self)
        out += ")"
        return out
