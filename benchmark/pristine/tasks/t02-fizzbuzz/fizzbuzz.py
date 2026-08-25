def fizzbuzz(n: int) -> list[str]:
    """Classic FizzBuzz from 1 to n inclusive.

    Multiples of 3 -> "Fizz", of 5 -> "Buzz", of both -> "FizzBuzz".
    """
    out = []
    for i in range(1, n + 1):
        if i % 3 == 0:
            out.append("Fizz")
        elif i % 5 == 0:
            out.append("Buzz")
        elif i % 15 == 0:
            out.append("FizzBuzz")
        else:
            out.append(str(i))
    return out
