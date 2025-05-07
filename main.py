from evaluate import evaluate_lambda_expr


def main():
    print("Lambda Calculus REPL")
    print("Enter 'exit' to quit\n")

    while True:
        try:
            text = input("λ> ").strip()
            if text.lower() in ("exit", "quit"):
                break

            print(f"NOR: {evaluate_lambda_expr(text, strategy='nor')}")
            print(f"AOR: {evaluate_lambda_expr(text, strategy='aor')}")

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    main()
