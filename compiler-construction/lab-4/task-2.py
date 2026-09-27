import re

def tokenize(s):
    tokens = []
    for match in re.finditer(r'\d+\.\d+|\d+|[A-Za-z_]\w*|[()+\-*/]', s):
        tokens.append((match.group(), match.start()))
    return tokens

class ParseError(Exception):
    pass

class Parser:
    def __init__(self, tokens, source):
        self.tokens = tokens
        self.pos = 0
        self.source = source

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else (None, len(self.source))

    def match(self, expected):
        value, position = self.peek()
        if value != expected:
            found = value if value is not None else "EOF"
            raise ParseError(f"Expected '{expected}', found '{found}' at position {position}")
        self.pos += 1
        return value

    def advance(self):
        value, position = self.peek()
        self.pos += 1
        return value, position

    def parse_E(self):
        node = self.parse_T()
        while self.peek()[0] in ('+', '-'):
            self.advance()
            self.parse_T()
        return node

    def parse_T(self):
        node = self.parse_U()
        while self.peek()[0] in ('*', '/'):
            self.advance()
            self.parse_U()
        return node

    def parse_U(self):
        if self.peek()[0] == '-':
            self.advance()
            return self.parse_U()
        return self.parse_F()

    def parse_F(self):
        value, position = self.peek()
        if value == '(':
            self.advance()
            node = self.parse_E()
            self.match(')')
            return node
        if value is None or not (value.isidentifier() or value.replace('.', '', 1).isdigit()):
            found = value if value is not None else "EOF"
            raise ParseError(f"Expected IDENTIFIER/NUMBER/'(', found '{found}' at position {position}")
        self.advance()
        return value

    def parse(self):
        node = self.parse_E()
        value, position = self.peek()
        if value is not None:
            raise ParseError(f"Expected EOF, found '{value}' at position {position}")
        return node

test_inputs = ["a + + b", "( a + b", "a b", "a +"]

for expr in test_inputs:
    tokens = tokenize(expr)
    p = Parser(tokens, expr)
    print(f"Input: '{expr}'")
    try:
        p.parse()
        print("Parsed successfully")
    except ParseError as e:
        print(f"ParseError: {e}")
    print()

print("Caret diagram for 'a + + b'")
expr = "a + + b"
tokens = tokenize(expr)
p = Parser(tokens, expr)
try:
    p.parse()
except ParseError as e:
    msg = str(e)
    pos = int(msg.split("position")[-1].strip())
    print(expr)
    print(" " * pos + "^")
    print(msg)