import re

program = """int x = 5;
int y = 10;
float z = 3.14;
x = x + y;
y = x * 2;
result = x + y;"""

token_spec = [
    ("OP2", r'==|!=|<=|>=|&&|\|\|'),
    ("OP1", r'[+\-*/=<>!]'),
    ("DELIM", r'[;(){}]'),
    ("NUMBER", r'\d+\.\d+|\d+'),
    ("ID", r'[A-Za-z_]\w*'),
    ("WS", r'\s+'),
    ("MISMATCH", r'.'),
]
master_regex = "|".join(f"(?P<{name}>{pattern})" for name, pattern in token_spec)

type_keywords = {"int", "float"}

symbol_table = {}
undeclared_uses = set()

lines = program.split("\n")
for line_num, line in enumerate(lines, start=1):
    tokens = []
    for match in re.finditer(master_regex, line):
        kind = match.lastgroup
        value = match.group()
        if kind in ("WS", "MISMATCH"):
            continue
        tokens.append(value)

    i = 0
    while i < len(tokens):
        tok = tokens[i]
        if tok in type_keywords:
            var_name = tokens[i + 1]
            symbol_table[var_name] = {"type": tok, "line": line_num, "uses": 0}
            i += 2
            continue
        if re.fullmatch(r'[A-Za-z_]\w*', tok):
            if tok in symbol_table:
                symbol_table[tok]["uses"] += 1
            else:
                undeclared_uses.add(tok)
        i += 1

for name in symbol_table:
    if symbol_table[name]["uses"] > 0:
        symbol_table[name]["uses"] -= 1

declared_but_unused = [name for name, info in symbol_table.items() if info["uses"] == 0]

print("Used but never declared:")
for name in sorted(undeclared_uses):
    print(f"  {name}")

print("\nDeclared but never used:")
for name in declared_but_unused:
    print(f"  {name}")

print("\nSymbol Table")
print(f"{'Identifier':<12}{'Type':<8}{'Declared Line':<15}{'Uses':<6}")
for name in sorted(symbol_table.keys()):
    info = symbol_table[name]
    print(f"{name:<12}{info['type']:<8}{info['line']:<15}{info['uses']:<6}")