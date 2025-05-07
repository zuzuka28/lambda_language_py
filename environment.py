from LambdaVisitor import LambdaVisitor
from ast_tree import (
    Abstraction,
    Application,
    Value,
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


def func_expand(x):
    if isinstance(x, RangeExpression):
        step = x.step.value if x.step is not None else None

        if step is not None:
            gen = range(int(x.start.value), int(x.end.value) + 1, int(x.step.value))
        else:
            gen = range(int(x.start.value), int(x.end.value) + 1)

        return map(Number, map(float, gen))

    return x.elements


def func_map(func, x):
    if not isinstance(func, Abstraction):
        return x

    if not isinstance(x, (List, Tuple, RangeExpression)):
        return x

    expanded = func_expand(x)

    return List([func.body.reduce(func.param, el) for el in expanded])


def func_fold(func, start, x):
    if not isinstance(func, Abstraction) and not isinstance(func.body, Abstraction):
        return x

    if not isinstance(x, (List, Tuple, RangeExpression)):
        return x

    expanded = func_expand(x)
    accumulator = start

    for el in expanded:
        step_result_accum = func.body.reduce(func.param, accumulator)
        step_result = step_result_accum.body.reduce(step_result_accum.param, el)
        accumulator.value = step_result.value

    return accumulator


def func_filter(predicate, x):
    if not isinstance(predicate, Abstraction):
        return x

    expanded = func_expand(x)

    filtered_elements = [
        el for el in expanded if predicate.body.reduce(predicate.param, el).value
    ]

    return List(filtered_elements)


initial_environment = {
    "print": print,
    "expand": func_expand,
    "map": func_map,
    "fold": func_fold,
    "filter": func_filter,
}
