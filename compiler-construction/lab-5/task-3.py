grammar = {
    "A": [["B", "a"], ["c"]],
    "B": [["A", "b"], ["d"]],
}

def format_grammar(g, order=None):
    lines = []
    keys = order if order else g.keys()
    for nt in keys:
        rhs = " | ".join(" ".join(prod) for prod in g[nt])
        lines.append(f"{nt} -> {rhs}")
    return "\n".join(lines)

def is_directly_left_recursive(nt, prods):
    return any(p[0] == nt for p in prods)

print("Grammar:")
print(format_grammar(grammar, ["A", "B"]))

print("\nDirect left recursion check:")
for nt, prods in grammar.items():
    print(f"{nt}: {'DIRECTLY left-recursive' if is_directly_left_recursive(nt, prods) else 'not directly left-recursive'}")

def compute_begins_with(grammar):
    begins_with = {nt: set() for nt in grammar}
    for nt, prods in grammar.items():
        for p in prods:
            if p[0] in grammar:
                begins_with[nt].add(p[0])

    changed = True
    while changed:
        changed = False
        for nt in grammar:
            for other in list(begins_with[nt]):
                for extra in begins_with[other]:
                    if extra not in begins_with[nt]:
                        begins_with[nt].add(extra)
                        changed = True
    return begins_with

begins_with = compute_begins_with(grammar)
print("\nBegins-with relation:")
for nt, s in begins_with.items():
    print(f"beginsWith({nt}) = {s}")

print("\nCycle detection:")
cycle_found = []
for nt, s in begins_with.items():
    if nt in s:
        cycle_found.append(nt)
        print(f"{nt} begins-with itself -> indirect left recursion detected")

print("\nDerivation cycle causing infinite loop:")
print("A => B a            (A -> B a)")
print("  => A b a          (substitute B -> A b)")
print("  => B a b a        (substitute A -> B a, leftmost symbol is A again)")
print("  => ...            (repeats forever, never consuming a terminal first)")

def substitute(prods, target, replacement_prods):
    new_prods = []
    for p in prods:
        if p[0] == target:
            for r in replacement_prods:
                new_prods.append(r + p[1:])
        else:
            new_prods.append(p)
    return new_prods

a_substituted = substitute(grammar["A"], "B", grammar["B"])
print(f"\nAfter substituting B into A: A -> {' | '.join(' '.join(p) for p in a_substituted)}")

def eliminate(nt, prods):
    alpha = [prod[1:] for prod in prods if prod[0] == nt]
    beta = [prod for prod in prods if prod[0] != nt]
    new_nt = nt + "'"
    new_main = [b + [new_nt] for b in beta] if beta else [[new_nt]]
    new_primed = [a + [new_nt] for a in alpha] + [["ε"]]
    return {nt: new_main, new_nt: new_primed}

final_grammar = {}
final_grammar.update(eliminate("A", a_substituted))
final_grammar["B"] = grammar["B"]

print("\nFinal grammar:")
print(format_grammar(final_grammar, ["A", "A'", "B"]))

final_begins_with = compute_begins_with(final_grammar)
print("\nFinal begins-with relation:")
for nt, s in final_begins_with.items():
    print(f"beginsWith({nt}) = {s}")

no_cycle = all(nt not in s for nt, s in final_begins_with.items())
print(f"\nNo non-terminal begins-with itself: {no_cycle}")