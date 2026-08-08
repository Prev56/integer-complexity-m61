# Task — The integer complexity of the Mersenne prime 2^61 − 1

*Leaderboard board, container-verified. Package: `TASK.md` · `check.py` (the checker) ·
`baseline.txt` (our expression) · `Dockerfile` and `run-checker.sh` · `examples/` · `task.json`.*

---

## The problem

The **integer complexity** of `n`, written `‖n‖`, is the fewest `1`s needed to write `n` using
only addition, multiplication and parentheses. So `‖6‖ = 5`, because `6 = (1+1)*(1+1+1)` and
nothing shorter works.

It is an unreasonably difficult quantity. No efficient algorithm for it is known; values are
computed by exhaustive dynamic programming, which runs out long before the numbers here.

**Target:**

```
N = 2^61 - 1 = 2305843009213693951
```

the Mersenne prime `M61`. Being prime, it has no factorisation to exploit — any expression must
build it additively, which is what makes it hard.

**Find an expression for N using fewer than 150 `1`s.**

## Where the two numbers come from

**150 is ours, not a record.** It is what a Horner-style expansion in base 32767 costs, and
`baseline.txt` contains the expression. We publish it so you know exactly what to beat and can
verify the bar yourself.

**115.5 is a floor nobody can go below.** Any expression using `k` ones has value at most
`3^(k/3)`, so `‖N‖ ≥ 3·log₃(N) ≈ 115.5`, hence at least 116 ones.

The gap between 116 and 150 is the board. Something in it is almost certainly achievable — our
baseline uses one generic technique and no search at all.

## Win condition (locked)

An expression that evaluates exactly to `N` using fewer than 150 occurrences of `1`.

Permitted characters: `1`, `+`, `*`, `(`, `)` and spaces. **Nothing else** — no other digits, no
subtraction, no exponentiation, no repeated-squaring notation. The checker parses this grammar
with a small recursive-descent parser rather than evaluating your string, so anything outside it
is rejected before it can mean anything.

## Submission format

```json
{"expression": "((1+1)*(1+1+1))"}
```

## Check your work before submitting

```bash
./preflight.sh
docker build -t checker .
./run-checker.sh my_expression.json
```

Exit codes: `0` accepted · `1` correct value but not fewer than 150 ones · `2` not a valid
submission.

## Licensing

Submissions must be Apache-2.0 licensed so they can be archived and republished as part of a
permanent public record.
