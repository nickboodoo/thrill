def prime_factors(n):
    factors = []
    # Check for number of 2s that divide n
    while n % 2 == 0:
        factors.append(2)
        n //= 2

    # n must be odd at this point, so we can skip even numbers
    for i in range(3, int(n**0.5) + 1, 2):
        while n % i == 0:
            factors.append(i)
            n //= i

    # This condition is to check if n is a prime number greater than 2
    if n > 2:
        factors.append(n)

    return factors

def is_perfect_number(n):
    sum_divisors = 1
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            sum_divisors += i
            if i != n // i:
                sum_divisors += n // i
    return sum_divisors == n

def main():
    while True:
        try:
            number = int(input("Enter a number to find its prime factors and check if it's a perfect number (or type 'exit' to quit): "))
            if number <= 1:
                print("Please enter a number greater than 1.")
            else:
                factors = prime_factors(number)
                if factors:
                    print("Prime factors of", number, "are:", factors)
                else:
                    print("No prime factors, the number is prime itself.")

                if is_perfect_number(number):
                    print(number, "is a perfect number.")
                else:
                    print(number, "is not a perfect number.")
        except ValueError as e:
            if str(e) == "invalid literal for int() with base 10: 'exit'":
                print("Exiting the program. Goodbye!")
                break
            else:
                print("Please enter a valid integer or 'exit'.")

if __name__ == "__main__":
    main()
