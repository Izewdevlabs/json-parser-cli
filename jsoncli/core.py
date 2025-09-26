# top of file
import copy
import json
from pathlib import Path
from typing import Any, Dict, List, Union

JSONLike = Union[Dict[str, Any], List[Any], str, int, float, bool, None]


class JsonPathError(Exception):
    pass


class JsonValidationError(Exception):
    pass


class JsonTool:
    def __init__(self, data: JSONLike):
        # defensive copy so callers/tests can't mutate shared state
        self.data = copy.deepcopy(data)

    @classmethod
    def load(cls, path: Union[str, Path]) -> "JsonTool":
        p = Path(path)
        try:
            text = p.read_text(encoding="utf-8-sig")
        except Exception:
            text = p.read_text(encoding="utf-8")
        return cls(json.loads(text))

    def pretty(self) -> str:
        return json.dumps(self.data, indent=2, ensure_ascii=False)

    def minify(self) -> str:
        return json.dumps(self.data, separators=(",", ":"), ensure_ascii=False)

    def keys(self) -> List[str]:
        if isinstance(self.data, dict):
            return list(self.data.keys())
        raise JsonPathError("Root is not a dict")

    def get(self, path: str) -> Any:
        parts = path.split(".")
        cur = self.data
        for part in parts:
            if isinstance(cur, list):
                idx = int(part)
                cur = cur[idx]
            elif isinstance(cur, dict):
                if part not in cur:
                    raise JsonPathError(f"Key {part} not found")
                cur = cur[part]
            else:
                raise JsonPathError(f"Cannot descend into {type(cur)}")
        return cur

    def set(self, path: str, value: Any):
        parts = path.split(".")
        cur = self.data
        for part in parts[:-1]:
            if isinstance(cur, list):
                idx = int(part)
                cur = cur[idx]
            elif isinstance(cur, dict):
                cur = cur.setdefault(part, {})
            else:
                raise JsonPathError(f"Cannot descend into {type(cur)}")
        last = parts[-1]
        if isinstance(cur, list):
            cur[int(last)] = value
        elif isinstance(cur, dict):
            cur[last] = value
        else:
            raise JsonPathError("Invalid set target")

    def find_by_key(self, key: str, prefix: str = ""):
        if isinstance(self.data, dict):
            for k, v in self.data.items():
                new_prefix = f"{prefix}.{k}" if prefix else k
                if k == key:
                    yield new_prefix, v
                if isinstance(v, (dict, list)):
                    yield from JsonTool(v).find_by_key(key, new_prefix)
        elif isinstance(self.data, list):
            for i, v in enumerate(self.data):
                new_prefix = f"{prefix}.{i}" if prefix else str(i)
                if isinstance(v, (dict, list)):
                    yield from JsonTool(v).find_by_key(key, new_prefix)
