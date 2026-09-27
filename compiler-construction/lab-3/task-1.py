def classify(ch):
    if ch.isalpha():
        return "letter"
    if ch.isdigit():
        return "digit"
    if ch == "_":
        return "underscore"
    return "other"

table = {
    "q0": {"letter": "q1", "digit": "qd", "underscore": "q2"},
    "q1": {"letter": "q1", "digit": "q1", "underscore": "q2"},
    "q2": {"letter": "q1", "digit": "q1", "underscore": "q2"},
    "qd": {"letter": "qd", "digit": "qd", "underscore": "qd", "other": "qd"},
}

accept = {"q1"}
start = "q0"

def run_dfa(table, start, accept, s):
    state = start
    for ch in s:
        cls = classify(ch)
        state = table.get(state, {}).get(cls, "qd")
    return state, state in accept

test_strings = ["count", "_total", "user_id", "value_", "x1_y2", "9abc"]

for s in test_strings:
    final_state, ok = run_dfa(table, start, accept, s)
    if ok:
        print(f"{s}: ACCEPTED")
    else:
        print(f"{s}: REJECTED")

print()
for s in test_strings:
    final_state, ok = run_dfa(table, start, accept, s)
    if not ok:
        if final_state == "q2":
            reason = "string ends with an underscore, which is not allowed"
        elif final_state == "qd":
            reason = "invalid start character (identifier cannot begin with a digit)"
        else:
            reason = "did not reach accepting state"
        print(f"{s}: halted in {final_state} - {reason}")