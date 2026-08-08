#!/usr/bin/env python3
"""Prove the checker's ACCEPT path works.

Every other test in CI asserts that something is rejected. A checker that
rejected everything unconditionally would pass all of them and be worthless, so
this exercises the one branch they cannot reach: it loads the checker, lowers
only the winning threshold, and feeds it a submission that is valid but does not
beat the real bar. That submission must now be accepted with exit code 0.

Nothing here is used in judging — the shipped checker has no threshold knob, by
design. This is a unit test of the branch, not a configuration option.
"""
import importlib.util, sys, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
spec = importlib.util.spec_from_file_location("checker", root / "check.py")
checker = importlib.util.module_from_spec(spec)
spec.loader.exec_module(checker)

real = checker.BASELINE
checker.BASELINE = 200
sys.argv = ["check.py", str(root / "examples" / "valid-not-winning.json")]
try:
    checker.main()
except SystemExit as e:
    code = e.code
else:
    code = None

if code != 0:
    print(f"FAIL: with the threshold lowered from {real} to 200 the checker "
          f"exited {code}; expected 0. The accept path is unreachable.")
    sys.exit(1)
print(f"ok: accept path reached (threshold {real} -> 200 makes the example win)")
