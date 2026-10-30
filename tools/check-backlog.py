"""Kiểm tra backlog (Phần 3 của B2).

Cục bộ (luôn chạy):
  - mọi WU trong handoff có issue, hoặc được ghi ở task-breakdown.md §2 là "chưa thành issue"
  - item lá có giờ, bội 0.5, 1h ≤ giờ ≤ 15h; backlog.yaml không có khóa SWP (SWP chỉ ở swp-report/swp-scores.yaml)
  - phụ thuộc tồn tại, không vòng; item đã xếp sprint thì phụ thuộc xếp cùng hoặc sớm hơn
  - mọi item E10 có Constraint = 完納奨励金
  - tải từng 担当(仮) mỗi Sprint ≤ capacity
--remote: so trường Project #2 và cha–con thật trên GitHub với YAML (cha = tổng con), thử truy cập ẩn danh.
  Từ B3b SWP phải CÓ trên mọi item: lá = điểm đã review trong swp-scores.yaml (pl_final, không có thì Scope × Complexity);
  cha / epic = tổng SWP các con thật trên Project.

Chạy:  python tools/check-backlog.py [--handoff PATH] [--remote]
"""
import json
import re
import sys
import urllib.request
from collections import defaultdict
from pathlib import Path

import yaml

import backlog_model as bm

REPO_ROOT = bm.TOOLS_DIR.parent
DEFAULT_HANDOFF = REPO_ROOT.parent / "product-a-fishmarket" / "specs" / "_meta" / "lab5_handoff.yaml"
SCORES_PATH = REPO_ROOT / "swp-report" / "swp-scores.yaml"
errors, notes = [], []


def check_local(meta, items, by_id, handoff):
    leaves = [i for i in items if i.is_leaf]
    if re.search(r"\bswp\s*:", bm.BACKLOG_PATH.read_text(encoding="utf-8"), re.I):
        errors.append("backlog.yaml có khóa 'swp' — SWP chỉ nằm ở swp-report/swp-scores.yaml")
    # WU coverage
    if handoff.exists():
        wus = {u["id"] for u in yaml.safe_load(handoff.read_text(encoding="utf-8"))["units"]}
        covered = {w for i in items for w in i.wu}
        breakdown = (REPO_ROOT / "task-breakdown.md").read_text(encoding="utf-8")
        missing = sorted(w for w in wus - covered if w not in breakdown)
        if missing:
            errors.append(f"WU không có issue và không ghi ở task-breakdown §2: {missing}")
        notes.append(f"WU handoff: {len(wus)} · có issue: {len(wus & covered)} · lạ: {sorted(covered - wus)}")
    else:
        notes.append(f"BỎ QUA đối chiếu WU: không thấy {handoff}")
    # hours
    for lf in leaves:
        h = lf.hours
        if h is None or h < 1 or h > meta["leaf_max_hours"] or (h * 2) % 1:
            errors.append(f"{lf.id}: giờ không hợp lệ ({h})")
        if not lf.owner or lf.owner not in meta["capacity"]:
            errors.append(f"{lf.id}: 担当(仮) không hợp lệ ({lf.owner})")
    # deps + sprint order
    for it in items:
        for d in it.deps:
            if d not in by_id:
                errors.append(f"{it.id}: phụ thuộc không tồn tại {d}")
    for lf in leaves:
        if lf.sprint is None:
            continue
        for dl in bm.dep_leaves(lf, by_id):
            if dl.sprint is None or dl.sprint > lf.sprint:
                errors.append(f"{lf.id} (Sprint {lf.sprint}) phụ thuộc {dl.id} (Sprint {dl.sprint})")
    _check_cycles(items, by_id)
    # constraint
    for it in items:
        if it.epic == "E10" and it.constraint != "完納奨励金":
            errors.append(f"{it.id}: thuộc E10 nhưng Constraint = {it.constraint}")
    # capacity
    load = defaultdict(float)
    for lf in leaves:
        if lf.sprint:
            load[(lf.sprint, lf.owner)] += lf.hours or 0
    for (s, who), h in sorted(load.items(), key=str):
        if h > meta["capacity"].get(who, 0):
            errors.append(f"Sprint {s}: {who} {h}h > capacity {meta['capacity'][who]}h")
    for s in sorted({k[0] for k in load}):
        row = {w: load[(s, w)] for w in meta["capacity"]}
        notes.append(f"Sprint {s}: {row} · tổng {sum(row.values()):g}h / {sum(meta['capacity'].values()):g}h")
    notes.append(f"Item: {len(items)} (epic {sum(i.level == 'epic' for i in items)}, issue "
                 f"{sum(i.level == 'issue' for i in items)}, sub-issue {sum(i.level == 'sub' for i in items)}) · "
                 f"lá {len(leaves)} · tổng giờ lá {sum(lf.hours for lf in leaves):g}h")


def _check_cycles(items, by_id):
    state = {}

    def visit(lf, path):
        if state.get(lf.id) == 1:
            errors.append(f"vòng phụ thuộc: {' → '.join(path + [lf.id])}")
            return
        if state.get(lf.id) == 2:
            return
        state[lf.id] = 1
        for dl in bm.dep_leaves(lf, by_id):
            visit(dl, path + [lf.id])
        state[lf.id] = 2

    for it in items:
        if it.is_leaf:
            visit(it, [])


def expected_swp():
    """(SWP đã review của lá: pl_final hoặc Scope × Complexity, lá đã đóng giữ giá trị cũ, số issue cha / epic)."""
    data = yaml.safe_load(SCORES_PATH.read_text(encoding="utf-8"))
    want = {r["number"]: r["pl_final"] if r.get("pl_final") is not None else r["swp"] for r in data["items"]}
    kept = {r["number"] for r in data["items"] if r.get("skip_write")}  # lá đã đóng có SWP: Project giữ giá trị cũ
    return want, kept, {p["number"] for p in data["parents"]}


def check_swp(board, parents, expected):
    """SWP có trên mọi item, khớp swp-scores.yaml; cha / epic = tổng SWP các con thật (đọc lại từ Project)."""
    want, kept, scored_parents = expected
    swp = {n: board[n]["values"].get("SWP") for n in board}
    for num, have in sorted(swp.items()):
        if have is None:
            errors.append(f"#{num}: SWP trống")
        elif num in scored_parents or num in kept:
            continue  # cha / epic: kiểm bằng tổng con thật bên dưới; lá đã đóng giữ giá trị cũ
        elif num not in want:
            errors.append(f"#{num}: có SWP {have} nhưng không có trong swp-scores.yaml")
        elif float(have) != float(want[num]):
            errors.append(f"#{num}: SWP = {have}, mong đợi {want[num]} (swp-scores.yaml)")
    kids = defaultdict(list)
    for child, parent in parents.items():
        if parent in board and child in board:
            kids[parent].append(child)
    for parent, children in sorted(kids.items()):
        total = sum(float(swp[c] or 0) for c in children)
        if swp[parent] is None or float(swp[parent]) != total:
            errors.append(f"#{parent}: SWP = {swp[parent]} ≠ tổng {len(children)} con {total:g}")
    leaves = [n for n in board if n not in kids]
    notes.append(f"SWP: {sum(v is not None for v in swp.values())}/{len(swp)} item có giá trị · {len(kids)} cha / epic "
                 f"= tổng con · tổng lá {sum(float(swp[n] or 0) for n in leaves):g}")


def check_remote(meta, items, by_id):
    from github_api import graphql_nodes
    from project_fields import F_STATUS, Project, desired_values
    mapping = json.loads(bm.MAP_PATH.read_text(encoding="utf-8"))
    repo, owner = meta["repo"], meta["project_owner"]
    board = Project(owner, meta["project_number"]).items(repo)
    q = """query($o:String!,$r:String!,$after:String){repository(owner:$o,name:$r){issues(first:100,after:$after){
     pageInfo{hasNextPage endCursor} nodes{number parent{number}}}}}"""
    parents = {n["number"]: (n["parent"] or {}).get("number")
               for n in graphql_nodes(q, {"o": owner, "r": repo.split("/")[1]}, ["repository", "issues"])}
    for it in items:
        num = mapping.get(it.id, {}).get("number")
        if num is None or num not in board:
            errors.append(f"{it.id}: chưa có issue / chưa ở Project")
            continue
        vals = board[num]["values"]
        for name, want in desired_values(it, meta).items():
            have = vals.get(name)
            if not ((have is None and want is None) or (have is not None and want is not None and str(
                    float(have) if isinstance(want, (int, float)) else have) == str(
                    float(want) if isinstance(want, (int, float)) else want))):
                errors.append(f"#{num} {it.id}: {name} = {have!r}, mong đợi {want!r}")
        if vals.get(F_STATUS) is None:
            errors.append(f"#{num} {it.id}: Status trống")
        want_parent = mapping.get(it.parent, {}).get("number")
        if it.parent and parents.get(num) != want_parent:
            errors.append(f"#{num} {it.id}: cha thật = {parents.get(num)}, mong đợi #{want_parent}")
    check_swp(board, parents, expected_swp())
    notes.append(f"Remote: đối chiếu {len(items)} item với Project #{meta['project_number']}")
    sample = [f"https://github.com/users/{owner}/projects/{meta['project_number']}"]
    sample += [mapping[k]["url"] for k in ("E10", "I-002", "I-062") if k in mapping]
    for url in sample:
        req = urllib.request.Request(url, headers={"User-Agent": "backlog-check"})  # không gửi cookie / token
        try:
            code = urllib.request.urlopen(req, timeout=20).status
        except Exception as exc:  # noqa: BLE001 — chỉ cần ghi lỗi truy cập
            code = exc
        (notes if code == 200 else errors).append(f"ẩn danh {url} → {code}")


def main():
    args = sys.argv[1:]
    handoff = Path(args[args.index("--handoff") + 1]) if "--handoff" in args else DEFAULT_HANDOFF
    meta, items, by_id = bm.load()
    check_local(meta, items, by_id, handoff)
    if "--remote" in args:
        check_remote(meta, items, by_id)
    for n in notes:
        print("·", n)
    for e in errors:
        print("✗", e)
    print("KẾT QUẢ:", "ĐẠT" if not errors else f"{len(errors)} lỗi")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
