grammar = {
    "S": [
        ["if", "E", "then", "S", "else", "S"],
        ["if", "E", "then", "S"],
        ["while", "E", "do", "S"],
        ["id", "=", "E"],
    ]
}

def format_grammar(g):
    lines = []
    for nt, prods in g.items():
        rhs = " | ".join(" ".join(prod) for prod in prods)
        lines.append(f"{nt} -> {rhs}")
    return "\n".join(lines)

def find_common_prefix(prods):
    if len(prods) < 2:
        return []
    prefix = []
    min_len = min(len(p) for p in prods)
    for i in range(min_len):
        symbols_at_i = set(p[i] for p in prods)
        if len(symbols_at_i) == 1:
            prefix.append(prods[0][i])
        else:
            break
    return prefix

def left_factor(nt, prods):
    groups = {}
    for p in prods:
        key = p[0]
        groups.setdefault(key, []).append(p)

    new_prods = []
    new_rules = {}
    counter = 1

    for key, group in groups.items():
        if len(group) > 1:
            prefix = find_common_prefix(group)
            suffixes = [p[len(prefix):] for p in group]
            suffixes = [s if s else ["ε"] for s in suffixes]
            new_nt = nt + "'" * counter
            new_prods.append(prefix + [new_nt])
            new_rules[new_nt] = suffixes
            counter += 1
        else:
            new_prods.append(group[0])

    result = {nt: new_prods}
    result.update(new_rules)
    return result

print("Grammar before factoring:")
print(format_grammar(grammar))

if_group = [p for p in grammar["S"] if p[0] == "if"]
common = find_common_prefix(if_group)
print(f"\nCommon prefix found among 'if' productions: {' '.join(common)}")

new_grammar = left_factor("S", grammar["S"])

print("\nGrammar after factoring:")
print(format_grammar(new_grammar))

print("\nLookahead analysis")
before_needed = len(common) + 1
print(f"Before: 'if E then S else S' and 'if E then S' share a {len(common)}-symbol prefix,")
print(f"so distinguishing them needs {before_needed} symbols of context (far more than 1 token).")
print("After: S's productions now start with 'if', 'while', 'id' - all distinct, so 1 token of lookahead suffices.")
print("S' productions start with 'else' vs epsilon, also distinguishable with 1 token of lookahead.")