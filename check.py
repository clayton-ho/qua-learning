"""Offline check: import an exercise file, find every QUA Program object in it, serialize each.

Usage: python check.py exercises/day1/hello_day1.py
No OPX or SaaS needed. Build errors (bad types, misuse of for_/declare) surface here;
config validation does NOT (that happens server-side).
"""
import importlib.util
import sys
from pathlib import Path

from qm import Program, generate_qua_script


def main(path: str) -> None:
    p = Path(path)
    spec = importlib.util.spec_from_file_location(p.stem, p)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    config = getattr(mod, "config", None)
    progs = {k: v for k, v in vars(mod).items() if isinstance(v, Program)}
    if not progs:
        sys.exit("No Program objects found at module level.")
    for name, prog in progs.items():
        print(f"\n===== {name} =====")
        print(generate_qua_script(prog, config))


if __name__ == "__main__":
    if len(sys.argv) != 2:
        sys.exit(__doc__)
    main(sys.argv[1])
