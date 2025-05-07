# Generated from Lambda.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .LambdaParser import LambdaParser
else:
    from LambdaParser import LambdaParser

# This class defines a complete generic visitor for a parse tree produced by LambdaParser.

class LambdaVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by LambdaParser#prog.
    def visitProg(self, ctx:LambdaParser.ProgContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LambdaParser#AndExpr.
    def visitAndExpr(self, ctx:LambdaParser.AndExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LambdaParser#IfExpr.
    def visitIfExpr(self, ctx:LambdaParser.IfExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LambdaParser#ComparisonExpr.
    def visitComparisonExpr(self, ctx:LambdaParser.ComparisonExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LambdaParser#LetExpr.
    def visitLetExpr(self, ctx:LambdaParser.LetExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LambdaParser#AtomExpr.
    def visitAtomExpr(self, ctx:LambdaParser.AtomExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LambdaParser#TupleExpr.
    def visitTupleExpr(self, ctx:LambdaParser.TupleExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LambdaParser#OrExpr.
    def visitOrExpr(self, ctx:LambdaParser.OrExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LambdaParser#SimpleRangeExpr.
    def visitSimpleRangeExpr(self, ctx:LambdaParser.SimpleRangeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LambdaParser#AbstractionExpr.
    def visitAbstractionExpr(self, ctx:LambdaParser.AbstractionExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LambdaParser#ApplicationExpr.
    def visitApplicationExpr(self, ctx:LambdaParser.ApplicationExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LambdaParser#MulDivExpr.
    def visitMulDivExpr(self, ctx:LambdaParser.MulDivExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LambdaParser#FullRangeExpr.
    def visitFullRangeExpr(self, ctx:LambdaParser.FullRangeExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LambdaParser#NotExpr.
    def visitNotExpr(self, ctx:LambdaParser.NotExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LambdaParser#ListExpr.
    def visitListExpr(self, ctx:LambdaParser.ListExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LambdaParser#ParenExpr.
    def visitParenExpr(self, ctx:LambdaParser.ParenExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LambdaParser#AddSubExpr.
    def visitAddSubExpr(self, ctx:LambdaParser.AddSubExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LambdaParser#abstraction.
    def visitAbstraction(self, ctx:LambdaParser.AbstractionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by LambdaParser#atom.
    def visitAtom(self, ctx:LambdaParser.AtomContext):
        return self.visitChildren(ctx)



del LambdaParser