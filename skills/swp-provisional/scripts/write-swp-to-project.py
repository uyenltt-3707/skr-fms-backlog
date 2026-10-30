"""Ghi SWP ĐÃ REVIEW từ swp-scores.yaml lên trường SWP của Project. Mặc định DRY-RUN (chỉ in kế hoạch).

Chạy:  python write-swp-to-project.py --scores swp-report/swp-scores.yaml            # dry-run
       python write-swp-to-project.py --scores swp-report/swp-scores.yaml --confirm  # ghi thật

Quy tắc an toàn (SKILL.md):
- chỉ ghi khi có --confirm VÀ mọi item mẫu đã có pl_final + pl_reason;
- giá trị lá = pl_final (nếu PL chốt) hoặc Scope × Complexity; phải là tích của hai số 1–5 → không thể là giờ hay SP Fibonacci;
- cha / epic = tổng con, tính lại tại đây; con bị giữ nguyên (đã đóng) thì cộng giá trị đang có trên Project;
- trạng thái đóng / mở lấy LIVE từ GitHub cho mọi cấp: đã đóng mà Project đã có SWP → không ghi đè;
  đã đóng mà mới chấm → gắn nhãn 「chấm sau khi đóng」 (gắn TRƯỚC khi ghi SWP để chạy lại không mất nhãn).
"""
import argparse
import sys
from pathlib import Path

import yaml

from gh_client import GhError, graphql, rest
from issue_snapshot import FIELD_SWP, project_items, project_meta
from swp_rubric import ALLOWED_SWP

CLOSED_LABEL = "chấm sau khi đóng"
_SET_Q = """mutation($p:ID!,$i:ID!,$f:ID!,$v:Float!){updateProjectV2ItemFieldValue(input:{projectId:$p,itemId:$i,
 fieldId:$f,value:{number:$v}}){clientMutationId}}"""


def leaf_value(row):
    """Giá trị lá đã review; ném ValueError nếu không hợp lệ."""
    if row.get("pl_final") is not None:
        v = row["pl_final"]
        if not isinstance(v, int) or v not in ALLOWED_SWP:
            raise ValueError(f"#{row['number']}: pl_final = {v!r} không phải tích Scope × Complexity (1–25)")
        return v
    if row["swp"] != row["scope"] * row["complexity"] or row["swp"] not in ALLOWED_SWP:
        raise ValueError(f"#{row['number']}: swp {row['swp']} ≠ Scope × Complexity")
    return row["swp"]


def plan(data, board):
    """Trả về (giá trị mong muốn, số issue giữ nguyên, lỗi chặn ghi). board: item Project live (có state, SWP hiện tại)."""
    blockers, values = [], {}
    for r in data["items"]:
        if r["sample"] and (r.get("pl_final") is None or not str(r.get("pl_reason") or "").strip()):
            blockers.append(f"mẫu #{r['number']} chưa có quyết định PL (pl_final + pl_reason)")
        try:
            values[r["number"]] = leaf_value(r)
        except ValueError as exc:
            blockers.append(str(exc))
    kept = set()
    for num, cur in board.items():  # issue đã đóng và đã có SWP: giữ nguyên, tổng của cha cộng đúng giá trị này
        have = cur["values"].get(FIELD_SWP)
        if cur["state"] == "closed" and have is not None:
            kept.add(num)
            values[num] = have
    kids = {p["number"]: p["children"] for p in data["parents"]}

    def total(n):
        if n not in values:
            values[n] = sum(total(c) for c in kids.get(n, []))
        return values[n]

    for n in kids:
        total(n)
    return values, kept, blockers


def ensure_label(repo):
    try:
        rest("POST", f"repos/{repo}/labels", {"name": CLOSED_LABEL, "color": "bfbfbf",
                                              "description": "SWP chấm sau khi issue đã đóng, theo mô tả ban đầu"})
    except GhError as exc:
        if "already_exists" not in str(exc):
            raise


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--scores", required=True)
    ap.add_argument("--confirm", action="store_true", help="ghi thật (mặc định chỉ in kế hoạch)")
    a = ap.parse_args()
    data = yaml.safe_load(Path(a.scores).read_text(encoding="utf-8"))
    owner, number = data["meta"]["project"].split("#")
    repo = data["meta"]["repo"]
    proj = project_meta(owner, int(number))
    board = project_items(owner, int(number), repo)
    values, kept, blockers = plan(data, board)
    if FIELD_SWP not in proj["fields"] or proj["fields"][FIELD_SWP]["type"] != "NUMBER":
        blockers.append(f"Project không có trường số '{FIELD_SWP}'")
    todo, closed_new = [], []
    for num, v in sorted(values.items()):
        cur = board.get(num)
        if cur is None:
            blockers.append(f"#{num} không có trên Project")
            continue
        have = cur["values"].get(FIELD_SWP)
        if num in kept or (have is not None and float(have) == float(v)):
            continue
        todo.append((num, cur["item_id"], v, have))
        if cur["state"] == "closed":
            closed_new.append(num)
    print(f"Kế hoạch: ghi {len(todo)} item · giữ nguyên {len(kept)} item đã đóng có SWP · "
          f"gắn nhãn '{CLOSED_LABEL}' cho {len(closed_new)} item")
    for num, _, v, have in todo[:20]:
        print(f"  #{num}: {have!r} → {v}")
    if blockers:
        print("CHẶN GHI:\n  - " + "\n  - ".join(blockers))
    if not a.confirm or blockers:
        print("DRY-RUN — không ghi gì." if not blockers else "Dừng — sửa các điểm chặn rồi chạy lại.")
        sys.exit(1 if blockers and a.confirm else 0)
    if closed_new:
        ensure_label(repo)
        for num in closed_new:
            rest("POST", f"repos/{repo}/issues/{num}/labels", {"labels": [CLOSED_LABEL]})
    field_id = proj["fields"][FIELD_SWP]["id"]
    for num, item_id, v, _ in todo:
        graphql(_SET_Q, {"p": proj["id"], "i": item_id, "f": field_id, "v": float(v)})
    print(f"XONG: đã ghi SWP cho {len(todo)} item.")


if __name__ == "__main__":
    main()
