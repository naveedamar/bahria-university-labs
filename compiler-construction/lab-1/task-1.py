# compilation 
program = "int x = 4; int y = 6; int z = x * y;"

statements = [s.strip() for s in program.split(";") if s.strip()]

print("Source Program")
for i, line in enumerate(statements, start=1):
    print(f"{i}: {line};")

keywords = {"int"}
tokens = []
for stmt in statements:
    for word in stmt.replace("*", " * ").replace("=", " = ").split():
        if word in keywords:
            ttype = "Keyword"
        elif word.isidentifier():
            ttype = "Identifier"
        elif word.isdigit():
            ttype = "Int"
        else:
            ttype = "Operator"
        tokens.append((word, ttype))

print("\nLexical Analysis (Tokenization)")
for lexeme, ttype in tokens:
    print(f"<{lexeme}, {ttype}>")

symbol_table = {}
errors = []
i = 0
while i < len(tokens):
    lexeme, ttype = tokens[i]
    if ttype == "Keyword" and lexeme == "int":
        var_name = tokens[i + 1][0]
        symbol_table[var_name] = "int"
        i += 3
        continue
    if ttype == "Identifier" and lexeme not in symbol_table:
        errors.append(f"'{lexeme}' used before declaration")
    i += 1

print("\nSemantic Analysis (Symbol Table)")
for name, vtype in symbol_table.items():
    print(f"{name}: {vtype}")
if errors:
    print("Errors:")
    for e in errors:
        print(f" - {e}")
else:
    print("No errors")

print("\nPhase-by-Phase Report")
print(f"Lexical Analysis: {len(tokens)} tokens")
print(f"Semantic Analysis: {len(symbol_table)} symbols, {len(errors)} errors")
print(f"Source Lines: {len(statements)} statements")