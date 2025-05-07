import copy
import uuid


def fresh_name(original: str, forbidden: set[str]) -> str:
    if original not in forbidden:
        return original

    i = 1
    while f"{original}{i}" in forbidden:
        i += 1
    return f"{original}{i}"


class ASTNode:
    def __repr__(self):
        return self.__str__()

    def __eq__(self, value):
        return self.__str__() == value.__str__()

    def free_variables(self):
        raise NotImplementedError()

    def bound_variables(self):
        raise NotImplementedError()

    def substitute(self, old: "Variable", new: "Variable") -> "ASTNode":
        raise NotImplementedError()

    def reduce(self, var: "Variable", new_expr: "ASTNode") -> "ASTNode":
        raise NotImplementedError()


class Variable(ASTNode):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

    def __hash__(self):
        return hash((self.name))

    def __eq__(self, other):
        if not isinstance(other, Variable):
            return False
        return (self.name) == (other.name)

    def free_variables(self):
        return set([self])

    def bound_variables(self):
        return set()

    def substitute(self, old: "Variable", new: "Variable"):
        if self == old:
            return new
        else:
            return self

    def reduce(self, var: "Variable", new_expr: "ASTNode"):
        if self == var:
            return new_expr
        else:
            return self


class Abstraction(ASTNode):
    def __init__(self, param: Variable, body: ASTNode):
        self.param = param
        self.body = body

    def __str__(self):
        return f"(\{self.param}.{self.body})"

    def __hash__(self):
        return hash((self.param, self.body))

    def __eq__(self, other):
        if not isinstance(other, Abstraction):
            return False
        return (self.param, self.body) == (other.param, other.body)

    def free_variables(self):
        return self.body.free_variables()

    def bound_variables(self):
        return self.param | self.body.bound_variables

    def substitute(self, old: "Variable", new: "Variable"):
        if self.param == old:
            return Abstraction(self.param, self.body)
        else:
            return Abstraction(self.param, self.body.substitute(old, new))

    def reduce(self, var: "Variable", new_expr: "ASTNode"):
        if var is None and new_expr is None:
            return self

        if self.param == var:
            return self
        else:
            if self.param not in new_expr.free_variables():
                return Abstraction(self.param, self.body.reduce(var, new_expr))

            new = Variable(fresh_name(self.param, new_expr.free_variables()))
            new_body = self.body.substitute(self.param, new)

            return Abstraction(new, new_body.reduce(var, new_expr))


class Application(ASTNode):
    def __init__(self, func: ASTNode, arg: ASTNode):
        self.func = func
        self.arg = arg

    def __str__(self):
        return f"({self.func} {self.arg})"

    def __hash__(self):
        return hash((self.func, self.arg))

    def __eq__(self, other):
        if not isinstance(other, Application):
            return False
        return (self.func, self.arg) == (other.func, other.arg)

    def free_variables(self):
        return self.func.free_variables() | self.arg.free_variables()

    def bound_variables(self):
        return self.func.bound_variables() | self.arg.bound_variables()

    def substitute(self, old: "Variable", new: "Variable"):
        return Application(
            self.func.substitute(old, new),
            self.arg.substitute(old, new),
        )

    def reduce(self, var: "Variable", new_expr: "ASTNode"):
        return Application(
            self.func.reduce(var, new_expr),
            self.arg.reduce(var, new_expr),
        )


class Value(ASTNode):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return f"{self.value}"

    def free_variables(self):
        return set()

    def bound_variables(self):
        return set()

    def substitute(self, old: "Variable", new: "Variable") -> "ASTNode":
        return self

    def reduce(self, var: "Variable", new_expr: "ASTNode") -> "ASTNode":
        return self


class Number(Value):
    pass


class Boolean(Value):
    def __str__(self):
        return "true" if self.value else "false"


class IfExpression(ASTNode):
    def __init__(self, condition: ASTNode, then_expr: ASTNode, else_expr: ASTNode):
        self.condition = condition
        self.then_expr = then_expr
        self.else_expr = else_expr

    def __str__(self):
        return f"(if {self.condition} then {self.then_expr} else {self.else_expr})"

    def free_variables(self):
        return (
            self.condition.free_variables()
            | self.then_expr.free_variables()
            | self.else_expr.free_variables()
        )

    def bound_variables(self):
        return (
            self.condition.bound_variables()
            | self.then_expr.bound_variables()
            | self.else_expr.bound_variables()
        )

    def substitute(self, var: Variable, replacement: ASTNode) -> ASTNode:
        return IfExpression(
            self.condition.substitute(var, replacement),
            self.then_expr.substitute(var, replacement),
            self.else_expr.substitute(var, replacement),
        )

    def reduce(self, var: "Variable", new_expr: "ASTNode"):
        if isinstance(self.condition, Application):
            reduced_cond = self.condition.func.body.reduce(
                self.condition.func.param, self.condition.arg
            )
        else:
            reduced_cond = self.condition.reduce(var, new_expr)

        reduced_then = self.then_expr.reduce(var, new_expr)
        reduced_else = self.else_expr.reduce(var, new_expr)

        if isinstance(reduced_cond, Boolean):
            return reduced_then if reduced_cond.value else reduced_else

        else:
            return IfExpression(reduced_cond, reduced_then, reduced_else)


class BinaryOperation(ASTNode):
    def __init__(self, left: ASTNode, op: str, right: ASTNode):
        self.left = left
        self.op = op
        self.right = right

    def __str__(self):
        return f"({self.left} {self.op} {self.right})"

    def free_variables(self):
        return self.left.free_variables() | self.right.free_variables()

    def bound_variables(self):
        return self.left.bound_variables() | self.right.bound_variables()

    def substitute(self, var: Variable, replacement: ASTNode) -> ASTNode:
        return BinaryOperation(
            self.left.substitute(var, replacement),
            self.op,
            self.right.substitute(var, replacement),
        )

    def reduce(self, var: "Variable", new_expr: "ASTNode"):
        left_reduced = self.left.reduce(var, new_expr)
        right_reduced = self.right.reduce(var, new_expr)

        if isinstance(left_reduced, Number) and isinstance(right_reduced, Number):
            ops = {
                "+": lambda x, y: x + y,
                "-": lambda x, y: x - y,
                "*": lambda x, y: x * y,
                "/": lambda x, y: x / y,
                "%": lambda x, y: x % y,
                "==": lambda x, y: x == y,
                "!=": lambda x, y: x != y,
                "<": lambda x, y: x < y,
                ">": lambda x, y: x > y,
                "<=": lambda x, y: x <= y,
                ">=": lambda x, y: x >= y,
            }

            if self.op in ops:
                result = ops[self.op](left_reduced.value, right_reduced.value)
                return (
                    Boolean(bool(result))
                    if self.op in {"==", "!=", "<", ">", "<=", ">="}
                    else Number(float(result))
                )

        if isinstance(left_reduced, Boolean) and isinstance(right_reduced, Boolean):
            ops = {
                "&&": lambda x, y: x and y,
                "||": lambda x, y: x or y,
            }

            if self.op in ops:
                result = ops[self.op](left_reduced.value, right_reduced.value)
                return Boolean(bool(result))

        return BinaryOperation(left_reduced, self.op, right_reduced)


class UnaryOperation(ASTNode):
    def __init__(self, op: str, value: ASTNode):
        self.op = op
        self.value = value

    def __str__(self):
        return f"({self.op} ({self.value}))"

    def free_variables(self):
        return self.value.free_variables()

    def bound_variables(self):
        return self.value.bound_variables()

    def substitute(self, var: Variable, replacement: ASTNode) -> ASTNode:
        return self.value.substitute(var, replacement)

    def reduce(self, var: "Variable", new_expr: "ASTNode"):
        value_reduced = self.value.reduce(var, new_expr)

        if isinstance(value_reduced, Boolean):
            ops = {
                "!": lambda x: not x,
            }

            if self.op in ops:
                result = ops[self.op](value_reduced.value)
                return Boolean(bool(result))

        return UnaryOperation(self.op, value_reduced)


class LetExpression(ASTNode):
    def __init__(self, var: Variable, bound_expr, body):
        self.var = var
        self.bound_expr = bound_expr
        self.body = body

    def __str__(self):
        return f"let {self.var} = {self.bound_expr} in {self.body}"

    def free_variables(self):
        bound_fv = self.bound_expr.free_variables()
        body_fv = self.body.free_variables()
        return bound_fv | (body_fv - self.var.free_variables())

    def bound_variables(self):
        return (
            self.var.free_variables()
            | self.bound_expr.bound_variables()
            | self.body.bound_variables()
        )

    def substitute(self, old: Variable, new: Variable) -> ASTNode:
        new_bound_expr = self.bound_expr.substitute(old, new)

        if self.var == old:
            new_body = self.body
        else:
            new_body = self.body.substitute(old, new)

        return LetExpression(self.var, new_bound_expr, new_body)

    def reduce(self, var: Variable, new_expr: ASTNode) -> ASTNode:
        reduced_bound = self.bound_expr.reduce(var, new_expr)
        return self.body.substitute(self.var, reduced_bound)


class String(Value):
    def __str__(self):
        return f'"{self.value}"'


class List(ASTNode):
    def __init__(self, elements):
        self.elements = elements

    def __str__(self):
        return f"[{', '.join(str(e) for e in self.elements)}]"

    def free_variables(self):
        fv = set()
        for e in self.elements:
            fv.update(e.free_variables())
        return fv

    def bound_variables(self):
        bv = set()
        for e in self.elements:
            bv.update(e.bound_variables())
        return bv

    def substitute(self, old: "Variable", new: "Variable") -> "ASTNode":
        return List([e.substitute(old, new) for e in self.elements])

    def reduce(self, var: "Variable", new_expr: "ASTNode") -> "ASTNode":
        return List([e.reduce(var, new_expr) for e in self.elements])


class Tuple(ASTNode):
    def __init__(self, elements):
        self.elements = elements

    def __str__(self):
        return f"({', '.join(str(e) for e in self.elements)})"

    def free_variables(self):
        fv = set()
        for e in self.elements:
            fv.update(e.free_variables())
        return fv

    def bound_variables(self):
        bv = set()
        for e in self.elements:
            bv.update(e.bound_variables())
        return bv

    def substitute(self, old: "Variable", new: "Variable") -> "ASTNode":
        return Tuple([e.substitute(old, new) for e in self.elements])

    def reduce(self, var: "Variable", new_expr: "ASTNode") -> "ASTNode":
        return Tuple([e.reduce(var, new_expr) for e in self.elements])


class RangeExpression(ASTNode):
    def __init__(self, start, end, step=None):
        self.start = start
        self.end = end
        self.step = step

    def __str__(self):
        if self.step:
            return f"[{self.start}, {self.step}..{self.end}]"
        return f"[{self.start}..{self.end}]"

    def free_variables(self):
        fv = self.start.free_variables().union(self.end.free_variables())
        if self.step:
            fv.update(self.step.free_variables())
        return fv

    def bound_variables(self):
        bv = self.start.bound_variables().union(self.end.bound_variables())
        if self.step:
            bv.update(self.step.bound_variables())
        return bv

    def substitute(self, old: "Variable", new: "Variable") -> "ASTNode":
        new_start = self.start.substitute(old, new)
        new_end = self.end.substitute(old, new)
        new_step = self.step.substitute(old, new) if self.step else None
        return RangeExpression(new_start, new_end, new_step)

    def reduce(self, var: "Variable", new_expr: "ASTNode") -> "ASTNode":
        reduced_start = self.start.reduce(var, new_expr)
        reduced_end = self.end.reduce(var, new_expr)
        reduced_step = self.step.reduce(var, new_expr) if self.step else None
        return RangeExpression(reduced_start, reduced_end, reduced_step)


class BuiltinFunction(Value):
    def __init__(self, id, name, func):
        self.id = id
        self.name = name
        self.func = func

    def __call__(self, *args):
        return self.func(*args)

    def __str__(self):
        return f"{self.name}<{self.id}>"


def do_reduce(redex: ASTNode, reduce) -> ASTNode:
    def is_reducible_element(node: ASTNode) -> bool:
        return isinstance(
            node,
            (
                Application,
                BinaryOperation,
                UnaryOperation,
                IfExpression,
                LetExpression,
            ),
        )

    if isinstance(redex, Application):
        if isinstance(redex.func, BuiltinFunction):
            return redex.func(*reduce(redex.arg).elements)

        return redex.func.body.reduce(redex.func.param, redex.arg)

    elif isinstance(redex, BinaryOperation):
        left_reduced = redex.left
        if isinstance(left_reduced, Application):
            left_reduced = reduce(left_reduced)

        right_reduced = redex.right
        if isinstance(right_reduced, Application):
            right_reduced = reduce(right_reduced)

        redex.left = left_reduced
        redex.right = right_reduced

        return redex.reduce(None, None)

    elif isinstance(redex, (UnaryOperation, IfExpression, LetExpression)):
        return redex.reduce(None, None)

    elif isinstance(redex, List):
        redex.elements = [
            reduce(e) if is_reducible_element(e) else e for e in redex.elements
        ]

        return redex

    elif isinstance(redex, Tuple):
        redex.elements = [
            do_reduce(e) if is_reducible_element(e) else e for e in redex.elements
        ]

        return redex

    elif isinstance(redex, RangeExpression):
        return redex

    return redex


def is_redex(node: ASTNode) -> bool:
    return (
        (
            isinstance(node, Application)
            and isinstance(node.func, (Abstraction, BuiltinFunction))
        )
        or isinstance(node, BinaryOperation)
        or isinstance(node, UnaryOperation)
        or isinstance(node, IfExpression)
        or isinstance(node, LetExpression)
    )


def nor_step(node):
    def find_redex(current, parent=None, key=None):
        if is_redex(current):
            return (current, parent, key)

        if isinstance(current, Application):
            result = find_redex(current.func, current, "func")
            if result[0] is not None:
                return result
            return find_redex(current.arg, current, "arg")

        elif isinstance(current, Abstraction):
            return find_redex(current.body, current, "body")

        elif isinstance(current, RangeExpression):
            result = find_redex(current.start, current, "start")
            if result[0] is not None:
                return result

            result = find_redex(current.end, current, "end")
            if result[0] is not None:
                return result

            result = find_redex(current.step, current, "step")
            if result[0] is not None:
                return result

        return (None, None, None)

    redex, parent, key = find_redex(node)

    if redex is None:
        if isinstance(node, (List, Tuple)):
            for i, elem in enumerate(node.elements):
                node.elements[i] = normal_order_reduction(elem)

        return node

    reduced = do_reduce(redex, normal_order_reduction)

    if parent is None:
        return reduced

    if isinstance(key, str):
        setattr(parent, key, reduced)
    elif isinstance(key, int):
        parent.elements[key] = reduced

    return node


def normal_order_reduction(node, max_steps=1000):
    current = node
    steps = 0

    while steps < max_steps:
        print(f"NOR step {steps}: {current}")
        next_node = nor_step(copy.deepcopy(current))

        if next_node == current:
            break

        current = next_node
        steps += 1

    return current


def aor_step(node):
    def is_redex(n):
        if isinstance(n, Application) and isinstance(n.func, Abstraction):
            return True

        if isinstance(n, Application) and isinstance(n.func, BuiltinFunction):
            return True

        if isinstance(
            n, (BinaryOperation, UnaryOperation, IfExpression, LetExpression)
        ):
            return all_reduced(n)

        return False

    def all_reduced(n):
        if isinstance(n, Application):
            return all_reduced(n.func) and all_reduced(n.arg)

        elif isinstance(n, Abstraction):
            return all_reduced(n.body)

        elif isinstance(n, BinaryOperation):
            return all_reduced(n.left) and all_reduced(n.right)

        elif isinstance(n, UnaryOperation):
            return all_reduced(n.value)

        elif isinstance(n, IfExpression):
            return (
                all_reduced(n.condition)
                and all_reduced(n.then_expr)
                and all_reduced(n.else_expr)
            )

        elif isinstance(n, LetExpression):
            return all_reduced(n.bound_expr) and all_reduced(n.body)

        elif isinstance(n, (List, Tuple)):
            return all(all_reduced(e) for e in n.elements)

        elif isinstance(n, RangeExpression):
            return all_reduced(n.start) and all_reduced(n.end) and all_reduced(n.step)

        return True

    def reduce(current, parent=None, is_left=False):
        if is_redex(current):
            return do_reduce(current, applicative_order_reduction)

        if isinstance(current, Application):
            new_func = reduce(current.func, current, True)
            if new_func is not current.func:
                return Application(new_func, current.arg)

            new_arg = reduce(current.arg, current, False)
            if new_arg is not current.arg:
                return Application(current.func, new_arg)

        elif isinstance(current, Abstraction):
            new_body = reduce(current.body, current, False)
            if new_body is not current.body:
                return Abstraction(current.param, new_body)

        elif isinstance(current, BinaryOperation):
            new_left = reduce(current.left, current, True)
            if new_left is not current.left:
                return BinaryOperation(new_left, current.op, current.right)

            new_right = reduce(current.right, current, False)
            if new_right is not current.right:
                return BinaryOperation(current.left, current.op, new_right)

        elif isinstance(current, UnaryOperation):
            new_expr = reduce(current.value, current, False)
            if new_expr is not current.value:
                return UnaryOperation(current.op, new_expr)

        elif isinstance(current, IfExpression):
            new_cond = reduce(current.condition, current, False)
            if new_cond is not current.condition:
                return IfExpression(new_cond, current.then_expr, current.else_expr)

        elif isinstance(current, LetExpression):
            new_value = reduce(current.bound_expr, current, False)
            if new_value is not current.bound_expr:
                return LetExpression(current.var, new_value, current.body)

        elif isinstance(current, List):
            new_elements = []
            changed = False
            for elem in current.elements:
                new_elem = reduce(elem)
                if new_elem is not elem:
                    changed = True
                new_elements.append(new_elem)
            if changed:
                return List(new_elements)

        elif isinstance(current, Tuple):
            new_elements = []
            changed = False
            for elem in current.elements:
                new_elem = reduce(elem)
                if new_elem is not elem:
                    changed = True
                new_elements.append(new_elem)
            if changed:
                return Tuple(new_elements)

        elif isinstance(current, RangeExpression):
            new_start = reduce(current.start)
            new_end = reduce(current.end)
            new_step = reduce(current.step)
            if (
                new_start is not current.start
                or new_end is not current.end
                or new_step is not current.step
            ):
                return RangeExpression(new_start, new_end, new_step)

        return current

    return reduce(node)


def applicative_order_reduction(node, max_steps=1000):
    current = node
    steps = 0

    while steps < max_steps:
        print(f"AOR step {steps}: {current}")
        next_node = aor_step(copy.deepcopy(current))

        if next_node == current:
            break

        current = next_node
        steps += 1

    return current
