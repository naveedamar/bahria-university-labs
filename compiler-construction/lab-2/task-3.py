import re

program = """int a = 5;
int b = 10;
c = a @ b $ 2;
return c;"""

token_spec = [
    ("STRING", r'"[^"]*"'),
    ("OP2", r'==|!=|<=|>=|&&|\|\|'),
    ("OP1", r'[+\-*/=<>!]'),
    ("DELIM", r'[;(){}]'),
    ("NUMBER", r'\d+'),
    ("ID", r'[A-Za-z_]\w*'),
    ("WS", r'\s+'),
    ("MISMATCH", r'.'),
]
master_regex = "|".join(f"(?P<{name}>{pattern})" for name, pattern in token_spec)

keywords = {"int", "return"}

def classify(kind, value):
    if kind == "ID" and value in keywords:
        return "KEYWORD"
    if kind == "ID":
        return "IDENTIFIER"
    if kind == "NUMBER":
        return "NUMBER"
    if kind == "STRING":
        return "STRING"
    if kind in ("OP1", "OP2"):
        return "OPERATOR"
    if kind == "DELIM":
        return "DELIMITER"
    return kind

valid_count = 0
error_count = 0

for line_num, line in enumerate(program.split("\n"), start=1):
    for match in re.finditer(master_regex, line):
        kind = match.lastgroup
        value = match.group()
        column = match.start() + 1
        if kind == "WS":
            continue
        if kind == "MISMATCH":
            print(f"Lexical Error: illegal character '{value}' at line {line_num}, column {column}")
            error_count += 1
            continue
        ttype = classify(kind, value)
        print(f"<{value}, {ttype}> at line {line_num}, column {column}")
        valid_count += 1

print(f"\nTotal valid tokens: {valid_count}")
print(f"Total lexical errors: {error_count}")