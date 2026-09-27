cfg = {
    "B1": ["B2"],
    "B2": ["B3"],
    "B3": ["B4", "B5"],
    "B4": ["B5"],
    "B5": [],
}

print("CFG Edges")
for block, successors in cfg.items():
    for succ in successors:
        print(f"{block} ---> {succ}")

def reachable(cfg, entry):
    visited = set()
    stack = [entry]
    while stack:
        node = stack.pop()
        if node not in visited:
            visited.add(node)
            for succ in cfg.get(node, []):
                if succ not in visited:
                    stack.append(succ)
    return visited

reached = reachable(cfg, "B1")
print(f"\nReachable from B1: {sorted(reached)}")

cfg["B7"] = ["B5"]

new_reached = reachable(cfg, "B1")
dead_blocks = set(cfg.keys()) - new_reached

print(f"\nAfter adding B7:")
print(f"Reachable: {sorted(new_reached)}")
print(f"Dead code (unreachable blocks): {sorted(dead_blocks)}")