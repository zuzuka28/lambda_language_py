# Generated from Lambda.g4 by ANTLR 4.13.2
from antlr4 import *
if "." in __name__:
    from .LambdaParser import LambdaParser
else:
    from LambdaParser import LambdaParser

# This class defines a complete listener for a parse tree produced by LambdaParser.
class LambdaListener(ParseTreeListener):

    # Enter a parse tree produced by LambdaParser#prog.
    def enterProg(self, ctx:LambdaParser.ProgContext):
        pass

    # Exit a parse tree produced by LambdaParser#prog.
    def exitProg(self, ctx:LambdaParser.ProgContext):
        pass


    # Enter a parse tree produced by LambdaParser#AndExpr.
    def enterAndExpr(self, ctx:LambdaParser.AndExprContext):
        pass

    # Exit a parse tree produced by LambdaParser#AndExpr.
    def exitAndExpr(self, ctx:LambdaParser.AndExprContext):
        pass


    # Enter a parse tree produced by LambdaParser#IfExpr.
    def enterIfExpr(self, ctx:LambdaParser.IfExprContext):
        pass

    # Exit a parse tree produced by LambdaParser#IfExpr.
    def exitIfExpr(self, ctx:LambdaParser.IfExprContext):
        pass


    # Enter a parse tree produced by LambdaParser#ComparisonExpr.
    def enterComparisonExpr(self, ctx:LambdaParser.ComparisonExprContext):
        pass

    # Exit a parse tree produced by LambdaParser#ComparisonExpr.
    def exitComparisonExpr(self, ctx:LambdaParser.ComparisonExprContext):
        pass


    # Enter a parse tree produced by LambdaParser#LetExpr.
    def enterLetExpr(self, ctx:LambdaParser.LetExprContext):
        pass

    # Exit a parse tree produced by LambdaParser#LetExpr.
    def exitLetExpr(self, ctx:LambdaParser.LetExprContext):
        pass


    # Enter a parse tree produced by LambdaParser#AtomExpr.
    def enterAtomExpr(self, ctx:LambdaParser.AtomExprContext):
        pass

    # Exit a parse tree produced by LambdaParser#AtomExpr.
    def exitAtomExpr(self, ctx:LambdaParser.AtomExprContext):
        pass


    # Enter a parse tree produced by LambdaParser#TupleExpr.
    def enterTupleExpr(self, ctx:LambdaParser.TupleExprContext):
        pass

    # Exit a parse tree produced by LambdaParser#TupleExpr.
    def exitTupleExpr(self, ctx:LambdaParser.TupleExprContext):
        pass


    # Enter a parse tree produced by LambdaParser#OrExpr.
    def enterOrExpr(self, ctx:LambdaParser.OrExprContext):
        pass

    # Exit a parse tree produced by LambdaParser#OrExpr.
    def exitOrExpr(self, ctx:LambdaParser.OrExprContext):
        pass


    # Enter a parse tree produced by LambdaParser#SimpleRangeExpr.
    def enterSimpleRangeExpr(self, ctx:LambdaParser.SimpleRangeExprContext):
        pass

    # Exit a parse tree produced by LambdaParser#SimpleRangeExpr.
    def exitSimpleRangeExpr(self, ctx:LambdaParser.SimpleRangeExprContext):
        pass


    # Enter a parse tree produced by LambdaParser#AbstractionExpr.
    def enterAbstractionExpr(self, ctx:LambdaParser.AbstractionExprContext):
        pass

    # Exit a parse tree produced by LambdaParser#AbstractionExpr.
    def exitAbstractionExpr(self, ctx:LambdaParser.AbstractionExprContext):
        pass


    # Enter a parse tree produced by LambdaParser#ApplicationExpr.
    def enterApplicationExpr(self, ctx:LambdaParser.ApplicationExprContext):
        pass

    # Exit a parse tree produced by LambdaParser#ApplicationExpr.
    def exitApplicationExpr(self, ctx:LambdaParser.ApplicationExprContext):
        pass


    # Enter a parse tree produced by LambdaParser#MulDivExpr.
    def enterMulDivExpr(self, ctx:LambdaParser.MulDivExprContext):
        pass

    # Exit a parse tree produced by LambdaParser#MulDivExpr.
    def exitMulDivExpr(self, ctx:LambdaParser.MulDivExprContext):
        pass


    # Enter a parse tree produced by LambdaParser#FullRangeExpr.
    def enterFullRangeExpr(self, ctx:LambdaParser.FullRangeExprContext):
        pass

    # Exit a parse tree produced by LambdaParser#FullRangeExpr.
    def exitFullRangeExpr(self, ctx:LambdaParser.FullRangeExprContext):
        pass


    # Enter a parse tree produced by LambdaParser#NotExpr.
    def enterNotExpr(self, ctx:LambdaParser.NotExprContext):
        pass

    # Exit a parse tree produced by LambdaParser#NotExpr.
    def exitNotExpr(self, ctx:LambdaParser.NotExprContext):
        pass


    # Enter a parse tree produced by LambdaParser#ListExpr.
    def enterListExpr(self, ctx:LambdaParser.ListExprContext):
        pass

    # Exit a parse tree produced by LambdaParser#ListExpr.
    def exitListExpr(self, ctx:LambdaParser.ListExprContext):
        pass


    # Enter a parse tree produced by LambdaParser#ParenExpr.
    def enterParenExpr(self, ctx:LambdaParser.ParenExprContext):
        pass

    # Exit a parse tree produced by LambdaParser#ParenExpr.
    def exitParenExpr(self, ctx:LambdaParser.ParenExprContext):
        pass


    # Enter a parse tree produced by LambdaParser#AddSubExpr.
    def enterAddSubExpr(self, ctx:LambdaParser.AddSubExprContext):
        pass

    # Exit a parse tree produced by LambdaParser#AddSubExpr.
    def exitAddSubExpr(self, ctx:LambdaParser.AddSubExprContext):
        pass


    # Enter a parse tree produced by LambdaParser#abstraction.
    def enterAbstraction(self, ctx:LambdaParser.AbstractionContext):
        pass

    # Exit a parse tree produced by LambdaParser#abstraction.
    def exitAbstraction(self, ctx:LambdaParser.AbstractionContext):
        pass


    # Enter a parse tree produced by LambdaParser#atom.
    def enterAtom(self, ctx:LambdaParser.AtomContext):
        pass

    # Exit a parse tree produced by LambdaParser#atom.
    def exitAtom(self, ctx:LambdaParser.AtomContext):
        pass



del LambdaParser