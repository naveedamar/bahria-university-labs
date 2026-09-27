import re

def tokenize(s):
    return re.findall(r'\d+\.\d+|\d+|[A-Za-z_]\w*|[()+\-*/]', s)

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def advance(self):
        tok = self.tokens[self.pos]
        self.pos += 1
        return tok

    def parse_E(self):
        node = self.parse_T()
        while self.peek() in ('+', '-'):
            op = self.advance()
            right = self.parse_T()
            node = (op, node, right)
        return node

    def parse_T(self):
        node = self.parse_U()
        while self.peek() in ('*', '/'):
            op = self.advance()
            right = self.parse_U()
            node = (op, node, right)
        return node

    def parse_U(self):
        if self.peek() == '-':
            self.advance()
            operand = self.parse_U()
            return ('neg', operand)
        return self.parse_F()

    def parse_F(self):
        tok = self.peek()
        if tok == '(':
            self.advance()
            node = self.parse_E()
            self.advance()
            return node
        return self.advance()

def parse(expr):
    tokens = tokenize(expr)
    p = Parser(tokens)
    return p.parse_E()

def print_tree(node, indent=0):
    prefix = "  " * indent
    if isinstance(node, tuple):
        op = node[0]
        print(f"{prefix}{op}")
        for child in node[1:]:
            print_tree(child, indent + 1)
    else:
        print(f"{prefix}{node}")

expressions = ["a - b - c", "8 / 4 / 2", "- a * b"]

for expr in expressions:
    tree = parse(expr)
    print(f"Expression: {expr}")
    print(f"Tree (tuple form): {tree}")
    print("Indented tree:")
    print_tree(tree)
    print()