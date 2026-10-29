"""Gọi GitHub qua `gh` CLI (dùng phiên đăng nhập sẵn có, không đọc token).

JSON luôn truyền qua stdin (`--input -`) để tránh lỗi mã hóa tham số dòng lệnh trên Windows.
Tự chờ và thử lại khi gặp secondary rate limit / lỗi 5xx tạm thời.
"""
import json
import re
import subprocess
import time

RATE_LIMITED = re.compile(r"rate limit|abuse|submitted too quickly|HTTP 429", re.I)
# Lỗi tạm thời: chỉ thử lại cho lệnh idempotent. POST tạo mới có thể đã thành công dù mất response → không thử lại.
TRANSIENT = re.compile(r"HTTP 5\d\d|timeout|timed out|connection|EOF", re.I)


class GhError(RuntimeError):
    pass


def _run(args, payload=None, retries=10, idempotent=True):
    data = json.dumps(payload, ensure_ascii=False).encode("utf-8") if payload is not None else None
    for attempt in range(retries):
        proc = subprocess.run(["gh", *args], input=data, capture_output=True)
        out = proc.stdout.decode("utf-8", "replace")
        err = proc.stderr.decode("utf-8", "replace")
        if proc.returncode == 0:
            return json.loads(out) if out.strip() else None
        msg = err + out
        retry = RATE_LIMITED.search(msg) or (idempotent and TRANSIENT.search(msg))
        if retry and attempt < retries - 1:
            wait = min(60 * (attempt + 1), 300)
            print(f"  [gh] tạm bị giới hạn, chờ {wait}s rồi thử lại ({attempt + 1}/{retries})")
            time.sleep(wait)
            continue
        raise GhError(f"gh {' '.join(args[:3])} lỗi: {err.strip() or out.strip()}")
    raise GhError("hết số lần thử lại")


def graphql(query, variables=None):
    res = _run(["api", "graphql", "--input", "-"], {"query": query, "variables": variables or {}})
    if res and res.get("errors"):
        raise GhError(json.dumps(res["errors"], ensure_ascii=False))
    return res["data"]


def graphql_nodes(query, variables, path):
    """Phân trang GraphQL: query phải nhận $after và có pageInfo{hasNextPage endCursor} ở `path`."""
    after, nodes = None, []
    while True:
        data = graphql(query, {**variables, "after": after})
        conn = data
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
    return _run(args, body, idempotent=method != "POST")


def rest_all(path):
    """GET có phân trang, trả về danh sách phẳng."""
    pages = _run(["api", path, "--paginate", "--slurp"])
    return [row for page in pages for row in page]
