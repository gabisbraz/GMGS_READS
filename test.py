def func(x):
    return x + 1


def test_answer():
    print("TESTE")
    assert func(3) == 6, "PASSOU"
