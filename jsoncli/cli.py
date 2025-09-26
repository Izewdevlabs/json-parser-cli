from __future__ import annotations

import argparse
import json
import logging
import sys
from typing import List

from .core import JsonTool, JsonPathError, JsonValidationError

# Optional deps for query
try:
    import jmespath
except Exception:
    jmespath = None

try:
    from jsonpath_ng import parse as jsonpath_parse
except Exception:
    jsonpath_parse = None

logger = logging.getLogger("jsoncli")
logging.basicConfig(level=logging.ERROR)


def _load_tool(path: str) -> JsonTool:
    return JsonTool.load(path)


def parse_args(argv: List[str] | None = None) -> argparse.Namespace:
    p = argparse.ArgumentParser(prog="jsoncli", description="JSON Parser CLI")
    sub = p.add_subparsers(dest="cmd", required=True)

    # pretty
    sp = sub.add_parser("pretty", help="Pretty-print JSON")
    sp.add_argument("file")
    sp.add_argument("--indent", type=int, default=2)

    # minify
    sp = sub.add_parser("minify", help="Minify JSON")
    sp.add_argument("file")

    # keys
    sp = sub.add_parser("keys", help="List keys at root")
    sp.add_argument("file")

    # get
    sp = sub.add_parser("get", help="Get value at dot-path (e.g., a.b.0.c)")
    sp.add_argument("file")
    sp.add_argument("path")

    # set
    sp = sub.add_parser("set", help="Set value at dot-path")
    sp.add_argument("file")
    sp.add_argument("path")
    sp.add_argument("value", help="JSON literal (e.g., 42, true, [1,2])")
    sp.add_argument("--write", metavar="OUT", help="Write modified JSON to file")

    # find
    sp = sub.add_parser("find", help="Find by key")
    sp.add_argument("file")
    sp.add_argument("--key", required=True)

    # query
    sp = sub.add_parser("query", help="Run a JMESPath or JSONPath query")
    sp.add_argument("file")
    g = sp.add_mutually_exclusive_group(required=True)
    g.add_argument("--jmes", help="JMESPath expression")
    g.add_argument("--jsonpath", help="JSONPath expression")

    return p.parse_args(argv)


def main(argv: List[str] | None = None) -> int:
    ns = parse_args(argv)
    try:
        if ns.cmd == "pretty":
            print(_load_tool(ns.file).pretty())

        elif ns.cmd == "minify":
            print(_load_tool(ns.file).minify())

        elif ns.cmd == "keys":
            print("\n".join(_load_tool(ns.file).keys()))

        elif ns.cmd == "get":
            val = _load_tool(ns.file).get(ns.path)
            print(json.dumps(val, indent=2, ensure_ascii=False))

        elif ns.cmd == "set":
            tool = _load_tool(ns.file)
            try:
                value = json.loads(ns.value)
            except json.JSONDecodeError as e:
                raise SystemExit(f"Value must be valid JSON literal: {e}")
            tool.set(ns.path, value)
            if ns.write:
                with open(ns.write, "w", encoding="utf-8") as f:
                    f.write(tool.pretty())
            else:
                print(tool.pretty())

        elif ns.cmd == "find":
            tool = _load_tool(ns.file)
            for path, v in tool.find_by_key(ns.key):
                print(f"{path}\t{json.dumps(v, ensure_ascii=False)}")

        elif ns.cmd == "query":
            tool = _load_tool(ns.file)
            if ns.jmes:
                if not jmespath:
                    raise SystemExit("JMESPath support requires: pip install '.[query]'")
                result = jmespath.search(ns.jmes, tool.data)
                print(json.dumps(result, indent=2, ensure_ascii=False))
            else:
                if not jsonpath_parse:
                    raise SystemExit("JSONPath support requires: pip install '.[query]'")
                expr = jsonpath_parse(ns.jsonpath)
                matches = [m.value for m in expr.find(tool.data)]
                print(json.dumps(matches, indent=2, ensure_ascii=False))

        return 0

    except (JsonPathError, JsonValidationError) as e:
        logger.error(str(e))
        return 2
    except FileNotFoundError as e:
        logger.error(str(e))
        return 3
    except Exception as e:
        logger.exception("Unexpected error: %s", e)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
