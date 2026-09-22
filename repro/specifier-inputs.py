"""从可迭代对象构造时，成员形状一路带到哪里才炸

跑法：PYTHONPATH=src .venv/bin/python repro/specifier-inputs.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

import pickle

from packaging.specifiers import Specifier, SpecifierSet
from packaging.version import Version

CASES = [[Specifier(">=1.0")], [">=1.0"], [">=1.0", "junk"], [None], [Version("1.0")],
         [Specifier(">=1.0"), "<2.0"]]


def probe(ss, name):
    out = [f"{name:26s} constructed; str={str(ss)!r}"]
    for label, fn in (("contains", lambda: "1.5" in ss), ("filter", lambda: list(ss.filter(["1.5"]))),
                      ("to_range", lambda: str(ss.to_range())), ("is_unsatisfiable", lambda: ss.is_unsatisfiable()),
                      ("pickle", lambda: str(pickle.loads(pickle.dumps(ss))))):
        try:
            out.append(f"{label}={fn()!r}")
        except Exception as e:
            out.append(f"{label}!={type(e).__name__}")
    print(" ".join(out))


for case in CASES:
    try:
        probe(SpecifierSet(case), repr(case)[:26])
    except Exception as e:
        print(f"{repr(case)[:26]:26s} ctor -> {type(e).__name__}: {e}")
