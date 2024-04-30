def prime_factors(n):
    factors = []
    # Check for number of 2s that divide n
    while n % 2 == 0:
        factors.append(2)
        n = n // 2

    # n must be odd at this point, thus skip even numbers
    for i in range(3, int(n**0.5) + 1, 2):
        # While i divides n, add i and divide n
        while n % i == 0:
            factors.append(i)
            n = n // i

    # This condition is to check if n is a prime number greater than 2
    if n > 2:
        factors.append(n)

    return factors

def main():
    try:
        number = int(input("Enter a number to find its prime factors: "))
        if number <= 1:
            print("Please enter a number greater than 1.")
        else:
            factors = prime_factors(number)
            if factors:
                print("Prime factors of", number, "are:", factors)
            else:
                print("No prime factors, the number is prime itself.")
    except ValueError:
        print("Please enter a valid integer.")

if __name__ == "__main__":
    main()
