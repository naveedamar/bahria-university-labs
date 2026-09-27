import re

def tokenize(s):
    return re.findall(r'\d+|[A-Za-z_]\w*|[()+\-*/]', s)

class DepthLimitExceeded(Exception):
    def __init__(self, depth):
        self.depth = depth

def parse_E_broken(tokens, pos, counter, limit):
    counter[0] += 1
    if counter[0] > limit:
        raise DepthLimitExceeded(counter[0])
    left = parse_E_broken(tokens, pos, counter, limit)
    return left

tokens = tokenize("x")
counter = [0]
limit = 20

try:
    parse_E_broken(tokens, 0, counter, limit)
except DepthLimitExceeded as e:
    broken_depth = e.depth
    print(f"parse_E_broken called itself {broken_depth} times before hitting the depth limit of {limit}")

def parse_T(tokens, pos, counter):
    counter[0] += 1
    value = tokens[pos[0]]
    pos[0] += 1
    return value

def parse_Eprime(tokens, pos, counter):
    counter[0] += 1
    if pos[0] < len(tokens) and tokens[pos[0]] == '+':
        pos[0] += 1
        parse_T(tokens, pos, counter)
        parse_Eprime(tokens, pos, counter)

def parse_E_corrected(tokens, pos, counter):
    counter[0] += 1
    parse_T(tokens, pos, counter)
    parse_Eprime(tokens, pos, counter)

pos = [0]
counter2 = [0]
parse_E_corrected(tokens, pos, counter2)
corrected_depth = counter2[0]
print(f"parse_E_corrected finished successfully after {corrected_depth} calls total")

print(f"\nComparison")
print(f"Broken  (E -> E + T): reached {broken_depth} recursive calls, never consumed a token, hit the depth limit")
print(f"Corrected (E -> T E'): completed in {corrected_depth} calls, successfully parsed the input")