"""AI tự kiểm progress-report.md: so MỌI con số với dữ liệu đọc từ Project #2 (+ lịch sử progress-data/sprint1.yaml).

1. Bảng sinh tự động (§2 trạng thái, §2 theo 担当, §3 burndown): sinh lại từ Project, phải giống từng ký tự.
2. Câu khẳng định trong lời văn: kiểm bằng điều kiện tính từ Project + phụ thuộc trong backlog.yaml (carry-over, item bị chặn, ngày lệch, item SWP lớn, tải BE…).
3. Mọi con số còn lại trong lời văn: tìm nguồn — số liệu Project / cấu hình sprint / tài liệu repo (estimate.md, README…);
   không tìm được nguồn thì liệt kê để người đọc kiểm.
Kết quả in ra và ghi progress-data/self-check-progress-report.txt.

Chạy:  python tools/check-progress-report.py
"""
import re
import sys

import sprint_report_render as rr
import backlog_model as bm
import sprint_sim as ss

ROOT = ss.SPRINT_PATH.parent.parent
REPORT, OUT = ROOT / "progress-report.md", ss.SPRINT_PATH.parent / "self-check-progress-report.txt"
DOCS = ["estimate.md", "README.md", "PREMISE.md", "task-breakdown.md"]
# số có thể dính đơn vị (52%, 1,096h); số đứng sau chữ / - / # là mã (P2-3, E09, #14) → bỏ
NUM = re.compile(r"(?<![\w#./-])(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.\d+)?(?!\d)")


def main():
    sprint, sim = ss.load_sim()
    ctx = ss.read_board()
    blocks, leaves, rows = rr.build_blocks(ctx, sprint, sim)
    table = ss.status_table(leaves)
    text = REPORT.read_text(encoding="utf-8")
    ok, bad, lines = 0, 0, []

    def check(cond, what):
        nonlocal ok, bad
        ok, bad = ok + bool(cond), bad + (not cond)
        lines.append(f"{'ĐẠT ' if cond else 'LỆCH'} {what}")

    # 1. bảng sinh tự động
    for key, want in blocks.items():
        m = re.search(rf"<!-- sprint-sim:{key} -->\n(.*?)\n<!-- /sprint-sim:{key} -->", text, re.S)
        check(m and m.group(1) == want, f"bảng {key}: {want.count(chr(10)) - 1} dòng số liệu = sinh lại từ Project")

    # 2. câu khẳng định
    not_done = {n for n, lf in leaves.items() if lf["status"] != "Done"}
    carry = re.search(r"\*\*Carry-over sang Sprint 2 \((\d+) item\):\*\*(.*?)\n- ", text, re.S)
    listed = {int(x) for x in re.findall(r"#(\d+)", carry.group(2))} if carry else set()
    check(carry and int(carry.group(1)) == len(not_done) and listed == not_done,
          f"carry-over §2 = item chưa Done trên Project {sorted(not_done)}")
    check(all(leaves[n]["state"] == "CLOSED" for n in leaves if n not in not_done), "mọi item Done đã đóng issue")
    check(rows[1][3] == 0, "ngày 1 (11-02) không có SWP Done")
    check(all(rows[k][2] - rows[k][1] > rows[k - 1][2] - rows[k - 1][1] for k in range(2, 6)),
          "ngày 2–5 lệch tăng mỗi ngày")
    check(max(leaves, key=lambda n: leaves[n]["swp"]) == 244, "#244 là item SWP cao nhất Sprint 1")
    swp_rate = table["Done"][1] / sum(r[1] for r in table.values())
    hour_rate = table["Done"][2] / sum(r[2] for r in table.values())
    check(abs(swp_rate - hour_rate) < 0.03, f"tỷ lệ Done SWP {swp_rate:.1%} ≈ giờ {hour_rate:.1%}")
    check(f"{rows[-1][2]:g} / {rows[0][2]:g} SWP ({rows[-1][2] / rows[0][2]:.1%})" in text,
          f"cuối sprint còn {rows[-1][2]:g} / {rows[0][2]:g} SWP ({rows[-1][2] / rows[0][2]:.1%})")
    gaps = [r[2] - r[1] for r in rows]
    check(all((gaps[k] < gaps[k - 1]) == (rows[k][0] == "2026-11-10") for k in range(6, 11)),
          "ngày 6–10 lệch mở rộng, chỉ 11-10 thu hẹp")
    top3 = sorted(not_done, key=lambda n: -leaves[n]["swp"])[:3]
    top_swp = sum(leaves[n]["swp"] for n in top3)
    check(set(top3) == {244, 166, 243} and f"{top_swp:g} / {rows[-1][2]:g} SWP còn lại ({top_swp / rows[-1][2]:.0%})" in text,
          f"3 item SWP lớn nhất chưa Done {sorted(top3)} = {top_swp:g} SWP")
    be = [lf for lf in leaves.values() if lf["owner"] in ("BE-A", "BE-B")]
    check(sum(lf["hours"] for lf in be if lf["status"] == "Done") < sum(lf["hours"] for lf in be),
          "BE Sprint 1 dưới kế hoạch (điều kiện thêm BE đã chạm)")
    cap = ctx["meta"]["capacity"]
    be_load = [sum(lf["hours"] for lf in be if lf["owner"] == w) / cap[w] for w in ("BE-A", "BE-B")]
    check(all(0.99 <= x <= 1 for x in be_load), f"BE-A / BE-B xếp 99–100% trần ({be_load[0]:.1%}, {be_load[1]:.1%})")
    check(sim[14]["history"][-1][0] == "2026-11-05", "#14 xong 11-05")
    _check_blocked(ctx, text, not_done, check)
    _check_replan(ctx, sprint, leaves, not_done, check)

    # 3. con số trong lời văn
    known = {"sprint1.yaml / Project": _derived(sprint, table, rows, leaves, not_done)}
    docs = "\n".join((ROOT / d).read_text(encoding="utf-8") for d in DOCS)
    prose = re.sub(r"<!-- sprint-sim:(\w+) -->.*?<!-- /sprint-sim:\1 -->", "", text, flags=re.S)
    prose = re.sub(r"\d{4}-\d{2}-\d{2}|\d{1,2}-\d{2}(?=\D)|\d{1,2}/\d{1,2}|Sprint \d|`[^`]*`|\([^()]*\.(png|csv|yaml|md)\)",
                   "", prose)
    unsourced = []
    for m in NUM.finditer(prose):
        tok = m.group(0)
        val = float(tok.replace(",", ""))
        ctxt = prose[max(0, m.start() - 30):m.end() + 15].replace("\n", " ")
        if val in known["sprint1.yaml / Project"]:
            src = "Project / sprint1.yaml" + (" (số nhỏ ≤ 10: khớp yếu)" if val <= 10 else "")
        elif re.search(rf"(?<![\d.,]){re.escape(tok)}(?![\d])", docs):
            src = "tài liệu repo"
        else:
            unsourced.append(f"  {tok}: …{ctxt}…")
            continue
        lines.append(f"     số {tok} ← {src}")
    lines.append(f"Số trong lời văn không tìm được nguồn tự động ({len(unsourced)}) — người đọc kiểm:")
    lines.extend(unsourced or ["  (không có)"])
    summary = f"KẾT QUẢ: {ok} đạt, {bad} lệch · {len(unsourced)} số cần người kiểm"
    report = "\n".join([f"# Tự kiểm progress-report.md với Project #{ctx['meta']['project_number']}", *lines, summary])
    OUT.write_text(report + "\n", encoding="utf-8")
    print(report)
    sys.exit(1 if bad else 0)


def _check_blocked(ctx, text, not_done, check):
    """Dòng «Item bị chặn bởi carry-over»: mỗi #số không thuộc carry-over phải phụ thuộc (bắc cầu) vào một item carry-over;
    «#146 chặn trực tiếp N item» phải đúng N."""
    by_id, num = ctx["by_id"], {k: v["number"] for k, v in ctx["mapping"].items()}
    inv = {v: k for k, v in num.items()}

    def upstream(item_id, seen):
        for d in bm.dep_leaves(by_id[item_id], by_id):
            if d.id not in seen:
                seen.add(d.id)
                upstream(d.id, seen)
        return {num[i] for i in seen}

    line = re.search(r"\*\*Item bị chặn bởi carry-over\*\*(.*?)\n- ", text, re.S)
    nums = set()
    for a, b in re.findall(r"#(\d+)(?:〜#(\d+))?", line.group(1) if line else ""):
        nums |= set(range(int(a), int(b or a) + 1))
    blocked = {n for n in nums - not_done if n in inv}
    wrong = sorted(n for n in blocked if not upstream(inv[n], set()) & not_done)
    check(line and not wrong, f"{len(blocked)} item ghi «bị chặn» đều phụ thuộc carry-over" + (f" — sai: {wrong}" if wrong else ""))
    direct = [it for it in ctx["items"] if it.is_leaf and any(num[d.id] == 146 for d in bm.dep_leaves(it, by_id))]
    m = re.search(r"#146 chặn trực tiếp (\d+) item", text)
    check(m and int(m.group(1)) == len(direct), f"#146 chặn trực tiếp {len(direct)} item")


def _check_replan(ctx, sprint, leaves, not_done, check):
    """Đề xuất rút item (§4): item rút ở Sprint 2 và không item Sprint 2 nào phụ thuộc; #7, #8, #29, #60 (BE-B) thì có;
    carry-over ≈ 0.3 sprint năng lực cả đội."""
    by_id, num = ctx["by_id"], {k: v["number"] for k, v in ctx["mapping"].items()}
    s2 = ss.sprint_leaves(ctx, ctx["meta"]["sprints"][2])
    dependents_s2 = {}
    for n, lf in s2.items():
        for d in bm.dep_leaves(by_id[lf["id"]], by_id):
            dependents_s2.setdefault(num[d.id], set()).add(n)
    push = sprint.get("replan_push_to_sprint3", [])
    check(push and all(n in s2 and not dependents_s2.get(n) for n in push),
          f"item đề xuất rút {push} thuộc Sprint 2 và không có item Sprint 2 phụ thuộc")
    stuck = [7, 8, 29, 60]
    check(all(s2.get(n, {}).get("owner") == "BE-B" and dependents_s2.get(n) for n in stuck),
          f"BE-B {stuck} đều có item Sprint 2 phụ thuộc")
    share = sum(leaves[n]["hours"] for n in not_done) / sum(ctx["meta"]["capacity"].values())
    check(round(share, 1) == 0.3, f"carry-over ≈ {share:.2f} sprint năng lực cả đội")
    cap = ctx["meta"]["capacity"]
    beb = sum(lf["hours"] for lf in s2.values() if lf["owner"] == "BE-B") + sum(
        leaves[n]["hours"] for n in not_done if leaves[n]["owner"] == "BE-B") - cap["BE-B"]
    low = beb / sum(cap.values())
    check(beb == 23.5 and round(low, 1) == 0.1, f"BE-B vượt Sprint 2 {beb:g}h ≈ {low:.2f} sprint (cận dưới mức lùi mốc)")


def _derived(sprint, table, rows, leaves, not_done):
    vals = {len(sprint["workdays"]), 14, len(not_done), len(leaves), 23.5, 0.1,
            sum(leaves[n]["hours"] for n in not_done), round(100 * table["Done"][1] / rows[0][2], 1),
            round(100 * rows[-1][2] / rows[0][2], 1)}
    for count, swp, hours in table.values():
        vals |= {count, swp, hours}
    for _, ideal, actual, done in rows:
        vals |= {ideal, actual, done, round(actual - ideal, 1)}
    for who in {lf["owner"] for lf in leaves.values()}:
        mine = [lf for lf in leaves.values() if lf["owner"] == who]
        plan, done = sum(lf["hours"] for lf in mine), sum(lf["hours"] for lf in mine if lf["status"] == "Done")
        vals |= {plan, done, round(100 * done / plan), sum(lf["status"] != "Done" for lf in mine)}
    return vals


if __name__ == "__main__":
    main()
