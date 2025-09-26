from pathlib import Path
import json
from jsoncli.core import JsonTool

DATA = Path(__file__).parent / "data" / "sample.json"


def test_core_find_and_get():
    tool = JsonTool.load(DATA)
    # find_by_key
    found = dict(tool.find_by_key("x"))
    assert found["b.0.x"] == 10
    assert found["b.1.x"] == 20
    # get path
    assert tool.get("c.d") is True
