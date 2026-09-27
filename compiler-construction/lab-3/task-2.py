def classify(ch):
    if ch.isdigit():
        return "digit"
    if ch == ".":
        return "dot"
    if ch in "eE":
        return "e"
    if ch in "+-":
        return "sign"
    return "other"

table = {
    "q0": {"digit": "q1"},
    "q1": {"digit": "q1", "dot": "q2", "e": "q4"},
    "q2": {"digit": "q3"},
    "q3": {"digit": "q3", "e": "q4"},
    "q4": {"digit": "q6", "sign": "q5"},
    "q5": {"digit": "q6"},
    "q6": {"digit": "q6"},
}

accepting = {"q1": "INTEGER", "q3": "REAL", "q6": "SCIENTIFIC"}
intermediate = {"q0", "q2", "q4", "q5"}
start = "q0"

def run_dfa(table, start, s):
    state = start
    for ch in s:
        cls = classify(ch)
        nxt = table.get(state, {}).get(cls)
        if nxt is None:
            return "dead"
        state = nxt
    return state

print("Accepting states: q1 (INTEGER), q3 (REAL), q6 (SCIENTIFIC)")
print(f"Intermediate (non-accepting) states: {sorted(intermediate)}")
print()

test_strings = ["42", "3.14", "2.5e10", "6e-3", "10.", ".5", "3.4.5", "2e."]

print(f"{'Input':<10}{'Result':<10}{'Token Type':<12}")
for s in test_strings:
    final_state = run_dfa(table, start, s)
    if final_state in accepting:
        print(f"{s:<10}{'ACCEPTED':<10}{accepting[final_state]:<12}")
    else:
        print(f"{s:<10}{'REJECTED':<10}{'-':<12}")