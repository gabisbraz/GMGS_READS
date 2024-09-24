def is_prime(num):
    if num <= 1:
        return False
    for i in range(2, int(num ** 0.5) + 1):
        if num % i == 0:
            return False
    return True

def test_prime_numbers():
    test_cases = [1, 2, 3, 4, 17, 20, 29, 35]
    for num in test_cases:
        result = is_prime(num)
        print(f"O número {num} é primo? {result}")

if __name__ == "__main__":
    test_prime_numbers()
