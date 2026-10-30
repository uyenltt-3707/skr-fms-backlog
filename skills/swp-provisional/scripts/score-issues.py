"""Chấm SWP TẠM cho mọi item lá trong ảnh chụp, cộng cho cha / epic, chọn mẫu → swp-scores.yaml.

Chạy:  python score-issues.py --snapshot tmp/swp-snapshot.json --out swp-report/swp-scores.yaml
Chạy lại giữ nguyên pl_final / pl_reason đã điền trong file cũ (khóa theo số issue).
"""
import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

import yaml

import sample_selection
from swp_rubric import ALLOWED_SWP, PROVISIONAL_NOTE, score_leaf

SECTION = re.compile(r"^###\s+(.+)$", re.M)
KEEP_SECTIONS = ("mô tả", "tiêu chí xong", "description", "acceptance")
KIND = re.compile(r"\*\*Loại:\*\*[^/\n]*/\s*([^·\n]+?)\s*(?:·|$)", re.M)
CLOSED_LABEL = "chấm sau khi đóng"


def description_text(body):
    """Phần MÔ TẢ của issue: mục Mô tả + Tiêu chí xong; bỏ metadata (giờ, 担当, Iteration), câu DoD chung, chân trang."""
    parts = SECTION.split(body)
    if len(parts) < 3:
        return "\n".join(ln for ln in body.splitlines() if not ln.startswith(("<!--", ">", "**")))
    keep = []
    for head, text in zip(parts[1::2], parts[2::2]):
        if head.strip().lower().startswith(KEEP_SECTIONS):
            keep += [ln for ln in text.splitlines() if ln.strip() and not ln.startswith(">")
                     and "Định nghĩa xong chung" not in ln]
    return "\n".join(keep)


def root_of(num, by_num):
    while by_num[num]["parent"] in by_num:
        num = by_num[num]["parent"]
    return by_num[num]


def epic_label(root):
    m = re.match(r"\[Epic\]\s*(\S+)", root["title"])
    return m.group(1) if m else f"#{root['number']}"


def load_previous(path):
    if not path.exists():
        return {}
    old = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    rows = {r["number"]: r for r in old.get("items", [])}
    bad = [f"#{n} pl_final = {r['pl_final']!r}" for n, r in rows.items()
           if r.get("pl_final") is not None and r["pl_final"] not in ALLOWED_SWP]
    if bad:  # dừng sớm: giá trị ngoài thang (giờ, SP Fibonacci…) không được đi vào báo cáo hay Project
        raise SystemExit("pl_final phải là tích Scope × Complexity (1–25): " + ", ".join(bad))
    return rows


def build(snapshot, previous):
    by_num = {r["number"]: r for r in snapshot["issues"] if r["on_project"]}
    rows = []
    for r in by_num.values():
        if not r["is_leaf"] or r.get("item_type") == "Epic":
            continue
        body = r.get("original_body", r["body"]) if r["state"] == "closed" else r["body"]
        parent = by_num.get(r["parent"])
        if parent is None or parent.get("item_type") == "Epic":  # mô tả epic quá rộng → không làm ngữ cảnh
            parent = {"title": "", "body": ""}
        m = KIND.search(body)
        kind = m.group(1).strip() if m else ""
        parent_body = parent.get("original_body", parent["body"])  # cha đã đóng: cũng dùng mô tả ban đầu
        s = score_leaf(r["title"], kind, description_text(body), parent["title"],
                       parent["title"] + "\n" + description_text(parent_body))
        if r.get("original_missing"):
            s["confidence"], s["confidence_note"] = "thấp", "không đọc được mô tả ban đầu — chấm theo mô tả hiện tại"
        prev = previous.get(r["number"], {})
        rows.append({
            "number": r["number"], "title": r["title"], "url": r["url"], "epic": epic_label(root_of(r["number"], by_num)),
            "parent": r["parent"],
            "kind": kind, "constraint": r.get("constraint"), "state": r["state"], **s,
            "closed_note": (CLOSED_LABEL + " — chấm theo mô tả ban đầu") if r["state"] == "closed" else "",
            "skip_write": "đã đóng và đã có SWP — không ghi đè" if r["state"] == "closed" and r["swp_now"] is not None else "",
            "hours_ref": r.get("hours"), "sample": False, "sample_reasons": [],
            "pl_final": prev.get("pl_final"), "pl_reason": prev.get("pl_reason"),
        })
    rows.sort(key=lambda x: (x["epic"], x["number"]))
    for num, reasons in sample_selection.select(rows).items():
        row = next(x for x in rows if x["number"] == num)
        row["sample"], row["sample_reasons"] = True, reasons
    return rows, rollup(rows, by_num)


def rollup(rows, by_num):
    """Cha / epic: SWP = tổng SWP các con (lá dùng pl_final nếu PL đã chốt). Không chấm riêng."""
    value = {x["number"]: (x["pl_final"] if x["pl_final"] is not None else x["swp"]) for x in rows}
    kids = {}
    for r in by_num.values():
        if r["parent"] in by_num:
            kids.setdefault(r["parent"], []).append(r["number"])

    def total(num):
        if num in value:
            return value[num]
        return sum(total(c) for c in kids.get(num, []))

    parents = [{"number": n, "title": by_num[n]["title"], "level": by_num[n].get("item_type"),
                "children": sorted(kids[n]), "swp_sum": total(n)} for n in sorted(kids)]
    return parents


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--snapshot", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    snap = json.loads(Path(a.snapshot).read_text(encoding="utf-8"))
    out = Path(a.out)
    rows, parents = build(snap, load_previous(out))
    meta = {"note": PROVISIONAL_NOTE, "formula": "SWP = Scope × Complexity (1–25); cha / epic = tổng con",
            "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "snapshot_fetched_at": snap["fetched_at"], "repo": snap["repo"],
            "project": f"{snap['project_owner']}#{snap['project_number']}", "seed": sample_selection.SEED,
            "status": "bản nháp — SWP chỉ ghi lên Project bằng write-swp-to-project.py --confirm sau khi PL quyết mọi mẫu",
            "leaf_count": len(rows), "sample_count": sum(x["sample"] for x in rows),
            "hours_ref_note": "hours_ref chỉ dùng kiểm chéo giờ / SWP; KHÔNG dùng khi chấm"}
    header = f"# {PROVISIONAL_NOTE}\n# pl_final / pl_reason: PL điền cho item mẫu (và item muốn sửa); để trống = chưa quyết.\n"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(header + yaml.safe_dump({"meta": meta, "items": rows, "parents": parents}, allow_unicode=True,
                                           sort_keys=False, width=200), encoding="utf-8")
    print(f"Chấm {len(rows)} item lá · mẫu {meta['sample_count']} · cha {len(parents)} → {out}")


if __name__ == "__main__":
    main()
