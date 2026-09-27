import re

def tokenize(expr):
    return re.findall(r'\d+|[A-Za-z_]\w*|[=+\-*/]', expr)

def generate_tac(statement):
    tokens = tokenize(statement)
    target = tokens[0]
    rhs = tokens[2:]
    pos = [0]
    tac = []
    temp_count = [0]

    def new_temp():
        temp_count[0] += 1
        return f"t{temp_count[0]}"

    def peek():
        return rhs[pos[0]] if pos[0] < len(rhs) else None

    def advance():
        tok = rhs[pos[0]]
        pos[0] += 1
        return tok

    def parse_factor():
        return advance()

    def parse_term():
        left = parse_factor()
        while peek() in ('*', '/'):
            op = advance()
            right = parse_factor()
            result = new_temp()
            tac.append((op, left, right, result))
            left = result
        return left

    def parse_expr():
        left = parse_term()
        while peek() in ('+', '-'):
            op = advance()
            right = parse_term()
            result = new_temp()
            tac.append((op, left, right, result))
            left = result
        return left

    final = parse_expr()
    tac.append(('=', final, None, target))
    return tac

def is_numeric(x):
    return x is not None and x.lstrip('-').isdigit()

def constant_fold(tac):
    folded = []
    for op, a1, a2, res in tac:
        if op in ('+', '-', '*', '/') and is_numeric(a1) and is_numeric(a2):
            a1n, a2n = int(a1), int(a2)
            if op == '+':
                val = a1n + a2n
            elif op == '-':
                val = a1n - a2n
            elif op == '*':
                val = a1n * a2n
            else:
                val = a1n // a2n
            folded.append(('=', str(val), None, res))
        else:
            folded.append((op, a1, a2, res))
    return folded

def generate_target_code(tac):
    asm = []
    op_map = {'+': 'ADD', '-': 'SUB', '*': 'MUL', '/': 'DIV'}
    for op, a1, a2, res in tac:
        if op == '=':
            asm.append(f"LOAD {a1}")
            asm.append(f"STORE {res}")
        else:
            asm.append(f"LOAD {a1}")
            asm.append(f"{op_map[op]} {a2}")
            asm.append(f"STORE {res}")
    return asm

statement = "z = 3 * 4 + x"

tac_before = generate_tac(statement)
print("Three-Address Code (unoptimized)")
for instr in tac_before:
    op, a1, a2, res = instr
    if op == '=':
        print(f"{res} = {a1}")
    else:
        print(f"{res} = {a1} {op} {a2}")

tac_after = constant_fold(tac_before)
print("\nThree-Address Code (after constant folding)")
for instr in tac_after:
    op, a1, a2, res = instr
    if op == '=':
        print(f"{res} = {a1}")
    else:
        print(f"{res} = {a1} {op} {a2}")

asm_before = generate_target_code(tac_before)
asm_after = generate_target_code(tac_after)

print("\nTarget Code (before optimization)")
for line in asm_before:
    print(line)

print("\nTarget Code (after optimization)")
for line in asm_after:
    print(line)

count_before = len(asm_before)
count_after = len(asm_after)
reduction = (count_before - count_after) / count_before * 100

print(f"\nInstruction count before: {count_before}")
print(f"Instruction count after: {count_after}")
print(f"Reduction: {reduction:.2f}%")