import pytest
from jsoncli.core import JsonTool

SAMPLE = {"a":1,"b":[{"x":10},{"x":20}],"c":{"d":True}}

def test_get_set_roundtrip():
    t = JsonTool(SAMPLE.copy())
    assert t.get("b.1.x") == 20
    t.set("b.0.x", 99)
    assert t.get("b.0.x") == 99

def test_keys():
    t = JsonTool(SAMPLE)
    assert set(t.keys()) == {"a","b","c"}

def test_find():
    t = JsonTool(SAMPLE)
    found = dict(t.find_by_key("x"))
    assert found["b.0.x"] == 10
    assert found["b.1.x"] == 20
