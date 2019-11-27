def sum_numbers(numbers=None):
    try:
        return sum(numbers)
    except TypeError:
        return sum([n for n in range(101)])