def power(base: float, exp: int) -> float:
    result = 1.0

    if exp >= 0:
        for _ in range(exp):
            result *= base
    else:                       
        for _ in range(-exp):
            result *= base
        result = 1.0 / result

    return result


def main() -> None:

    try:
        num = float(input("Enter number: "))
    except ValueError:
        print("Invalid number input.")
        return

    try:
        exp = int(input("Enter exponent: "))
    except ValueError:
        print("Invalid exponent input.")
        return

    result = power(num, exp)
    # Ensure integers print without a trailing .0
    print(f"Result: {int(result) if result.is_integer() else result}")


if __name__ == "__main__":
    main()