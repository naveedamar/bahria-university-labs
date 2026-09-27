def classify_id(ch):
    if ch.isalpha():
        return "letter"
    if ch.isdigit():
        return "digit"
    if ch == "_":
        return "underscore"
    return "other"

id_table = {
    "q0": {"letter": "q1", "underscore": "q2"},
    "q1": {"letter": "q1", "digit": "q1", "underscore": "q2"},
    "q2": {"letter": "q1", "digit": "q1", "underscore": "q2"},
}
id_accept = {"q1"}

def classify_num(ch):
    if ch.isdigit():
        return "digit"
    if ch == ".":
        return "dot"
    if ch in "eE":
        return "e"
    if ch in "+-":
        return "sign"
    return "other"

num_table = {
    "q0": {"digit": "q1"},
    "q1": {"digit": "q1", "dot": "q2", "e": "q4"},
    "q2": {"digit": "q3"},
    "q3": {"digit": "q3", "e": "q4"},
    "q4": {"digit": "q6", "sign": "q5"},
    "q5": {"digit": "q6"},
    "q6": {"digit": "q6"},
}
num_accept = {"q1": "INTEGER", "q3": "REAL", "q6": "SCIENTIFIC"}

def longest_match(table, classify, s, pos, accept_states):
    state = "q0"
    best_len = 0
    i = pos
    while i < len(s):
        cls = classify(s[i])
        nxt = table.get(state, {}).get(cls)
        if nxt is None:
            break
        state = nxt
        i += 1
        if state in accept_states:
            best_len = i - pos
    return best_len

keywords = {"if", "then", "else", "while"}

def recognize_lexeme(s, pos):
    ch = s[pos]
    if ch.isalpha() or ch == "_":
        length = longest_match(id_table, classify_id, s, pos, id_accept)
        if length == 0:
            return None
        lexeme = s[pos:pos + length]
        ttype = "KEYWORD" if lexeme in keywords else "IDENTIFIER"
        return lexeme, ttype, length
    if ch.isdigit():
        length = longest_match(num_table, classify_num, s, pos, set(num_accept.keys()))
        if length == 0:
            return None
        lexeme = s[pos:pos + length]
        state = "q0"
        for c in lexeme:
            state = num_table[state][classify_num(c)]
        ttype = num_accept[state]
        return lexeme, ttype, length
    return None

multi_ops = ["==", "!=", "<=", ">=", "&&", "||"]
single_ops = set("+-*/=<>!")
delimiters = set(";(){}")

def scan(text):
    tokens = []
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        if ch.isspace():
            i += 1
            continue
        matched = False
        for op in multi_ops:
            if text[i:i+len(op)] == op:
                tokens.append((op, "OPERATOR"))
                i += len(op)
                matched = True
                break
        if matched:
            continue
        if ch.isalpha() or ch == "_" or ch.isdigit():
            result = recognize_lexeme(text, i)
            if result:
                lexeme, ttype, length = result
                tokens.append((lexeme, ttype))
                i += length
                continue
        if ch in single_ops:
            tokens.append((ch, "OPERATOR"))
            i += 1
            continue
        if ch in delimiters:
            tokens.append((ch, "DELIMITER"))
            i += 1
            continue
        i += 1
    return tokens

line = "if count1 >= 3.5 then total = total2"
tokens = scan(line)

print("Token Stream")
for lexeme, ttype in tokens:
    print(f"<{lexeme}, {ttype}>")