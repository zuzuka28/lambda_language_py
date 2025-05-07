from evaluate import evaluate_lambda_expr


def run_tests(test_cases):
    passed = 0
    for test in test_cases:
        try:
            result = evaluate_lambda_expr(test["expression"])
            if str(result) == test["expected"]:
                print(f"✅ {test['name']} - PASSED")
                passed += 1
            else:
                print(f"❌ {test['name']} - FAILED")
                print(f"   Expression: {test['expression']}")
                print(f"   Expected:   {test['expected']}")
                print(f"   Got:        {result}")
        except Exception as e:
            print(f"💥 {test['name']} - CRASHED with exception: {str(e)}")
            print(f"   Expression: {test['expression']}")

    print(
        f"\nTotal: {len(test_cases)}, Passed: {passed}, Failed: {len(test_cases) - passed}"
    )


def main():
    test_cases = [
        {"name": "Identity function", "expression": r"((\x.x) a)", "expected": "a"},
        {
            "name": "K combinator application",
            "expression": r"(((\x.\y.x) a) b)",
            "expected": "a",
        },
        {
            "name": "Alpha conversion",
            "expression": r"((\x.(\y.(x y))) z)",
            "expected": r"(\y.(z y))",
        },
        {
            "name": "Nested beta reduction",
            "expression": r"((\x.(x (\y.y))) (\z.z))",
            "expected": r"(\y.y)",
        },
        # {
        #     "name": "Eta conversion",
        #     "expression": r"(\x.(\y.(x y)))",
        #     "expected": r"\x.x",
        # },
        {
            "name": "Church numeral 0",
            "expression": r"(((\f.\x.x) a) b)",
            "expected": "b",
        },
        {
            "name": "Church numeral 1",
            "expression": r"(((\f.\x.(f x)) a) b)",
            "expected": "(a b)",
        },
        {
            "name": "S combinator",
            "expression": r"((((\x.\y.\z.((x z) (y z))) a) b) c)",
            "expected": "((a c) (b c))",
        },
        {
            "name": "Variable capture",
            "expression": r"((\x.\y.(x y)) y)",
            "expected": r"(\y1.(y y1))",
        },
        {
            "name": "Y-combinator",
            "expression": r"((\f.(\x.(f (x x))) (\x.(f (x x)))) g)",
            "expected": r"(g ((\x.(g (x x))) (\x.(g (x x)))))",
        },
        {
            "name": "Normal order reduction",
            "expression": r"((\x.y) ((\x.(x x)) (\x.(x x))))",
            "expected": "y",
        },
        {
            "name": "Variable shadowing",
            "expression": r"(((\x.\x.x) a) b)",
            "expected": "b",
        },
        {
            "name": "Currying",
            "expression": r"((((\x.\y.\z.((x y) z)) a) b) c)",
            "expected": "((a b) c)",
        },
        {
            "name": "Free variables",
            "expression": r"(\x.y)",
            "expected": r"(\x.y)",
        },
        {
            "name": "K combinator with grouping",
            "expression": r"((\x.(\y.(x y))) (\a.a))",
            "expected": r"(\y.y)",
        },
    ]

    run_tests(test_cases)

    math_test_cases = [
        {
            "name": "floating",
            "expression": "2.5",
            "expected": "2.5",
        },
        {
            "name": "floating e",
            "expression": "2e2",
            "expected": "200.0",
        },
        {
            "name": "Simple addition",
            "expression": "2 + 3",
            "expected": "5.0",
        },
        {
            "name": "Simple subtraction",
            "expression": "5 - 2",
            "expected": "3.0",
        },
        {
            "name": "Simple multiplication",
            "expression": "3 * 4",
            "expected": "12.0",
        },
        {
            "name": "Simple division",
            "expression": "10 / 2",
            "expected": "5.0",
        },
        {
            "name": "Operator precedence (* before +)",
            "expression": "2 + 3 * 4",
            "expected": "14.0",
        },
        {
            "name": "Parentheses override precedence",
            "expression": "(2 + 3) * 4",
            "expected": "20.0",
        },
        {
            "name": "Chained operations (left-associative)",
            "expression": "10 - 4 - 2",
            "expected": "4.0",
        },
        {
            "name": "Mixed operations with precedence",
            "expression": "2 * 3 + 8 / 4 - 1",
            "expected": "7.0",
        },
        {
            "name": "Negative numbers",
            "expression": "3 + (-5)",
            "expected": "-2.0",
        },
        {
            "name": "Comparison (greater than)",
            "expression": "5 > 3",
            "expected": "true",
        },
        {
            "name": "Comparison (equality)",
            "expression": "2 * 3 == 6",
            "expected": "true",
        },
        {
            "name": "Boolean and arithmetic mix",
            "expression": "(5 > 3) && (2 + 2 == 4)",
            "expected": "true",
        },
        {
            "name": "Lambda application with infix ops",
            "expression": r"(\x. x + 1) 5",
            "expected": "6.0",
        },
        {
            "name": "Nested lambdas with infix ops",
            "expression": r"(\x. \y. x * y + 2) 3 4",
            "expected": "14.0",  # 3 * 4 + 2 = 14
        },
    ]

    run_tests(math_test_cases)

    if_test_cases = [
        {
            "name": "Simple if true",
            "expression": "if true then 1 else 2",
            "expected": "1.0",
        },
        {
            "name": "Simple if false",
            "expression": "if false then 1 else 2",
            "expected": "2.0",
        },
        {
            "name": "If with comparison",
            "expression": "if 2 > 1 then 100 else 200",
            "expected": "100.0",
        },
        {
            "name": "Nested if expressions",
            "expression": "if true then (if false then 1 else 2) else 3",
            "expected": "2.0",
        },
        {
            "name": "If with logical operators",
            "expression": "if (2 < 3) && (1 > 0) then 42 else 0",
            "expected": "42.0",
        },
        {
            "name": "If with arithmetic",
            "expression": "if (2 + 2 == 4) then (4 * 2) else (4 / 2)",
            "expected": "8.0",
        },
        {
            "name": "If in lambda",
            "expression": "(\\x. if x then 1 else 0) true",
            "expected": "1.0",
        },
        {
            "name": "If with let binding",
            "expression": "let x = 5 in (if (x > 3) then (x * 2) else x)",
            "expected": "10.0",
        },
        {
            "name": "If returns lambda",
            "expression": "(if true then (\\x. x + 1) else (\\x. x - 1)) 5",
            "expected": "6.0",
        },
        {
            "name": "Complex condition",
            "expression": "if (((2 < 3) || (4 > 5)) && (not false)) then 42 else 0",
            "expected": "42.0",
        },
        {
            "name": "If with function application",
            "expression": "if (\\x. x > 0)(-1) then 1 else -1",
            "expected": "-1.0",
        },
        {
            "name": "If all branches are lambdas",
            "expression": "(if false then (\\x. x * 2) else (\\y. y + 3)) 4",
            "expected": "7.0",
        },
        {
            "name": "If with boolean variable",
            "expression": "let b = (1 < 2) in if b then 10 else 20",
            "expected": "10.0",
        },
        {
            "name": "If with not operator",
            "expression": "if not (1 == 2) then 3 else 4",
            "expected": "3.0",
        },
        {
            "name": "If with division",
            "expression": "if 4 != 0 then 8 / 4 else 0",
            "expected": "2.0",
        },
        {
            "name": "If with 2 vars 1_1",
            "expression": r"(\v. \n. if (n == 0) then v else n) 1 2",
            "expected": "2.0",
        },
        {
            "name": "If with 2 vars 1_2",
            "expression": r"(\v. \n. if (n == 0) then v else n) 1 0",
            "expected": "1.0",
        },
        {
            "name": "If with 2 vars 1_2",
            "expression": r"(\v. \n. if (n == 0) then v else n) 0 2",
            "expected": "2.0",
        },
    ]

    run_tests(if_test_cases)

    let_test_cases = [
        {
            "name": "Simple let binding",
            "expression": "let x = 5 in x + 3",
            "expected": "8.0",
        },
        {
            "name": "Let with boolean value",
            "expression": "let flag = true in if flag then 1 else 0",
            "expected": "1.0",
        },
        {
            "name": "Nested let expressions",
            "expression": "let x = 2 in (let y = 3 in (x * y))",
            "expected": "6.0",
        },
        {
            "name": "Let shadowing",
            "expression": "let x = 1 in let x = 2 in x",
            "expected": "2.0",
        },
        {
            "name": "Let in lambda body",
            "expression": "(\\x. let y = (x + 1) in (y * 2)) 3",
            "expected": "8.0",
        },
        {
            "name": "Let with function application",
            "expression": "let double = (\\x. x * 2) in double 4",
            "expected": "8.0",
        },
        {
            "name": "Let with arithmetic expression",
            "expression": "let x = 10 / 2 in x + 3",
            "expected": "8.0",
        },
        {
            "name": "Let with comparison",
            "expression": "let x = 5 in let y = 3 in (x > y)",
            "expected": "true",
        },
        {
            "name": "Let in condition",
            "expression": "if let x = 5 in x > 3 then 1 else 0",
            "expected": "1.0",
        },
        {
            "name": "Let with complex expression",
            "expression": "let x = 2 + 3 * 4 in let y = x / 2 in y - 1",
            "expected": "6.0",
        },
        {
            "name": "Let scope isolation",
            "expression": "let x = 1 in ((let x = 2 in x) + x)",
            "expected": "3.0",
        },
        {
            "name": "Let with boolean operations",
            "expression": "let a = true in (let b = false in (a && b || a))",
            "expected": "true",
        },
        {
            "name": "Let binding lambda",
            "expression": "let f = (\\x. x * x) in f 4",
            "expected": "16.0",
        },
        {
            "name": "Let with multiple arithmetic ops",
            "expression": "let x = 5 in (let y = (x * 2) in (let z = (y - 3) in (z / 2)))",
            "expected": "3.5",
        },
        {
            "name": "Let in nested expressions",
            "expression": "let x = 10 in x * (let y = 3 in y + 2)",
            "expected": "50.0",
        },
    ]

    run_tests(let_test_cases)

    string_test_cases = [
        # Строки
        {"name": "String literal", "expression": '"Hello"', "expected": '"Hello"'},
        {
            "name": "String with escape",
            "expression": r'"He said \"Hi\""',
            "expected": r'"He said "Hi""',
        },
    ]

    run_tests(string_test_cases)

    list_test_cases = [
        {"name": "Empty list", "expression": "[]", "expected": "[]"},
        {
            "name": "Simple list",
            "expression": "[1, 2, 3]",
            "expected": "[1.0, 2.0, 3.0]",
        },
        {
            "name": "Nested lists",
            "expression": "[[1], [2, 3]]",
            "expected": "[[1.0], [2.0, 3.0]]",
        },
        {
            "name": "List with variables",
            "expression": "let x = 5 in [x, x+1]",
            "expected": "[5.0, 6.0]",
        },
    ]

    run_tests(list_test_cases)

    tuple_test_cases = [
        {"name": "Simple tuple", "expression": '(1, "a")', "expected": '(1.0, "a")'},
        {
            "name": "Nested tuples",
            "expression": '(1, ("a", 2))',
            "expected": '(1.0, ("a", 2.0))',
        },
    ]

    run_tests(tuple_test_cases)

    range_test_cases = [
        {"name": "Simple range", "expression": "[1..5]", "expected": "[1.0..5.0]"},
        {
            "name": "Range with step",
            "expression": "[1, 2..5]",
            "expected": "[1.0, 2.0..5.0]",
        },
        {
            "name": "Range with variables",
            "expression": "let x = 1 in [x..x+3]",
            "expected": "[1.0..4.0]",
        },
    ]

    run_tests(range_test_cases)

    list_tuple_range_mix_test_cases = [
        {
            "name": "List of tuples",
            "expression": '[(1, "a"), (2, "b")]',
            "expected": '[(1.0, "a"), (2.0, "b")]',
        },
        {
            "name": "Tuple with range",
            "expression": '([1..3], "test")',
            "expected": '([1.0..3.0], "test")',
        },
        {
            "name": "Complex structure",
            "expression": '[("start", [1..3]), ("end", [4..6])]',
            "expected": '[("start", [1.0..3.0]), ("end", [4.0..6.0])]',
        },
    ]

    run_tests(list_tuple_range_mix_test_cases)

    map_fold_filter_tests = [
        {
            "name": "Simple map (numbers)",
            "expression": r"map (\x. x + 1) [1, 2, 3]",
            "expected": "[2.0, 3.0, 4.0]",
        },
        {
            "name": "Map with range",
            "expression": r"map (\x. x * 2) [1..3]",
            "expected": "[2.0, 4.0, 6.0]",
        },
        {
            "name": "Filter even numbers",
            "expression": r"filter (\x. x % 2 == 0) [1..5]",
            "expected": "[2.0, 4.0]",
        },
        {
            "name": "Fold (sum)",
            "expression": r"fold (\acc.\x. acc + x) 0 [1..3]",
            "expected": "6.0",
        },
        {
            "name": "Complex structure",
            "expression": '[("start", [1..3]), ("end", [4..6])]',
            "expected": '[("start", [1.0..3.0]), ("end", [4.0..6.0])]',
        },
    ]

    run_tests(map_fold_filter_tests)

    real_cases = [
        {
            "name": "factorial",
            "expression": r"(let Y = (\f. (\x. f (x x)) (\x. f (x x))) in let fact = (Y (\c.\n. if (n == 0) then 1 else (n * c (n - 1)))) in (fact 3))",
            "expected": "6.0",
        },
    ]

    run_tests(real_cases)


if __name__ == "__main__":
    main()
