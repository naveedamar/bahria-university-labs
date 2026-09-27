import re

program = '''int x = 5; // initialize x
/* this is a
block comment */
string s = "a+b;c";
'''

def strip_comments(text):
    result = []
    i = 0
    n = len(text)
    in_string = False
    while i < n:
        ch = text[i]
        if in_string:
            result.append(ch)
            if ch == '"':
                in_string = False
            i += 1
            continue
        if ch == '"':
            in_string = True
            result.append(ch)
            i += 1
            continue
        if ch == '/' and i + 1 < n and text[i+1] == '/':
            while i < n and text[i] != '\n':
                i += 1
            continue
        if ch == '/' and i + 1 < n and text[i+1] == '*':
            i += 2
            while i + 1 < n and not (text[i] == '*' and text[i+1] == '/'):
                i += 1
            i += 2
            continue
        result.append(ch)
        i += 1
    return "".join(result)

cleaned = strip_comments(program)

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

keywords = {"int", "string", "if", "while", "return"}

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

tokens = []
for match in re.finditer(master_regex, cleaned):
    kind = match.lastgroup
    value = match.group()
    if kind in ("WS", "MISMATCH"):
        continue
    tokens.append((value, classify(kind, value)))

print("Cleaned program")
print(cleaned)

print("Tokens")
for value, ttype in tokens:
    print(f"<{value}, {ttype}>")

removed_chars = len(program) - len(cleaned)
print(f"\nCharacters removed by comment stripping: {removed_chars}")

string_intact = any(t == "STRING" and value == '"a+b;c"' for value, t in tokens)
print(f"String literal captured as single token (contents untokenized): {string_intact}")