import re

token_spec_correct = [
    ("STRING", r'"[^"]*"'),
    ("OP2", r'==|!=|<=|>=|&&|\|\|'),
    ("OP1", r'[+\-*/=<>!]'),
    ("DELIM", r'[;(){}]'),
    ("NUMBER", r'\d+'),
    ("ID", r'[A-Za-z_]\w*'),
    ("WS", r'\s+'),
    ("MISMATCH", r'.'),
]

master_regex = "|".join(f"(?P<{name}>{pattern})" for name, pattern in token_spec_correct)

keywords = {"if", "while", "for", "int", "float", "return"}

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

def scan(line, regex):
    tokens = []
    for match in re.finditer(regex, line):
        kind = match.lastgroup
        value = match.group()
        if kind == "WS":
            continue
        if kind == "MISMATCH":
            continue
        tokens.append((value, classify(kind, value)))
    return tokens

line = "if (count >= 10 && flag != 0) total = total + 1;"

tokens_correct = scan(line, master_regex)
print("Tokens (correct regex)")
for value, ttype in tokens_correct:
    print(f"<{value}, {ttype}>")

operator_count_correct = sum(1 for _, t in tokens_correct if t == "OPERATOR")
print(f"\nOPERATOR token count (correct regex): {operator_count_correct}")

token_spec_wrong = [
    ("STRING", r'"[^"]*"'),
    ("OP1", r'[+\-*/=<>!]'),
    ("OP2", r'==|!=|<=|>=|&&|\|\|'),
    ("DELIM", r'[;(){}]'),
    ("NUMBER", r'\d+'),
    ("ID", r'[A-Za-z_]\w*'),
    ("WS", r'\s+'),
    ("MISMATCH", r'.'),
]

master_regex_wrong = "|".join(f"(?P<{name}>{pattern})" for name, pattern in token_spec_wrong)

tokens_wrong = scan(line, master_regex_wrong)
operator_count_wrong = sum(1 for _, t in tokens_wrong if t == "OPERATOR")
print(f"OPERATOR token count (wrong regex, single-char listed first): {operator_count_wrong}")