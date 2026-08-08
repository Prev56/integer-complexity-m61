# Integer complexity of 2^61 − 1

A Problem Market board. Write `N = 2305843009213693951` using only `1`, `+`, `*` and parentheses,
with **fewer than 150** ones. Our published baseline uses exactly 150 (`baseline.txt`); the
information-theoretic floor is 116, so the gap is real.

```bash
./preflight.sh
docker build -t checker .
./run-checker.sh my_expression.json
```

Task and win condition: [`TASK.md`](TASK.md). Constraints as data: [`task.json`](task.json).
