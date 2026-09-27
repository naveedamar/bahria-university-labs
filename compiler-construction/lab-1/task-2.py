instructions = [
    "L1: x = 1",
    "y = 2",
    "L2: z = x + y",
    "if z > 10 goto L4",
    "y = y + 1",
    "L3: x = x - 1",
    "goto L2",
    "L4: print(z)",
    "z = z + 1",
    "L5: print(y)",
]


def find_leaders(instructions):
    leaders = {0}

    label_to_index = {}
    for i, instr in enumerate(instructions):
        if ":" in instr:
            label = instr.split(":")[0].strip()
            label_to_index[label] = i

    for i, instr in enumerate(instructions):
        if "goto" in instr:
            target_label = instr.strip().split("goto")[-1].strip()
            leaders.add(label_to_index[target_label])
            if i + 1 < len(instructions):
                leaders.add(i + 1)

    return sorted(leaders)


def make_blocks(instructions, leaders):
    blocks = []
    for idx, start in enumerate(leaders):
        end = leaders[idx + 1] if idx + 1 < len(leaders) else len(instructions)
        blocks.append(instructions[start:end])
    return blocks


leaders = find_leaders(instructions)
blocks = make_blocks(instructions, leaders)

print("Basic Blocks")
for num, block in enumerate(blocks, start=1):
    print(f"Block {num}:")
    for instr in block:
        print(f"  {instr}")
