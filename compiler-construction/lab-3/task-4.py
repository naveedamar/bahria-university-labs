def step(state, ch):
    if state == "q0":
        return "q1" if ch == "/" else "dead"
    if state == "q1":
        return "q2" if ch == "*" else "dead"
    if state == "q2":
        return "q3" if ch == "*" else "q2"
    if state == "q3":
        if ch == "/":
            return "q4"
        if ch == "*":
            return "q3"
        return "q2"
    if state == "q4":
        return "q4"
    return "dead"

def run_dfa(s):
    state = "q0"
    entered_body = False
    for ch in s:
        state = step(state, ch)
        if state in ("q2", "q3"):
            entered_body = True
        if state == "q4":
            break
    return state, entered_body

test_strings = ["/*hi*/", "/**/", "/* a * b */", "/* unterminated", "/*/"]

print(f"{'Input':<20}{'Result':<10}")
for s in test_strings:
    final_state, entered_body = run_dfa(s)
    result = "ACCEPTED" if final_state == "q4" else "REJECTED"
    print(f"{s:<20}{result:<10}")

print()
for s in test_strings:
    final_state, entered_body = run_dfa(s)
    if final_state != "q4":
        if entered_body:
            reason = "unterminated comment"
        else:
            reason = "not a comment at all"
        print(f"{s}: halted in {final_state} - {reason}")