"""Chọn 12–15 item lá mẫu cho PL kiểm (quy tắc SKILL.md §Chọn mẫu). Tái lập được: seed cố định.

Thứ tự áp quy tắc: 3 SWP cao nhất · 2 SWP thấp nhất · độ tin cậy thấp (tối đa 5) · đủ ≥ 3 item Constraint = 完納奨励金
· 2 ngẫu nhiên · bù ngẫu nhiên cho đủ 12. Một item trúng nhiều quy tắc thì ghi đủ các lý do, chỉ tính một lần.
"""
import random

SEED = 20261030
TOP_N, BOTTOM_N, LOW_CONF_MAX, CONSTRAINT_MIN, RANDOM_N, SAMPLE_MIN = 3, 2, 5, 3, 2, 12
CONSTRAINT_VALUE = "完納奨励金"


def select(leaves, seed=SEED):
    """leaves: dict có number, swp, confidence, constraint, epic. Trả về {number: [lý do chọn]}."""
    rng = random.Random(seed)
    chosen = {}

    def add(item, reason):
        chosen.setdefault(item["number"], []).append(reason)

    by_high = sorted(leaves, key=lambda x: (-x["swp"], x["number"]))
    seen_parent = set()
    for it in by_high:  # hòa điểm thì rải theo issue cha, tránh 3 mẫu là 3 phần của cùng một issue
        if len(seen_parent) == TOP_N:
            break
        if it.get("parent") not in seen_parent:
            seen_parent.add(it.get("parent"))
            add(it, f"SWP cao nhất ({it['swp']})")
    by_low = sorted(leaves, key=lambda x: (x["swp"], x["number"]))
    for it in by_low[:BOTTOM_N]:
        add(it, f"SWP thấp nhất ({it['swp']})")

    low = [x for x in leaves if x["confidence"] == "thấp"]
    # Ưu tiên item thấp vì luật không tìm thấy dấu hiệu (lỗi chấm tiềm ẩn) trước item thấp vì màn 概算 (đã biết lý do)
    no_signal = [x for x in low if not x.get("confidence_note")]
    rough = [x for x in low if x.get("confidence_note")]
    ordered = rng.sample(no_signal, len(no_signal)) + rng.sample(rough, len(rough))
    for it in _spread_by_epic(ordered, LOW_CONF_MAX):
        add(it, f"độ tin cậy thấp ({len(low)} item, chọn tối đa {LOW_CONF_MAX}, rải theo epic)")

    tagged = [x for x in leaves if x.get("constraint") == CONSTRAINT_VALUE]
    have = sum(1 for x in tagged if x["number"] in chosen)
    for x in tagged:
        if x["number"] in chosen:
            add(x, f"Constraint = {CONSTRAINT_VALUE}")
    pool = [x for x in tagged if x["number"] not in chosen]
    for it in rng.sample(pool, min(max(CONSTRAINT_MIN - have, 0), len(pool))):
        add(it, f"Constraint = {CONSTRAINT_VALUE} (bổ sung cho đủ {CONSTRAINT_MIN})")

    rest = [x for x in leaves if x["number"] not in chosen]
    need = max(RANDOM_N, SAMPLE_MIN - len(chosen))
    for it in rng.sample(rest, min(need, len(rest))):
        add(it, f"ngẫu nhiên (seed {seed})")
    return chosen


def _spread_by_epic(ordered, limit):
    """Chọn tối đa `limit` item theo thứ tự ưu tiên đã cho, mỗi epic một item trước để mẫu không dồn vào một nhóm."""
    if len(ordered) <= limit:
        return list(ordered)
    picked, seen = [], set()
    for it in ordered:
        if it["epic"] not in seen:
            picked.append(it)
            seen.add(it["epic"])
        if len(picked) == limit:
            return picked
    for it in ordered:
        if it not in picked:
            picked.append(it)
        if len(picked) == limit:
            break
    return picked
