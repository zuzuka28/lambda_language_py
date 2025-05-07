import inspect
import uuid
from LambdaVisitor import LambdaVisitor
from environment import initial_environment
from ast_tree import (
    Abstraction,
    Application,
    Variable,
    Number,
    Boolean,
    IfExpression,
    BinaryOperation,
    LetExpression,
    UnaryOperation,
    BuiltinFunction,
    String,
    List,
    Tuple,
    RangeExpression,
)


class CustomVisitor(LambdaVisitor):
    def visitProg(self, ctx):
        return self.visit(ctx.expr())

    def visitApplicationExpr(self, ctx):
        return Application(self.visit(ctx.expr(0)), self.visit(ctx.expr(1)))

    def visitAbstractionExpr(self, ctx):
        abstraction_ctx = ctx.abstraction()
        params = [Variable(id.getText()) for id in abstraction_ctx.ID()]
        body = self.visit(abstraction_ctx.expr())

        for param in reversed(params):
            body = Abstraction(param, body)

        return body

    def visitParenExpr(self, ctx):
        return self.visit(ctx.expr())

    def visitAtomExpr(self, ctx):
        atom_ctx = ctx.atom()
        if atom_ctx.ID():
            id = atom_ctx.ID().getText()

            if id in initial_environment:
                func = initial_environment[id]

                sig = inspect.signature(func)

                params = [
                    Variable(uuid.uuid4().hex) for _ in range(0, len(sig.parameters))
                ]
                body = Application(
                    BuiltinFunction(uuid.uuid4().hex, id, func), Tuple(params)
                )

                for param in reversed(params):
                    body = Abstraction(param, body)

                return body

            return Variable(id)
        elif atom_ctx.NUMBER():
            return Number(float(atom_ctx.NUMBER().getText()))
        elif atom_ctx.BOOLEAN():
            return Boolean(atom_ctx.BOOLEAN().getText().lower() == "true")
        elif atom_ctx.STRING():
            text = atom_ctx.STRING().getText()[1:-1]
            text = text.replace('\\"', '"').replace("\\\\", "\\")
            return String(text)

    def visitIfExpr(self, ctx):
        condition = self.visit(ctx.expr(0))
        then_expr = self.visit(ctx.expr(1))
        else_expr = self.visit(ctx.expr(2))
        return IfExpression(condition, then_expr, else_expr)

    def visitMulDivExpr(self, ctx):
        left = self.visit(ctx.expr(0))
        op = ctx.op.text
        right = self.visit(ctx.expr(1))
        return BinaryOperation(left, op, right)

    def visitAddSubExpr(self, ctx):
        left = self.visit(ctx.expr(0))
        op = ctx.op.text
        right = self.visit(ctx.expr(1))
        return BinaryOperation(left, op, right)

    def visitNotExpr(self, ctx):
        expr = self.visit(ctx.expr())
        return UnaryOperation("!", expr)

    def visitAndExpr(self, ctx):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        return BinaryOperation(left, "&&", right)

    def visitOrExpr(self, ctx):
        left = self.visit(ctx.expr(0))
        right = self.visit(ctx.expr(1))
        return BinaryOperation(left, "||", right)

    def visitComparisonExpr(self, ctx):
        left = self.visit(ctx.expr(0))
        op = ctx.op.text
        right = self.visit(ctx.expr(1))
        return BinaryOperation(left, op, right)

    def visitLetExpr(self, ctx):
        var = Variable(ctx.ID().getText())
        bound_expr = self.visit(ctx.expr(0))
        body = self.visit(ctx.expr(1))
        return LetExpression(var, bound_expr, body)

    def visitListExpr(self, ctx):
        elements = [self.visit(expr) for expr in ctx.expr()] if ctx.expr() else []
        return List(elements)

    def visitTupleExpr(self, ctx):
        elements = [self.visit(expr) for expr in ctx.expr()] if ctx.expr() else []
        return Tuple(elements)

    def visitFullRangeExpr(self, ctx):
        start = self.visit(ctx.expr(0))
        step = self.visit(ctx.expr(1))
        end = self.visit(ctx.expr(2))
        return RangeExpression(start, end, step)

    def visitSimpleRangeExpr(self, ctx):
        start = self.visit(ctx.expr(0))
        end = self.visit(ctx.expr(1))
        return RangeExpression(start, end)
