grammar = {
    "E": [["E", "+", "T"], ["E", "-", "T"], ["T"]],
    "T": [["T", "*", "F"], ["F"]],
    "F": [["(", "E", ")"], ["id"]],
}

def format_grammar(g):
    lines = []
    for nt, prods in g.items():
        rhs = " | ".join(" ".join(prod) for prod in prods)
        lines.append(f"{nt} -> {rhs}")
    return "\n".join(lines)

def has_left_recursion(nt, prods):
    recursive = [prod for prod in prods if prod[0] == nt]
    return len(recursive) > 0, recursive

def eliminate(nt, prods):
    alpha = [prod[1:] for prod in prods if prod[0] == nt]
    beta = [prod for prod in prods if prod[0] != nt]
    new_nt = nt + "'"

    if not alpha:
        return {nt: prods}

    new_main = [b + [new_nt] for b in beta] if beta else [[new_nt]]
    new_primed = [a + [new_nt] for a in alpha] + [["ε"]]

    return {nt: new_main, new_nt: new_primed}

print("Grammar before:")
print(format_grammar(grammar))

print("\nLeft recursion check:")
for nt, prods in grammar.items():
    is_recursive, recursive_prods = has_left_recursion(nt, prods)
    if is_recursive:
        rules = ", ".join(" ".join(p) for p in recursive_prods)
        print(f"{nt}: LEFT-RECURSIVE ({rules})")
    else:
        print(f"{nt}: not left-recursive")

new_grammar = {}
for nt, prods in grammar.items():
    is_recursive, _ = has_left_recursion(nt, prods)
    if is_recursive:
        new_grammar.update(eliminate(nt, prods))
    else:
        new_grammar[nt] = prods

print("\nGrammar after:")
print(format_grammar(new_grammar))

print("\nLeft recursion check after elimination:")
all_clear = True
for nt, prods in new_grammar.items():
    is_recursive, _ = has_left_recursion(nt, prods)
    status = "LEFT-RECURSIVE" if is_recursive else "clear"
    if is_recursive:
        all_clear = False
    print(f"{nt}: {status}")

print(f"\nNo non-terminal is left-recursive: {all_clear}")