"""Số liệu cho báo cáo HTML: phân bố SWP theo epic và kiểm tra chéo giờ / SWP.

Kiểm chéo (estimate.md quy tắc 6): tỉ lệ giờ / SWP của từng item so với tỉ lệ chung của epic chứa nó;
lệch quá ±50% → đánh dấu rà lại. Chỉ để rà, không dùng để tính giờ hay sửa SWP.
"""
from collections import defaultdict

DEVIATION_LIMIT = 0.5
BUCKETS = [(1, 4), (5, 8), (9, 12), (15, 16), (20, 25)]
CONSTRAINT_VALUE = "完納奨励金"


def final_swp(row):
    return row["pl_final"] if row.get("pl_final") is not None else row["swp"]


def draft_swp(row):
    return row.get("swp_draft", row["swp"])


def _effect(rows, before, after):
    return {"items": len(rows), "changed": sum(before(r) != after(r) for r in rows),
            "swp_before": sum(before(r) for r in rows), "swp_after": sum(after(r) for r in rows)}


def rule_effects(rows):
    """Tách hai bước: quy tắc R1–R3 (nháp → skill chấm lại) rồi PL chốt mẫu (skill chấm lại → pl_final).
    Mỗi Rx: item áp quy tắc, item đổi SWP, tổng trước / sau; pl_samples: mẫu PL quyết; total: nháp → giá trị chốt."""
    out = {rule: _effect([r for r in rows if rule in (r.get("rules") or [])], draft_swp, lambda r: r["swp"])
           for rule in ("R1", "R2", "R3")}
    out["pl_samples"] = _effect([r for r in rows if r.get("pl_final") is not None], lambda r: r["swp"], final_swp)
    out["total"] = _effect(rows, draft_swp, final_swp)
    return out


def _group_stats(rows):
    swp = sum(final_swp(r) for r in rows)
    hours = sum(float(r["hours_ref"] or 0) for r in rows)
    buckets = [sum(lo <= final_swp(r) <= hi for r in rows) for lo, hi in BUCKETS]
    return {"count": len(rows), "swp": swp, "mean": swp / len(rows) if rows else 0, "hours": hours,
            "h_per_swp": hours / swp if swp else 0, "buckets": buckets,
            "low_conf": sum(r["confidence"] == "thấp" for r in rows)}


def distribution(rows):
    """[(nhãn, stats)] theo epic + dòng riêng 完納奨励金 + dòng tổng."""
    by_epic = defaultdict(list)
    for r in rows:
        by_epic[r["epic"]].append(r)
    out = [(epic, _group_stats(by_epic[epic])) for epic in sorted(by_epic)]
    tagged = [r for r in rows if r.get("constraint") == CONSTRAINT_VALUE]
    out.append((f"Riêng {CONSTRAINT_VALUE} (Constraint)", _group_stats(tagged)))
    out.append(("Tổng", _group_stats(rows)))
    return out


def cross_check(rows):
    """Trả về (bảng epic, danh sách item lệch). Mỗi item lệch: row + ratio + epic_ratio + deviation."""
    by_epic = defaultdict(list)
    for r in rows:
        by_epic[r["epic"]].append(r)
    total = _group_stats(rows)
    epics, flagged = [], []
    for epic in sorted(by_epic):
        st = _group_stats(by_epic[epic])
        dev = st["h_per_swp"] / total["h_per_swp"] - 1 if total["h_per_swp"] else 0
        epics.append({"epic": epic, **st, "deviation": dev, "flag": abs(dev) > DEVIATION_LIMIT})
        for r in by_epic[epic]:
            if r["hours_ref"] is None or not st["h_per_swp"]:
                continue
            ratio = float(r["hours_ref"]) / final_swp(r)
            d = ratio / st["h_per_swp"] - 1
            if abs(d) > DEVIATION_LIMIT:
                flagged.append({**r, "ratio": ratio, "epic_ratio": st["h_per_swp"], "deviation": d})
    flagged.sort(key=lambda x: -abs(x["deviation"]))
    return epics, flagged, total
