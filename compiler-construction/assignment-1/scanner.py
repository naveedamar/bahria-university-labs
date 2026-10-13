"""
Function to evaluate and accept only string containing a's and b's with exactly 3 bs
"""
def scanner(input_string):
    state = 0
    for c in input_string:
        if state == 0:
            if c == 'a':
                state = 0
            elif c == 'b':
                state = 1
            else:
                return 0
        elif state == 1:
            if c == 'a':
                state = 1
            elif c == 'b':
                state = 2
            else:
                return 0
        elif state == 2:
            if c == 'a':
                state = 2
            elif c == 'b':
                state = 3
            else:
                return 0
        elif state == 3:
            if c == 'a':
                state = 3
            elif c == 'b':
                return 0

    return 1 if state == 3 else 0


def main():
    input_string = input(">> Enter input string: ")

    if scanner(input_string) == 1:
        print("Output: valid string")
    else:
        print("Output: invalid string")


main()