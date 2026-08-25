from fizzbuzz import fizzbuzz


def test_length():
    assert len(fizzbuzz(15)) == 15


def test_plain_numbers():
    r = fizzbuzz(10)
    assert r[0] == "1" and r[1] == "2" and r[3] == "4"


def test_fizz():
    r = fizzbuzz(6)
    assert r[2] == "Fizz" and r[5] == "Fizz"


def test_buzz():
    r = fizzbuzz(5)
    assert r[4] == "Buzz"


def test_fizzbuzz_15():
    assert fizzbuzz(15)[14] == "FizzBuzz"


def test_fizzbuzz_30():
    assert fizzbuzz(30)[29] == "FizzBuzz"


def test_zero():
    assert fizzbuzz(0) == []


def test_no_integers_at_multiples():
    r = fizzbuzz(15)
    for idx in [2, 4, 5, 8, 11, 14]:
        assert r[idx] != str(idx + 1)
