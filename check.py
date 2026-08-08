#!/usr/bin/env python3
"""Checker for the integer-complexity board.

A submission is a JSON file:

    {"expression": "((1+1)*(1+1+1))"}

The expression may contain only the digit `1`, `+`, `*`, parentheses and spaces.
It must evaluate exactly to TARGET. The board is won when it does so using fewer
than BASELINE occurrences of `1`.

The expression is parsed by a small recursive-descent parser written out below —
deliberately, rather than by `eval`, which would execute whatever the submitter
sent. Restricting the *grammar* is what makes arbitrary input safe here; the
sandbox is the second line of defence, not the first.

Exit codes:  0 valid and beats the baseline · 1 valid but does not · 2 unreadable.
"""
import json, sys

TARGET   = 2**61 - 1          # the Mersenne prime M61
BASELINE = 150                # ones used by the published baseline expression
MAX_CHARS = 500_000           # bounds the work; the baseline is ~600 characters

def die(msg, code=2):
    print(f"REJECTED: {msg}")
    sys.exit(code)

class Parser:
    """expr := term ('+' term)* · term := factor ('*' factor)* · factor := '1' | '(' expr ')'

    Nothing else is accepted, so there is no construct through which a
    submission could express anything but a non-negative integer."""
    def __init__(self, s):
        self.s, self.i = s, 0
    def peek(self):
        while self.i < len(self.s) and self.s[self.i] == " ":
            self.i += 1
        return self.s[self.i] if self.i < len(self.s) else ""
    def expr(self):
        v = self.term()
        while self.peek() == "+":
            self.i += 1
            v += self.term()
        return v
    def term(self):
        v = self.factor()
        while self.peek() == "*":
            self.i += 1
            v *= self.factor()
        return v
    def factor(self):
        c = self.peek()
        if c == "1":
            self.i += 1
            return 1
        if c == "(":
            self.i += 1
            v = self.expr()
            if self.peek() != ")":
                raise SyntaxError(f"expected ')' at position {self.i}")
            self.i += 1
            return v
        raise SyntaxError(f"unexpected {c!r} at position {self.i}" if c
                          else "expression ended unexpectedly")

def main():
    if len(sys.argv) != 2:
        die("usage: check.py <submission.json>")
    try:
        with open(sys.argv[1]) as f:
            data = json.load(f)
    except Exception as e:
        die(f"could not read the submission as JSON: {e}")
    if not isinstance(data, dict) or "expression" not in data:
        die('the submission must be a JSON object with an "expression" key')
    s = data["expression"]
    if not isinstance(s, str):
        die('"expression" must be a string')
    if len(s) > MAX_CHARS:
        die(f"expression is {len(s)} characters; the limit is {MAX_CHARS}")

    allowed = set("1+*() ")
    bad = set(s) - allowed
    if bad:
        die(f"expression contains disallowed characters: {sorted(bad)!r}. "
            "Only the digit 1, +, *, parentheses and spaces are permitted — "
            "no other digits, no subtraction, no exponentiation.")

    sys.setrecursionlimit(20000)
    p = Parser(s)
    try:
        value = p.expr()
    except RecursionError:
        die("expression nests too deeply to parse")
    except SyntaxError as e:
        die(f"could not parse the expression: {e}")
    if p.peek():
        die(f"trailing input after a complete expression, at position {p.i}")

    ones = s.count("1")
    if value != TARGET:
        die(f"expression evaluates to {value}, not {TARGET}")

    print(f"valid: evaluates to {TARGET} using {ones} ones")
    if ones < BASELINE:
        print(f"ACCEPTED: {ones} < {BASELINE} — this improves on the published baseline")
        sys.exit(0)
    print(f"REJECTED: correct value, but {ones} ones does not beat the baseline of {BASELINE}")
    sys.exit(1)

if __name__ == "__main__":
    main()
