from pathlib import Path
import json
import subprocess
import sys
import pytest

DATA = Path(__file__).parent / "data" / "sample.json"


@pytest.mark.parametrize(
    "args,expect",
    [
        (["--jmes", "b[].x"], [10, 20]),
        (["--jsonpath", "$.b[*].x"], [10, 20]),
    ],
)
def test_cli_query(args, expect):
    # call: python -m jsoncli.cli query <file> <args...>
    cmd = [sys.executable, "-m", "jsoncli.cli", "query", str(DATA), *args]
    p = subprocess.run(cmd, capture_output=True, text=True)
    # If extras are missing, CLI prints a friendly message; skip instead of failing.
    if "jmespath" in args and "requires: pip install '.[query]'" in p.stdout + p.stderr:
        pytest.skip("JMESPath not installed")
    if (
        "--jsonpath" in args
        and "requires: pip install '.[query]'" in p.stdout + p.stderr
    ):
        pytest.skip("JSONPath not installed")
    assert p.returncode == 0, p.stderr
    out = json.loads(p.stdout)
    assert out == expect
