"""Gọi GitHub qua `gh` CLI (dùng phiên đăng nhập sẵn có, không đọc token). Dùng riêng cho skill để skill tự chứa.

JSON truyền qua stdin để tránh lỗi mã hóa tham số dòng lệnh trên Windows. Tự chờ khi bị rate limit.
"""
import json
import re
import subprocess
import sys
import time

for _stream in (sys.stdout, sys.stderr):  # Windows: stdout chuyển hướng mặc định code page ANSI
    if hasattr(_stream, "reconfigure"):
        _stream.reconfigure(encoding="utf-8", errors="replace")

RATE_LIMITED = re.compile(r"rate limit|abuse|submitted too quickly|HTTP 429", re.I)


class GhError(RuntimeError):
    pass


def _run(args, payload=None, retries=6):
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8") if payload is not None else None
    for attempt in range(retries):
        proc = subprocess.run(["gh", *args], input=data, capture_output=True)
        out, err = proc.stdout.decode("utf-8", "replace"), proc.stderr.decode("utf-8", "replace")
        if proc.returncode == 0:
            return json.loads(out) if out.strip() else None
        if RATE_LIMITED.search(err + out) and attempt < retries - 1:
            wait = 60 * (attempt + 1)
            print(f"  [gh] bị giới hạn, chờ {wait}s ({attempt + 1}/{retries})")
            time.sleep(wait)
            continue
        raise GhError(f"gh {' '.join(args[:3])} lỗi: {(err or out).strip()}")
    raise GhError("hết số lần thử lại")


def graphql(query, variables=None):
    res = _run(["api", "graphql", "--input", "-"], {"query": query, "variables": variables or {}})
    if res and res.get("errors"):
        raise GhError(json.dumps(res["errors"], ensure_ascii=False))
    return res["data"]


def graphql_nodes(query, variables, path):
    """Phân trang: query nhận $after và có pageInfo{hasNextPage endCursor} ở `path`."""
    after, nodes = None, []
    while True:
        conn = graphql(query, {**variables, "after": after})
        for key in path:
            conn = conn[key]
        nodes.extend(conn["nodes"])
        if not conn["pageInfo"]["hasNextPage"]:
            return nodes
        after = conn["pageInfo"]["endCursor"]


def rest(method, path, body=None):
    args = ["api", path, "--method", method, "-H", "Accept: application/vnd.github+json"]
    if body is not None:
        args += ["--input", "-"]
    return _run(args, body)
