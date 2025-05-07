from antlr4 import InputStream, CommonTokenStream
from LambdaLexer import LambdaLexer
from LambdaParser import LambdaParser
from visitor import CustomVisitor
from ast_tree import ASTNode, normal_order_reduction, applicative_order_reduction


def lambda_expr_to_ast(expr: str) -> ASTNode:
    input_stream = InputStream(expr)
    lexer = LambdaLexer(input_stream)
    stream = CommonTokenStream(lexer)
    parser = LambdaParser(stream)
    tree = parser.prog()
    return CustomVisitor().visit(tree)


def evaluate_lambda_ast(ast: ASTNode, strategy="nor") -> str:
    if strategy == "nor":
        return normal_order_reduction(ast)
    elif strategy == "aor":
        return applicative_order_reduction(ast)


def evaluate_lambda_expr(expr: str, strategy="nor") -> str:
    ast = lambda_expr_to_ast(expr)
    return evaluate_lambda_ast(ast, strategy=strategy)
