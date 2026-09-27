import re
from collections import namedtuple

Node = namedtuple('Node', ['op', 'left', 'right', 'value'])

def leaf(value):
    return Node(None, None, None, value)

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
            node = Node(op, node, right, None)
        return node

    def parse_T(self):
        node = self.parse_U()
        while self.peek() in ('*', '/'):
            op = self.advance()
            right = self.parse_U()
            node = Node(op, node, right, None)
        return node

    def parse_U(self):
        if self.peek() == '-':
            self.advance()
            operand = self.parse_U()
            return Node('neg', operand, None, None)
        return self.parse_F()

    def parse_F(self):
        tok = self.peek()
        if tok == '(':
            self.advance()
            node = self.parse_E()
            self.advance()
            return node
        self.advance()
        if re.fullmatch(r'\d+\.\d+|\d+', tok):
            return leaf(float(tok) if '.' in tok else int(tok))
        return leaf(tok)

def parse(expr):
    tokens = tokenize(expr)
    return Parser(tokens).parse_E()

def print_ast(node, indent=0):
    prefix = "  " * indent
    if node.op is None:
        print(f"{prefix}{node.value}")
    elif node.op == 'neg':
        print(f"{prefix}neg")
        print_ast(node.left, indent + 1)
    else:
        print(f"{prefix}{node.op}")
        print_ast(node.left, indent + 1)
        print_ast(node.right, indent + 1)

def evaluate(node):
    if node.op is None:
        return node.value
    if node.op == 'neg':
        return -evaluate(node.left)
    left = evaluate(node.left)
    right = evaluate(node.right)
    if node.op == '+':
        return left + right
    if node.op == '-':
        return left - right
    if node.op == '*':
        return left * right
    if node.op == '/':
        return left / right

expr = "2 + 3 * 4 - 6 / 2"
tree = parse(expr)

print(f"Expression: {expr}")
print("AST:")
print_ast(tree)

result = evaluate(tree)
python_result = eval(expr)

print(f"\nEvaluated result: {result}")
print(f"Python's own evaluation: {python_result}")
print(f"Match: {result == python_result}")