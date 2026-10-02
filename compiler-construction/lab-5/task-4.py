grammar_original = {
    "E": [["E", "+", "T"], ["T"]],
    "T": [["id"]],
}

grammar_transformed = {
    "E": [["T", "E'"]],
    "E'": [["+", "T", "E'"], []],
    "T": [["id"]],
}

def compute_min_lengths(grammar):
    nonterminals = set(grammar.keys())
    min_len = {nt: float('inf') for nt in nonterminals}
    changed = True
    while changed:
        changed = False
        for nt, prods in grammar.items():
            for prod in prods:
                total = 0
                feasible = True
                for sym in prod:
                    if sym in nonterminals:
                        if min_len[sym] == float('inf'):
                            feasible = False
                            break
                        total += min_len[sym]
                    else:
                        total += 1
                if feasible and total < min_len[nt]:
                    min_len[nt] = total
                    changed = True
    return min_len

def generate_strings(grammar, start, max_length):
    nonterminals = set(grammar.keys())
    min_len = compute_min_lengths(grammar)
    results = set()
    visited = set()

    def lower_bound(form):
        total = 0
        for sym in form:
            total += min_len[sym] if sym in nonterminals else 1
        return total

    def expand(form):
        if form in visited:
            return
        visited.add(form)
        if lower_bound(form) > max_length:
            return
        idx = next((i for i, s in enumerate(form) if s in nonterminals), None)
        if idx is None:
            if len(form) <= max_length:
                results.add(form)
            return
        nt = form[idx]
        for prod in grammar[nt]:
            new_form = form[:idx] + tuple(prod) + form[idx + 1:]
            expand(new_form)

    expand((start,))
    return results

max_length = 5

set_original = generate_strings(grammar_original, "E", max_length)
set_transformed = generate_strings(grammar_transformed, "E", max_length)

def fmt(s):
    return " ".join(s) if s else "ε"

sorted_original = sorted(set_original, key=lambda s: (len(s), s))
sorted_transformed = sorted(set_transformed, key=lambda s: (len(s), s))

print(f"{'Original grammar':<30}{'Transformed grammar':<30}")
max_rows = max(len(sorted_original), len(sorted_transformed))
for i in range(max_rows):
    left = fmt(sorted_original[i]) if i < len(sorted_original) else ""
    right = fmt(sorted_transformed[i]) if i < len(sorted_transformed) else ""
    print(f"{left:<30}{right:<30}")

print(f"\nSets equal: {set_original == set_transformed}")

only_in_original = set_original - set_transformed
only_in_transformed = set_transformed - set_original

print(f"Derivable only by original: {[fmt(s) for s in only_in_original] if only_in_original else 'none'}")
print(f"Derivable only by transformed: {[fmt(s) for s in only_in_transformed] if only_in_transformed else 'none'}")