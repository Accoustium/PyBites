def freq_digit(num: int) -> int:
    num_string = str(num)
    highest = ' '
    for val in num_string:
        if num_string.count(val) > num_string.count(highest):
            highest = val

    return int(highest) if highest != '' else int(num_string[0])
